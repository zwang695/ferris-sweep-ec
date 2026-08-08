#!/usr/bin/env python3
"""Apply reviewed power-source declarations to the Revision A schematic."""

from pathlib import Path
from uuid import UUID, uuid5
import re


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMATIC_PATH = PROJECT_ROOT / "hardware/rev-a/ferris-sweep-ec.kicad_sch"
ROOT_UUID = "72340b64-d7ab-445f-b1ce-2d9b5de13513"
NAMESPACE = UUID("87fc5316-f731-4f0c-81dd-7bba20035e45")

PWR_FLAG_LIBRARY = r'''    (symbol "power:PWR_FLAG" (power) (pin_numbers hide) (pin_names (offset 0) hide) (in_bom yes) (on_board yes)
      (property "Reference" "#FLG" (at 0 1.905 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Value" "PWR_FLAG" (at 0 3.81 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_keywords" "flag power" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "Special symbol for telling ERC where power comes from" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "PWR_FLAG_0_0"
        (pin power_out line (at 0 0 90) (length 0)
          (name "" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
      (symbol "PWR_FLAG_0_1"
        (polyline
          (pts (xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27))
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
    )
'''


def stable_uuid(name: str) -> str:
    return str(uuid5(NAMESPACE, name))


def flag_instance(reference: str, x: float, y: float) -> str:
    symbol_uuid = stable_uuid(reference + ":symbol")
    pin_uuid = stable_uuid(reference + ":pin")
    return f'''  (symbol (lib_id "power:PWR_FLAG") (at {x:g} {y:g} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced)
    (uuid {symbol_uuid})
    (property "Reference" "{reference}" (at {x:g} {y - 1.905:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "PWR_FLAG" (at {x:g} {y - 3.81:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Footprint" "" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {pin_uuid}))
    (instances
      (project "ferris-sweep-ec"
        (path "/{ROOT_UUID}"
          (reference "{reference}") (unit 1)
        )
      )
    )
  )
'''


def main() -> None:
    source = SCHEMATIC_PATH.read_text()
    changed = False
    if '(symbol "power:PWR_FLAG"' not in source:
        library_anchor = "\n  )\n\n  (junction"
        if source.count(library_anchor) != 1:
            raise RuntimeError("Could not uniquely locate the lib_symbols terminator")
        source = source.replace(
            library_anchor,
            "\n" + PWR_FLAG_LIBRARY + "  )\n\n  (junction",
            1,
        )
        changed = True

    required_flags = [
        ("#FLG01", 119.38, 21.59),    # +3.3V
        ("#FLG02", 160.02, 26.67),    # GND
        ("#FLG0101", 287.02, 21.59),  # +3.3V_R
        ("#FLG0102", 361.95, 182.88), # GND_R
        ("#FLG03", 82.55, 182.88),    # firmware-switched POWER
        ("#FLG0103", 250.19, 182.88), # firmware-switched POWER_R
    ]
    missing_flags = [
        flag_instance(reference, x, y)
        for reference, x, y in required_flags
        if f'(reference "{reference}")' not in source
    ]
    if missing_flags:
        instance_anchor = "\n  (sheet_instances"
        if source.count(instance_anchor) != 1:
            raise RuntimeError("Could not uniquely locate sheet_instances")
        source = source.replace(
            instance_anchor,
            "\n" + "\n".join(missing_flags) + instance_anchor,
            1,
        )
        changed = True

    source = source.replace('(project "tako"', '(project "ferris-sweep-ec"')
    optional_dnp_uuids = {
        "032bb02a-55bf-4970-a26a-556f78ca5160",  # BAT_HOLE+101
        "0e7e894e-e218-4b03-b7d3-f1761d76b07f",  # BAT_HOLE+1
        "20d4dffc-61ae-4f28-977a-5a0c754c46d9",  # BAT_HOLE-1
        "f5770937-2c82-4668-b860-4751585211bc",  # BAT_HOLE-101
        "16ab6465-ab34-4424-893b-2924b547b532",  # PSW1
        "bd6ebe61-0dee-4359-b2e4-1b52aa3758b9",  # PSW101
        "6241d340-34ef-4ae8-92b8-dff7daeb4ec3",  # DISP1
        "6420b812-df1b-425c-969a-be8d1dffb793",  # DISP101
    }
    for symbol_uuid in optional_dnp_uuids:
        pattern = re.compile(
            r'(\(symbol [^\n]+\n\s+\(in_bom yes\) \(on_board yes\) \(dnp )'
            r'no(\)[^\n]*\n\s+\(uuid ' + re.escape(symbol_uuid) + r'\))'
        )
        source, substitutions = pattern.subn(r'\1yes\2', source)
        if substitutions > 1:
            raise RuntimeError(f"Duplicate optional symbol UUID {symbol_uuid}")
        if substitutions == 1:
            changed = True
        elif f"(uuid {symbol_uuid})" not in source:
            raise RuntimeError(f"Missing optional symbol UUID {symbol_uuid}")
    if changed:
        SCHEMATIC_PATH.write_text(source)
        print(f"Repaired {SCHEMATIC_PATH}")
    else:
        print("Revision A schematic power repairs already applied")


if __name__ == "__main__":
    main()
