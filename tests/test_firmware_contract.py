import json
from pathlib import Path
import re
import unittest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KEYBOARD = PROJECT_ROOT / "firmware/qmk/keyboards/ferris_sweep_ec"


def macro_body(text: str, name: str) -> str:
    match = re.search(
        rf"#define\s+{re.escape(name)}\s+(.+?)(?=\n\s*#define|\n\s*// clang-format on)",
        text,
        re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Missing macro {name}")
    return match.group(1)


class FirmwareContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = (KEYBOARD / "config.h").read_text(encoding="utf-8")
        cls.revision = (KEYBOARD / "rev_a/config.h").read_text(encoding="utf-8")
        cls.keyboard_json = json.loads((KEYBOARD / "rev_a/keyboard.json").read_text())
        cls.keymap_json = json.loads(
            (KEYBOARD / "keymaps/default/keymap.json").read_text()
        )

    def test_physical_layout_has_exactly_34_unique_cells(self) -> None:
        layout = self.keyboard_json["layouts"]["LAYOUT_split_3x5_2"]["layout"]
        cells = [tuple(key["matrix"]) for key in layout]
        self.assertEqual(len(cells), 34)
        self.assertEqual(len(set(cells)), 34)
        expected_left = {(row, col) for row in range(3) for col in range(5)} | {
            (3, 0), (3, 1)
        }
        expected_right = {(row, col) for row in range(4, 7) for col in range(5)} | {
            (7, 0), (7, 1)
        }
        self.assertEqual(set(cells), expected_left | expected_right)

    def test_every_keymap_layer_has_34_keys(self) -> None:
        self.assertEqual(self.keymap_json["keyboard"], "ferris_sweep_ec/rev_a")
        self.assertEqual(self.keymap_json["layout"], "LAYOUT_split_3x5_2")
        for layer in self.keymap_json["layers"]:
            self.assertEqual(len(layer), 34)

    def test_mux_channel_order_matches_netlist_contract(self) -> None:
        left = [int(value) for value in re.findall(r"\d+", macro_body(self.revision, "MATRIX_COL_CHANNELS"))]
        right = [int(value) for value in re.findall(r"\d+", macro_body(self.revision, "MATRIX_COL_CHANNELS_RIGHT"))]
        self.assertEqual(left, [4, 6, 2, 1, 3])
        self.assertEqual(right, [2, 4, 6, 7, 5])

    def test_threshold_matrices_are_valid_hysteresis_windows(self) -> None:
        for side in ("LEFT", "RIGHT"):
            low = [int(value) for value in re.findall(r"\d+", macro_body(self.config, f"EC_LOW_THRESHOLD_{side}"))]
            high = [int(value) for value in re.findall(r"\d+", macro_body(self.config, f"EC_HIGH_THRESHOLD_{side}"))]
            self.assertEqual(len(low), 20)
            self.assertEqual(len(high), 20)
            self.assertTrue(all(release < press for release, press in zip(low, high)))

    def test_rp2040_adc_pin_is_legal(self) -> None:
        self.assertIn("#define ANALOG_PORT F6", self.revision)
        # Pro Micro F6 maps to RP2040 GPIO 27 under the rp2040_ce converter.
        analog_source = (KEYBOARD / "ec_analog.c").read_text(encoding="utf-8")
        self.assertIn("case 27U: return TO_MUX(1, 0);", analog_source)


if __name__ == "__main__":
    unittest.main()
