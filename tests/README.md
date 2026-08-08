# Tests

`verify-netlist.py` asserts MCU, mux, sensing-cell, peak-hold, ADC, power, and
split-link connectivity from KiCad's generated XML netlist.

The standard-library unit tests assert the 34-key matrix contract, mux channel
order, legal RP2040 ADC mapping, threshold dimensions, hysteresis, drift,
rapid taps, and simultaneous-key classification. Run them with
`../scripts/check-models`.

Tests will include:

- KiCad ERC and DRC jobs;
- critical-net and pin-map assertions;
- sensor-keepout assertions;
- QMK lint and compilation;
- matrix-layout assertions;
- generated ADC trace tests;
- deterministic manufacturing-output generation.
