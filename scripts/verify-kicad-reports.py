#!/usr/bin/env python3
"""Fail unless generated KiCad reports match the reviewed Revision A baseline."""

from collections import Counter
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS = PROJECT_ROOT / "production/generated/reports"


def load(name: str) -> dict:
    path = REPORTS / name
    with path.open(encoding="utf-8") as report:
        return json.load(report)


def require_empty_drc(name: str) -> None:
    report = load(name)
    violations = report.get("violations", [])
    unconnected = report.get("unconnected_items", [])
    if violations or unconnected:
        raise SystemExit(
            f"{name}: expected no violations/unconnected items, got "
            f"{len(violations)}/{len(unconnected)}"
        )


def check_erc() -> None:
    report = load("controller-erc.json")
    violations = [
        violation
        for sheet in report.get("sheets", [])
        for violation in sheet.get("violations", [])
    ]
    counts = Counter(item["type"] for item in violations)
    expected = Counter(
        {"multiple_net_names": 2, "pin_to_pin": 2, "lib_symbol_mismatch": 4}
    )
    if counts != expected or any(item["severity"] != "warning" for item in violations):
        raise SystemExit(f"controller-erc.json: unexpected ERC baseline {counts}")

    descriptions = "\n".join(item["description"] for item in violations)
    required_fragments = (
        "APLEX_OUT_PIN_0 and DISCHARGE_PIN",
        "APLEX_OUT_PIN_0_R and DISCHARGE_PIN_R",
        "Bidirectional and Power output",
        "Symbol 'SW_SPDT'",
        "Symbol 'nice!view'",
    )
    missing = [fragment for fragment in required_fragments if fragment not in descriptions]
    if missing:
        raise SystemExit(f"controller-erc.json: expected warnings changed: {missing}")


def check_parity() -> None:
    report = load("controller-parity.json")
    if report.get("violations") or report.get("unconnected_items"):
        raise SystemExit("controller-parity.json: electrical DRC/connectivity is not clean")

    parity = report.get("schematic_parity", [])
    counts = Counter(item["type"] for item in parity)
    expected = Counter(
        {
            "duplicate_footprints": 1,
            "extra_footprint": 2,
            "footprint_symbol_field_mismatch": 78,
            "footprint_symbol_mismatch": 76,
        }
    )
    if counts != expected or any(item["severity"] != "warning" for item in parity):
        raise SystemExit(f"controller-parity.json: unexpected parity baseline {counts}")

    mechanical = [
        item
        for item in parity
        if item["type"] in {"duplicate_footprints", "extra_footprint"}
    ]
    if any(
        "mouse-bite-2mm-slot"
        not in " ".join(child["description"] for child in item.get("items", []))
        for item in mechanical
    ):
        raise SystemExit("controller-parity.json: unexpected extra/duplicate footprint")


def main() -> None:
    require_empty_drc("controller-drc.json")
    require_empty_drc("topre-plate-drc.json")
    require_empty_drc("bottom-plate-drc.json")
    check_erc()
    check_parity()
    print("KiCad reports match the reviewed Revision A baseline")


if __name__ == "__main__":
    main()
