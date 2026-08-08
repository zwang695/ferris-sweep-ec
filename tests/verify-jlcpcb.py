#!/usr/bin/env python3
"""Validate the generated wired-only JLCPCB upload package."""

from __future__ import annotations

import csv
import sys
import zipfile
from pathlib import Path


EXPECTED_PARTS = {
    "C38141": {"C1", "C3", "C101", "C103"},
    "C1805": {"C2", "C102"},
    "C17408": {"R1", "R2", "R3", "R4", "R101", "R102", "R103", "R104"},
    "C149504": {
        "R5", "R6", "R7", "R8", "R9", "R10",
        "R105", "R106", "R107", "R108", "R109", "R110",
    },
    "C17513": {"R11", "R111"},
    "C27834": {"R12", "R112"},
    "C79174": {"RSW1", "RSW101"},
    "C9386": {"U2", "U102"},
    "C2862236": {"U3", "U103"},
    "C22355837": {"J1", "J101"},
}
EXPECTED_REFS = set().union(*EXPECTED_PARTS.values())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def require_zip(path: Path, suffixes: tuple[str, ...]) -> None:
    if not zipfile.is_zipfile(path):
        raise SystemExit(f"{path}: not a valid zip archive")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        for suffix in suffixes:
            matches = [name for name in names if name.endswith(suffix)]
            if len(matches) != 1:
                raise SystemExit(f"{path}: expected one *{suffix}, found {matches}")
            data = archive.read(matches[0]).rstrip()
            terminator = b"M30" if suffix.endswith(".drl") else b"M02*"
            if not data.endswith(terminator):
                raise SystemExit(f"{path}: {matches[0]} has no {terminator!r}")


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("production/generated/jlcpcb")

    bom = read_csv(root / "controller-bom.csv")
    if tuple(bom[0]) != ("Comment", "Designator", "Footprint", "JLCPCB Part #"):
        raise SystemExit("JLCPCB BOM headers are not canonical")
    bom_refs: set[str] = set()
    for row in bom:
        refs = {item.strip() for item in row["Designator"].split(",")}
        part = row["JLCPCB Part #"]
        if EXPECTED_PARTS.get(part) != refs:
            raise SystemExit(f"unexpected mapping for {part}: {sorted(refs)}")
        if bom_refs & refs:
            raise SystemExit(f"duplicate BOM references: {sorted(bom_refs & refs)}")
        bom_refs |= refs
    if bom_refs != EXPECTED_REFS:
        raise SystemExit("JLCPCB BOM reference set does not match the reviewed wired build")

    cpl = read_csv(root / "controller-cpl.csv")
    if tuple(cpl[0]) != ("Designator", "Mid X", "Mid Y", "Rotation", "Layer"):
        raise SystemExit("JLCPCB CPL headers are not canonical")
    cpl_refs = {row["Designator"] for row in cpl}
    if cpl_refs != EXPECTED_REFS or len(cpl) != len(EXPECTED_REFS):
        raise SystemExit("JLCPCB CPL and BOM reference sets differ")
    side_counts = {
        side: sum(row["Layer"] == side for row in cpl) for side in ("Top", "Bottom")
    }
    if side_counts != {"Top": 32, "Bottom": 6}:
        raise SystemExit(f"unexpected JLCPCB placement side counts: {side_counts}")
    for row in cpl:
        float(row["Mid X"])
        float(row["Mid Y"])
        rotation = float(row["Rotation"])
        if not 0 <= rotation < 360:
            raise SystemExit(f"invalid normalized rotation: {row}")

    require_zip(
        root / "controller-gerbers.zip",
        (
            "F_Cu.gtl", "B_Cu.gbl", "F_Paste.gtp", "B_Paste.gbp",
            "F_Silkscreen.gto", "B_Silkscreen.gbo", "F_Mask.gts",
            "B_Mask.gbs", "Edge_Cuts.gm1", "-PTH.drl", "-NPTH.drl",
        ),
    )
    for name in ("topre-plate", "bottom-plate"):
        require_zip(
            root / f"{name}-gerbers.zip",
            (
                "F_Cu.gtl", "B_Cu.gbl", "F_Silkscreen.gto",
                "B_Silkscreen.gbo", "F_Mask.gts", "B_Mask.gbs",
                "Edge_Cuts.gm1", "-PTH.drl", "-NPTH.drl",
            ),
        )

    for name in ("controller-assembly-top.pdf", "controller-assembly-bottom.pdf"):
        data = (root / name).read_bytes()
        if not data.startswith(b"%PDF-") or len(data) < 10_000:
            raise SystemExit(f"missing or invalid assembly drawing: {name}")

    print("JLCPCB wired package has 38 reviewed placements and valid upload archives")


if __name__ == "__main__":
    main()
