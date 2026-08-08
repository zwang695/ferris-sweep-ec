# Bring-up and end-to-end verification

## What can be proven before ordering

Run `./scripts/check-all`. It verifies KiCad ERC/DRC, PCB-to-schematic
electrical parity, explicit netlist contracts, all 34 matrix positions, mux
channel mapping, ADC pin legality, threshold behavior, current upstream QMK
lint/compile, Gerber/drill generation, and output-file structure.

Open the generated Gerbers in KiCad Gerber Viewer for the independent visual
check:

```sh
flatpak run org.kicad.KiCad
```

Use **File -> Open Gerber Plot File(s)** and load each directory under
`production/generated/*/gerbers`. Check the outline, all internal routes,
sensor-pad exposure, plate copper rings, mouse bites, and left/right labels.

These checks cannot prove the absolute ADC signal produced by a real conical
spring and dome. Capacitance depends on the actual parts, alignment,
compression, PCB dielectric, finish, contamination, and tolerances. A SPICE or
synthetic-trace test can validate the electronics and classifier assumptions,
but it cannot replace one fabricated sensor stack.

## First power-up

1. Break the controller panel into its two halves and inspect the routed edges.
2. With controllers absent, check resistance from each 3.3 V rail to its local
   ground; investigate a near-short before applying power.
3. Inspect OPA350 and 74HC4051 orientation and solder joints.
4. Socket one RP2040 CE controller on one half. Do not connect the TRRS cable.
5. Flash `production/generated/firmware/ferris_sweep_ec_rev_a_diagnostic_rp2040_ce.uf2`
   by entering the controller's UF2 bootloader and copying the file to its
   mounted drive.
6. Open QMK Console. Confirm all 20 logical ADC cells print; the three unused
   positions are ignored by the physical layout.
7. Touch each bare EC electrode. Its reading should rise independently; a
   neighbor rising similarly suggests a mux, row, contamination, or soldering
   fault.
8. Repeat independently on the other half.
9. Power down both halves, connect TRRS, then connect USB. Never insert or
   remove TRRS while USB power is present.
10. Verify all 34 logical positions with a keyboard tester before assembling
    the Topre stack.

## After installing housings, domes, and springs

Record at least 100 released samples and 100 fully pressed samples per key.
For every key, require released readings below the release threshold (650),
pressed readings above the actuation threshold (700), and comfortable margin
beyond both thresholds. If baselines cluster far from the inherited values,
calibrate thresholds from the measured distributions instead of guessing.

Check slow presses, rapid taps, all-key rollover, adjacent-key crosstalk,
split reconnect, USB reconnect, suspend/resume, and at least one extended idle
run. A single key with an unusually high released reading is most often a
misaligned spring/dome stack and should be mechanically inspected first.
