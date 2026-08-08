# Firmware

The active QMK keyboard overlay is in `qmk/keyboards/ferris_sweep_ec`. It uses
the proven Tako split EC scan sequence and retains raw ADC console output for
bench validation.

Revision A targets a Pro-Micro-pin-compatible RP2040 module through QMK's
`rp2040_ce` converter. An ATmega32U4 Pro Micro is not supported: its ADC,
memory, and timing are not suitable for this design.

Revision A runs on regular upstream QMK with the Tako custom EC scanner adapted
to a split `4x5` logical matrix per half. No QMK core fork is required.

The default keymap remains intentionally minimal. The diagnostic keymap emits
raw ADC readings through QMK Console so the fixed per-key press and release
thresholds can be tuned after assembly. It does not claim automatic
calibration.
