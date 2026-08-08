# Reference audit

Status: primary sources pinned; available authoritative sources cross-checked.

| Reference | Intended use | Revision/hash | License | Retrieved | Notes |
|---|---|---|---|---|---|
| Ferris Sweep | key stagger and silhouette | `davidphilipbarr/Sweep@8ba72a256d627567660ecc0b6f51bb18fa8badb5` | Solderpad Hardware License 2.1 / Apache-2.0 option | 2026-08-08 | Sweep Mini is the coordinate reference; EC pitch remains 19.05 mm |
| Tako Rev1 | primary 34-key EC hardware | `ssbb/tako@5aa952ab5d5dc0c83aef36756252b27efc64e4cd` | MIT | 2026-08-08 | Manufactured design; OPA350, 74HC4051, controller module; only its Topre/OEM stack is in scope |
| Tako Rev0 | negative/control reference | same commit as Tako Rev1 | MIT | 2026-08-08 | Integrated STM32F4x1; author explicitly warns not to build it |
| Corne EC Revival | historical split EC architecture | unavailable | not yet independently recovered | no | original Cipulot repository URL currently returns not found; do not copy from unattributed mirrors |
| Cipulot EC60 | current electrical/firmware cross-check | `qmk/qmk_firmware@9caa5f871ddb9813c7370708be62d7a3e1cfeb75`, `keyboards/cipulot/ec_60` | GPL-2.0-or-later headers in firmware | 2026-08-08 | Current QMK configuration uses two muxes for 15 columns |
| Cipulot EC23U / EC60X | small/single-mux firmware cross-check | same QMK commit | GPL-2.0-or-later headers in firmware | 2026-08-08 | EC23U proves one mux for six columns; EC60X one mux for sixteen columns |
| Upstream QMK | final firmware build environment | `qmk/qmk_firmware@9caa5f871ddb9813c7370708be62d7a3e1cfeb75` | GPL and component licenses | 2026-08-08 | Revision A compiles and lints here; this is the final build target |
| Tako QMK firmware | split firmware provenance/regression reference | `ssbb/qmk_firmware@5d3c06185eee1663503bfd346dc5433c1a48a67a` | GPL-2.0-or-later headers in firmware | 2026-08-08 | Source of the known-working scanner and mapping; not a final build dependency |

## Required subsystem comparison

| Subsystem | Corne EC | EC60 | Additional EC | Revision A decision |
|---|---|---|---|---|
| Sensor electrode | source unavailable | current firmware only | Tako Rev1 EC pad | copy the MIT-licensed Tako Rev1 pad exactly, then verify dimensions |
| Peak hold/discharge | source unavailable | OPA-based interface expected from firmware contract | OPA350, 220 pF hold capacitor, 1 kOhm ADC isolation, MCU-controlled discharge | preserve Tako Rev1 topology and values |
| Analog mux | source unavailable | EC23U uses one mux for six columns | one 74HC4051 per half for five columns | one 74HC4051 per half |
| Row drive | source unavailable | four/five GPIO rows depending board | four GPIO rows per half | four GPIO rows per half |
| MCU/ADC | STM32-era design reported | supported by current ChibiOS code | supported RP2040 module | RP2040 module for replaceability and proven Rev1 path |
| Power/decoupling | source unavailable | board-specific | 3.3 V local rail, 100 nF local bypassing | reproduce and add explicit power flags/test points |
| USB/ESD | source unavailable | board-specific | provided by controller module | controller module owns USB for Revision A |
| Boot/reset/SWD | source unavailable | board-specific | module reset access | reset plus accessible module debug/test pads where possible |
| Split transport/power | historical split | n/a | serial plus power over TRRS | retain the proven TRRS/QMK serial mapping for Revision A; never hot-plug it |
| PCB sensor keepout | source unavailable | not represented in firmware | local copper and soldermask exclusions in EC footprint | copy exactly and test by rule/script |
| QMK configuration | unavailable | current adaptive Cipulot driver | known-working Tako split driver | start from Tako driver, retain raw-value diagnostic build |

The detailed scan-sequence and calibration comparison is recorded in
`docs/ec-cross-check.md`. The unavailable original Corne source remains a
provenance limitation, not a reason to copy an unattributed mirror.

## KiCad 10 baseline on untouched Tako Rev1

- ERC: 144 findings: 6 errors and 138 warnings. Most warnings are missing
  library/link metadata under the clean KiCad 10 environment.
- DRC: 67 findings: 9 errors and 58 warnings, with zero unconnected items.
- These results establish provenance and useful negative tests; they are not a
  waiver. This project's own source must pass with no unexplained findings.
