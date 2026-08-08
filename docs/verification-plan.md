# Verification plan

No individual check proves an EC keyboard. Release requires static electrical,
PCB, firmware, analog-model, mechanical, and generated-output evidence.

## Reference gate

- Pin every reference to a repository URL and commit or archived artifact hash.
- Record the license for every copied schematic, footprint, PCB, and source file.
- Compare EC Corne, EC60, and at least one other Cipulot EC implementation by
  subsystem.
- Resolve every intentional difference in the decision log.

## Schematic gate

- KiCad ERC has no unexplained errors or warnings.
- Controller-module symbol pin numbers match the RP2040 CE converter and
  physical Pro Micro footprint.
- Power, reset, ADC, mux, rows, and split nets pass scripted
  connectivity assertions.
- Decoupling and analog component values match the selected reference.

## PCB gate

- KiCad DRC has no unexplained errors or warnings.
- Embedded-footprint/library-copy mismatch reporting is disabled. Revision A
  deliberately freezes the geometry from the pinned, known-built Tako source;
  all electrical, clearance, outline, mask, and connectivity checks remain on.
- Sensor electrode and exclusion geometry match the selected reference.
- No unauthorized copper, vias, planes, or footprints occupy sensor keepouts.
- Board outlines, mounting holes, connector openings, and plates pass 1:1 and
  3D mechanical review.
- USB is owned by the socketed controller module; analog routing constraints
  pass on the carrier PCB.

## Firmware gate

- `qmk lint` passes.
- Default and diagnostic keymaps compile.
- Left and right logical matrices contain 17 populated and three unused cells.
- Generated ADC traces test press, release, drift, noise spikes, rapid taps, and
  simultaneous keys.
- Split transport mapping is verified for all 34 key positions.

## Analog-model gate

- The exact firmware hysteresis is tested against synthetic press, release,
  drift, threshold-band noise, rapid-tap, and simultaneous-key traces.
- Absolute sensor-capacitance and parasitic modeling remains pending measured
  physical parts. It cannot be used as pre-fabrication proof of signal margin.
- Press/release separation must be demonstrated with captured per-key ADC
  distributions after assembly.

## Manufacturing-output gate

- Gerbers, drills, netlist, BOM, and placement files regenerate from documented
  commands.
- Gerbers are inspected independently from the KiCad PCB view.
- Fabrication notes specify layer count, thickness, copper, soldermask, finish,
  and any stack details that influence sensing.
- Release is marked `prototype`; no claim of production validation is made.

## Physical validation after fabrication

- Verify shorts and rail resistance before power.
- Bring up and flash each half independently.
- Record raw ADC distributions for every key released and bottomed out.
- Calibrate and test false-press, missed-press, crosstalk, rollover, split-link,
  USB reconnect, suspend/resume, and extended idle behavior.
