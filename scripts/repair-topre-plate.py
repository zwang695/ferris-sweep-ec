#!/usr/bin/env python3
"""Apply reviewed, plate-specific cleanup to the Topre plate PCB."""

from pathlib import Path

import pcbnew


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOARD_PATH = (
    PROJECT_ROOT
    / "mechanical/topre-plate/ferris-sweep-ec-topre-plate.kicad_pcb"
)


def disconnect_mechanical_holes(board: pcbnew.BOARD) -> bool:
    """Keep plated mounting holes mechanical instead of inventing a GND net.

    The upstream plate has no copper plane or schematic, so assigning its
    mounting-hole barrels to GND only creates thirteen impossible ratsnest
    connections.  Net zero accurately describes independent plated holes.
    """
    expected = {f"H{number}" for number in range(1, 15)}
    holes = {
        footprint.GetReference(): footprint
        for footprint in board.GetFootprints()
        if footprint.GetReference().startswith("H")
    }
    if set(holes) != expected:
        raise RuntimeError(
            f"Expected mounting holes {sorted(expected)}, got {sorted(holes)}"
        )

    changed = False
    for reference, footprint in holes.items():
        pads = list(footprint.Pads())
        if len(pads) != 1 or pads[0].GetDrillSize().x != pcbnew.FromMM(2.2):
            raise RuntimeError(f"Unexpected geometry for mounting hole {reference}")
        pad = pads[0]
        if pad.GetNetCode() not in (0, 1) or pad.GetNetname() not in ("", "GND"):
            raise RuntimeError(
                f"Unexpected net on {reference}: {pad.GetNetCode()} {pad.GetNetname()}"
            )
        if pad.GetNetCode() != 0:
            pad.SetNetCode(0)
            changed = True
    return changed


def remove_upstream_logo(board: pcbnew.BOARD) -> bool:
    """Remove the copied Tako mascot; it is cosmetic and clips a hole mask."""
    target_uuid = "e8d053e4-0469-4845-86e1-27394865b7ba"
    matches = [
        footprint
        for footprint in board.GetFootprints()
        if footprint.m_Uuid.AsString() == target_uuid
    ]
    if not matches:
        return False
    if len(matches) != 1:
        raise RuntimeError(f"Expected one upstream logo, found {len(matches)}")
    logo = matches[0]
    actual = (logo.GetReference(), logo.GetFPID().GetLibNickname(), logo.GetFPID().GetLibItemName())
    if actual != ("G***", "ferris_sweep_ec", "tako"):
        raise RuntimeError(
            f"The reviewed upstream logo changed ({actual}); refusing blind removal"
        )
    board.Remove(logo)
    return True


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    changed = disconnect_mechanical_holes(board)
    changed |= remove_upstream_logo(board)
    if changed:
        pcbnew.SaveBoard(str(BOARD_PATH), board)
        print(f"Repaired {BOARD_PATH}")
    else:
        print("Topre plate repairs already applied")


if __name__ == "__main__":
    main()
