"""Behavioral tests for the exact hysteresis used by ecsm_update_key()."""

import unittest


LOW = 650
HIGH = 700


def classify(samples: list[int], initial: bool = False) -> list[bool]:
    state = initial
    states = []
    for sample in samples:
        if state and sample < LOW:
            state = False
        elif not state and sample > HIGH:
            state = True
        states.append(state)
    return states


class AdcClassifierTests(unittest.TestCase):
    def test_press_and_release(self) -> None:
        states = classify([500, 620, 690, 701, 760, 680, 651, 649, 500])
        self.assertEqual(states, [False, False, False, True, True, True, True, False, False])

    def test_hysteresis_rejects_threshold_band_noise(self) -> None:
        self.assertEqual(classify([660, 699, 675, 651]), [False] * 4)
        self.assertEqual(classify([699, 680, 651], initial=True), [True] * 3)

    def test_drift_below_press_threshold_does_not_actuate(self) -> None:
        ramp = list(range(450, HIGH + 1, 5)) + list(range(HIGH, 449, -5))
        self.assertFalse(any(classify(ramp)))

    def test_rapid_taps(self) -> None:
        samples = [500, 760, 500, 760, 500, 760, 500]
        self.assertEqual(classify(samples), [False, True, False, True, False, True, False])

    def test_simultaneous_keys_are_independent(self) -> None:
        traces = [[500, 750, 750, 500], [500, 500, 780, 500], [500] * 4]
        self.assertEqual(
            [classify(trace) for trace in traces],
            [[False, True, True, False], [False, False, True, False], [False] * 4],
        )


if __name__ == "__main__":
    unittest.main()
