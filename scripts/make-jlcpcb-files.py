#!/usr/bin/env python3
"""Create deterministic JLCPCB BOM and CPL files from the reviewed part map."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def split_designators(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parts", type=Path, required=True)
    parser.add_argument("--positions", type=Path, required=True)
    parser.add_argument("--bom", type=Path, required=True)
    parser.add_argument("--cpl", type=Path, required=True)
    args = parser.parse_args()

    with args.parts.open(newline="", encoding="utf-8") as source:
        part_rows = list(csv.DictReader(source))

    selected: set[str] = set()
    for row in part_rows:
        for reference in split_designators(row["Designator"]):
            if reference in selected:
                raise SystemExit(f"duplicate JLCPCB designator: {reference}")
            selected.add(reference)

    args.bom.parent.mkdir(parents=True, exist_ok=True)
    with args.bom.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(
            output,
            fieldnames=("Comment", "Designator", "Footprint", "JLCPCB Part #"),
        )
        writer.writeheader()
        for row in part_rows:
            writer.writerow({field: row[field] for field in writer.fieldnames})

    with args.positions.open(newline="", encoding="utf-8") as source:
        positions = {row["Ref"]: row for row in csv.DictReader(source)}

    missing = selected - positions.keys()
    if missing:
        raise SystemExit(f"selected parts missing from KiCad positions: {sorted(missing)}")

    with args.cpl.open("w", newline="", encoding="utf-8") as output:
        fields = ("Designator", "Mid X", "Mid Y", "Rotation", "Layer")
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for reference in sorted(selected):
            row = positions[reference]
            writer.writerow(
                {
                    "Designator": reference,
                    "Mid X": f'{float(row["PosX"]):.6f}',
                    "Mid Y": f'{float(row["PosY"]):.6f}',
                    "Rotation": f'{float(row["Rot"]) % 360:.6f}',
                    "Layer": "Top" if row["Side"].lower() == "top" else "Bottom",
                }
            )


if __name__ == "__main__":
    main()
