# EC architecture cross-check

The active design is a cleaned Tako Rev1 derivative because Tako already is a
built, 34-key, split, Sweep-like EC keyboard. Re-laying it out from the older
Corne EC would add risk without changing the target. The original Cipulot
Corne EC repository could not be recovered from an authoritative upstream
location, so no file in this project is represented as a direct Corne copy.

## Hardware contract retained from Tako Rev1

- one 74HC4051 analog mux per half for five physical columns;
- four driven row buses per half, with three unused logical cells;
- paired EC electrode geometry copied without modification;
- OPA350 stage, 220 pF hold capacitor, 1 kohm isolation/feedback network, and
  10 us firmware discharge interval;
- local 3.3 V sensing power controlled by the controller;
- separate left/right nets and sensor routing;
- RP2040 CE module, GPIO 27 ADC input, and serial split link.

The XML netlist test checks those relationships independently of PCB net names,
and the mux-channel test ties the schematic's 4051 input pins to the exact QMK
channel arrays.

## Current Cipulot QMK comparison

| Behavior | Cipulot EC60 / common driver | EC23U / EC60X | Revision A |
|---|---|---|---|
| Scan sequence | select mux, pulse row, ADC read, discharge | same | same inherited sequence |
| Discharge | 10 us | 10 us | 10 us |
| ADC scale | 10-bit thresholds | 10-bit thresholds | 10-bit thresholds |
| Mux topology | two 8-channel muxes for 15 columns | one mux for 6 or 15 columns | one 8-channel mux for 5 columns per half |
| Press/release | separate thresholds | separate thresholds | fixed 700/650 hysteresis |
| Calibration | sampled noise floor and bottom-out scaling | same current common driver | raw console capture and manual per-build calibration |
| Rapid trigger | supported | supported | deliberately out of scope |
| Split support | not required by EC60 | board dependent | known-working Tako split mapping retained |

The modern Cipulot driver is stronger for per-key calibration and rapid
trigger. Porting all of it would be a firmware feature project, not a
requirement for first electrical function. Revision A keeps the smaller
known-working Tako scanner, exposes raw readings, and requires measured
threshold calibration during bring-up.
