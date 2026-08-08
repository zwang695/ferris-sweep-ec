#!/usr/bin/env python3
"""Assert the electrical contracts that generic ERC cannot express."""

from pathlib import Path
import xml.etree.ElementTree as ET


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NETLIST = PROJECT_ROOT / "production/generated/reports/controller-netlist.xml"


def main() -> None:
    root = ET.parse(NETLIST).getroot()
    nets = {
        net.attrib["name"]: {
            (node.attrib["ref"], node.attrib["pin"]) for node in net.findall("node")
        }
        for net in root.findall("./nets/net")
    }

    def require(net: str, *nodes: tuple[str, str]) -> None:
        missing = set(nodes) - nets.get(net, set())
        if missing:
            raise SystemExit(f"{net}: missing expected nodes {sorted(missing)}")

    # Firmware channel order must select the schematic's 74HC4051 inputs.
    left_mux_pins = ("1", "2", "15", "14", "12")  # A4, A6, A2, A1, A3
    right_mux_pins = ("15", "1", "2", "4", "5")  # A2, A4, A6, A7, A5
    for column, pin in enumerate(left_mux_pins):
        require(f"COL{column}", ("U2", pin))
    for column, pin in enumerate(right_mux_pins):
        require(f"COL{column}_R", ("U102", pin))

    # All 34 sensing cells must appear once in the expected 3x5+2 matrix.
    left_columns = (
        (1, 6, 11, 16),
        (2, 7, 12, 17),
        (3, 8, 13),
        (4, 9, 14),
        (5, 10, 15),
    )
    right_columns = (
        (101, 106, 111, 116),
        (102, 107, 112, 117),
        (103, 108, 113),
        (104, 109, 114),
        (105, 110, 115),
    )
    seen: set[str] = set()
    for side_suffix, columns in (("", left_columns), ("_R", right_columns)):
        for column, switches in enumerate(columns):
            for number in switches:
                ref = f"SW{number}"
                require(f"COL{column}{side_suffix}", (ref, "1"))
                if ref in seen:
                    raise SystemExit(f"Duplicate matrix cell {ref}")
                seen.add(ref)
    if len(seen) != 34:
        raise SystemExit(f"Expected 34 sensing cells, found {len(seen)}")

    left_rows = ((1, 2, 3, 4, 5), (6, 7, 8, 9, 10), (11, 12, 13, 14, 15), (16, 17))
    right_rows = (
        (101, 102, 103, 104, 105),
        (106, 107, 108, 109, 110),
        (111, 112, 113, 114, 115),
        (116, 117),
    )
    row_bus_nets = (
        "Net-(R1-Pad1)", "Net-(R2-Pad2)", "Net-(R3-Pad2)", "Net-(R4-Pad2)"
    )
    row_bus_nets_right = (
        "Net-(R101-Pad1)", "Net-(R102-Pad2)",
        "Net-(R103-Pad2)", "Net-(R104-Pad2)"
    )
    for row, switches in enumerate(left_rows):
        for number in switches:
            require(row_bus_nets[row], (f"SW{number}", "2"))
    for row, switches in enumerate(right_rows):
        for number in switches:
            require(row_bus_nets_right[row], (f"SW{number}", "2"))

    # Peak-hold, discharge, ADC, power, and split-link contracts, both halves.
    require("APLEX_OUT_PIN_0", ("U2", "3"), ("U3", "3"), ("C2", "1"), ("U1", "15"))
    require("APLEX_OUT_PIN_0_R", ("U102", "3"), ("U103", "3"), ("C102", "1"), ("U101", "9"))
    require("ADC", ("U3", "6"), ("U1", "18"), ("JP1", "2"))
    require("ADC_R", ("U103", "6"), ("U101", "18"), ("JP101", "2"))
    require("POWER", ("U1", "16"), ("U2", "16"), ("U3", "7"))
    require("POWER_R", ("U101", "8"), ("U102", "16"), ("U103", "7"))
    require("DATA", ("U1", "1"), ("J1", "C"))
    require("DATA_R", ("U101", "1"), ("J101", "C"))
    require("+3.3V", ("U1", "21"), ("J1", "D"))
    require("+3.3V_R", ("U101", "21"), ("J101", "D"))
    require("GND", ("U1", "3"), ("U2", "8"), ("U3", "4"), ("J1", "B"))
    require("GND_R", ("U101", "3"), ("U102", "8"), ("U103", "4"), ("J101", "B"))

    print("Schematic netlist satisfies the Revision A electrical contracts")


if __name__ == "__main__":
    main()
