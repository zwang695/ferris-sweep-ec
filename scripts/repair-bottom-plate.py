#!/usr/bin/env python3
"""Apply reviewed metadata repairs to the Revision A bottom plate."""

from pathlib import Path

import pcbnew


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOARD_PATH = (
    PROJECT_ROOT
    / "mechanical/bottom-plate/ferris-sweep-ec-bottom-plate.kicad_pcb"
)


def repair_hole_references_and_nets(board: pcbnew.BOARD) -> bool:
    footprints = list(board.GetFootprints())
    duplicate_uuid = "80a4215a-0b50-4ffb-8cb0-d66f96549d3d"
    duplicate = [fp for fp in footprints if fp.m_Uuid.AsString() == duplicate_uuid]
    if len(duplicate) != 1:
        raise RuntimeError("Could not uniquely locate the reviewed duplicate H15")
    if duplicate[0].GetReference() == "H15":
        duplicate[0].SetReference("H17")
        changed = True
    elif duplicate[0].GetReference() == "H17":
        changed = False
    else:
        raise RuntimeError("The reviewed duplicate H15 changed unexpectedly")

    holes = [fp for fp in footprints if fp.GetReference().startswith("H")]
    expected = {f"H{number}" for number in range(1, 18)}
    actual = {fp.GetReference() for fp in holes}
    if len(holes) != 17 or actual != expected:
        raise RuntimeError(f"Unexpected bottom-plate holes: {sorted(actual)}")

    for footprint in holes:
        pads = list(footprint.Pads())
        if len(pads) != 1:
            raise RuntimeError(f"Unexpected pad count on {footprint.GetReference()}")
        pad = pads[0]
        if pad.GetNetCode() not in (0, 1) or pad.GetNetname() not in ("", "GND"):
            raise RuntimeError(f"Unexpected net on {footprint.GetReference()}")
        if pad.GetNetCode() != 0:
            pad.SetNetCode(0)
            changed = True
    return changed


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    changed = repair_hole_references_and_nets(board)
    if changed:
        pcbnew.SaveBoard(str(BOARD_PATH), board)
        print(f"Repaired {BOARD_PATH}")
    else:
        print("Bottom plate repairs already applied")


if __name__ == "__main__":
    main()
