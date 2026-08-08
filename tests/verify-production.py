#!/usr/bin/env python3
"""Lightweight independent structure checks for generated release artifacts."""

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATED = PROJECT_ROOT / "production/generated"


def require_terminated(path: Path, terminator: bytes) -> None:
    data = path.read_bytes().rstrip()
    if not data.endswith(terminator):
        raise SystemExit(f"{path}: missing {terminator!r} terminator")


def main() -> None:
    boards = {
        "controller": "ferris-sweep-ec",
        "topre-plate": "ferris-sweep-ec-topre-plate",
        "bottom-plate": "ferris-sweep-ec-bottom-plate",
    }
    gerber_suffixes = (
        "F_Cu.gtl", "B_Cu.gbl", "F_Silkscreen.gto", "B_Silkscreen.gbo",
        "F_Mask.gts", "B_Mask.gbs", "Edge_Cuts.gm1",
    )
    for directory, basename in boards.items():
        gerbers = GENERATED / directory / "gerbers"
        for suffix in gerber_suffixes:
            require_terminated(gerbers / f"{basename}-{suffix}", b"M02*")
        for kind in ("PTH", "NPTH"):
            require_terminated(gerbers / f"{basename}-{kind}.drl", b"M30")
        if (GENERATED / directory / "drill-report.txt").stat().st_size < 100:
            raise SystemExit(f"{directory}: drill report is unexpectedly small")
        render_name = "controller-top.png" if directory == "controller" else f"{directory}-top.png"
        render = (GENERATED / directory / render_name).read_bytes()
        if not render.startswith(b"\x89PNG\r\n\x1a\n") or len(render) < 10_000:
            raise SystemExit(f"{directory}: visual render is missing or invalid")

    for keymap in ("default", "diagnostic"):
        firmware = GENERATED / f"firmware/ferris_sweep_ec_rev_a_{keymap}_rp2040_ce.uf2"
        data = firmware.read_bytes()
        if len(data) % 512 or data[:4] != b"UF2\n":
            raise SystemExit(f"{keymap} firmware is not a structurally valid UF2 file")

    dnp_refs = {"DISP1", "DISP101", "PSW1", "PSW101", "BAT_HOLE"}
    with (GENERATED / "controller/bom.csv").open(newline="", encoding="utf-8") as bom:
        references = " ".join(row["Refs"] for row in csv.DictReader(bom))
    if any(reference in references for reference in dnp_refs):
        raise SystemExit("Generated BOM contains a Revision A DNP option")

    print("Generated Gerbers, drills, BOM, and UF2 pass structure checks")


if __name__ == "__main__":
    main()
