#!/usr/bin/env python3
"""Apply reviewed, UUID-addressed repairs to the Revision A KiCad PCB."""

from pathlib import Path

import pcbnew


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOARD_PATH = PROJECT_ROOT / "hardware/rev-a/ferris-sweep-ec.kicad_pcb"


def remove_redundant_col0_arc(board: pcbnew.BOARD) -> bool:
    """Remove a malformed legacy arc already covered by straight COL0 tracks."""
    target_uuid = "9c381fc0-a5ea-4821-bb59-16814484f50e"
    matches = [item for item in board.GetTracks() if item.m_Uuid.AsString() == target_uuid]
    if not matches:
        return False
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {target_uuid} item, found {len(matches)}")

    arc = matches[0]
    expected_start = (158.05142, 86.512459)
    expected_end = (158.05142, 85.785084)
    actual_start = tuple(pcbnew.ToMM(arc.GetStart()))
    actual_end = tuple(pcbnew.ToMM(arc.GetEnd()))
    if not isinstance(arc, pcbnew.PCB_ARC) or arc.GetNetname() != "COL0":
        raise RuntimeError("Target UUID is no longer the reviewed COL0 arc")
    for actual, expected in zip(actual_start + actual_end, expected_start + expected_end):
        if abs(actual - expected) > 0.001:
            raise RuntimeError("Target COL0 arc geometry changed; refusing blind repair")

    # Straight COL0 segments already span both arc endpoints. The legacy arc
    # has an invalid ~2.1 m center after conversion and creates a false/real
    # COL0-to-COL1 collision in KiCad 10.
    board.Remove(arc)
    return True


def solid_connect_reported_ground_pads(board: pcbnew.BOARD) -> bool:
    """Solid-connect five pads whose constrained geometry starves thermals."""
    targets = {
        "934a9451-b181-473d-97eb-efdc613eab5b": ("U103", "4", "GND_R"),
        "344b8ad4-067e-4343-9133-e59bbf31fd07": ("J1", "B", "GND"),
        "68306628-067c-408d-9b31-13db0707f9c1": ("DISP101", "4", "GND_R"),
        "f9a3b47e-8ab3-49f2-98b7-2123e81451c9": ("U2", "7", "GND"),
        "54e86d48-1124-43fd-afe5-57a4ff9d5122": ("U2", "13", "GND"),
    }
    pads = {
        pad.m_Uuid.AsString(): (footprint, pad)
        for footprint in board.GetFootprints()
        for pad in footprint.Pads()
    }
    changed = False
    for pad_uuid, (reference, number, net) in targets.items():
        if pad_uuid not in pads:
            raise RuntimeError(f"Missing reviewed thermal pad {pad_uuid}")
        footprint, pad = pads[pad_uuid]
        actual = (footprint.GetReference(), pad.GetNumber(), pad.GetNetname())
        if actual != (reference, number, net):
            raise RuntimeError(f"Thermal target changed: expected {(reference, number, net)}, got {actual}")
        if pad.GetLocalZoneConnection() != pcbnew.ZONE_CONNECTION_FULL:
            pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
            changed = True
    return changed


def remove_reported_silkscreen_clipping(board: pcbnew.BOARD) -> bool:
    """Remove only cosmetic silk primitives reported against pads/board edges."""
    graphic_uuids = {
        # Reset-switch silk clipped by the outer board edges.
        "3103b8ea-ae70-4587-8e18-9d8f69675c71",
        "2afc2ec4-e770-40c3-baf4-f64a17f36182",
        "0820e884-e135-40dd-ab07-becf981d345a",
        "19bb1b64-803f-403b-a4d9-268c6ba66836",
        # Mouse-bite guide arcs intentionally cross the breakaway edges.
        "fa093339-fe08-44ec-90a4-6b4435d87556",
        "14714a2e-de6a-4b5b-8d9a-2b1da0d4fd6b",
        "65982e9e-cb03-4dce-8623-0818f48675e7",
        "a454d717-31ec-4c34-bdf2-08468c054705",
        # TRRS outline segments clipped by its own through-hole pads.
        "8a8f40f2-b808-4596-bee9-5f939bf57baf",
        "0c9f3eac-cc85-4916-83ae-96a3fd4705e1",
        "7a15f556-f1f3-4d46-88e4-3c0eddfe51aa",
        "897f6a60-f3fd-4a0a-bae6-6c1aea7bfd84",
        "631954bd-ba65-4d71-88ef-cfbcb14425d2",
        "1af20254-fd34-4c53-9b29-034b51fcc11f",
    }
    reference_fields = {
        # Reference text placed over the component's own pads.
        "JP101": "0d6a87e2-0e73-4481-8c13-c5e7c3c69979",
        "R112": "1c3f08b5-9eaa-4ccd-9f6d-95fab2c0ff39",
    }

    changed = False
    graphics_to_remove = []
    for footprint in board.GetFootprints():
        for item in list(footprint.GraphicalItems()):
            item_uuid = item.m_Uuid.AsString()
            if item_uuid not in graphic_uuids:
                continue
            if item.GetLayer() != pcbnew.F_SilkS:
                raise RuntimeError(f"Reviewed silk item {item_uuid} changed layer")
            graphics_to_remove.append((footprint, item))
        if footprint.GetReference() in reference_fields:
            field = footprint.Reference()
            if field.m_Uuid.AsString() != reference_fields[footprint.GetReference()]:
                raise RuntimeError(f"Reference field for {footprint.GetReference()} changed")
            if field.IsVisible():
                field.SetVisible(False)
                changed = True
    for footprint, item in graphics_to_remove:
        footprint.Remove(item)
        changed = True
    return changed


def mark_out_of_scope_options_dnp(board: pcbnew.BOARD) -> bool:
    """Keep inherited battery/display footprints available but unpopulated."""
    expected = {
        "BAT_HOLE+1": "ferris_sweep_ec:bat_pin+",
        "BAT_HOLE+101": "ferris_sweep_ec:bat_pin+",
        "BAT_HOLE-1": "ferris_sweep_ec:bat_pin-",
        "BAT_HOLE-101": "ferris_sweep_ec:bat_pin-",
        "PSW1": "ferris_sweep_ec:SW_SPDT_SMD_PCM12",
        "PSW101": "ferris_sweep_ec:SW_SPDT_SMD_PCM12",
        "DISP1": "ferris_sweep_ec:nice_view",
        "DISP101": "ferris_sweep_ec:nice_view",
    }
    footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}
    changed = False
    for reference, footprint_id in expected.items():
        if reference not in footprints:
            raise RuntimeError(f"Missing optional footprint {reference}")
        footprint = footprints[reference]
        actual_id = (
            f"{footprint.GetFPID().GetLibNickname()}:"
            f"{footprint.GetFPID().GetLibItemName()}"
        )
        if actual_id != footprint_id:
            raise RuntimeError(f"Optional footprint {reference} changed to {actual_id}")
        if not footprint.IsDNP():
            footprint.SetDNP(True)
            changed = True
    return changed


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    changed = remove_redundant_col0_arc(board)
    changed |= solid_connect_reported_ground_pads(board)
    changed |= remove_reported_silkscreen_clipping(board)
    changed |= mark_out_of_scope_options_dnp(board)
    if changed:
        pcbnew.SaveBoard(str(BOARD_PATH), board)
        print(f"Repaired {BOARD_PATH}")
    else:
        print("Revision A board repairs already applied")


if __name__ == "__main__":
    main()
