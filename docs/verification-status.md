# Revision A verification status

Last automated run: 2026-08-08 with KiCad 10.0.5 and upstream QMK commit
`9caa5f871ddb9813c7370708be62d7a3e1cfeb75`.

| Gate | Status | Evidence |
|---|---|---|
| Provenance | Pass | Pinned Sweep, Tako, upstream QMK, and ssbb QMK revisions; copied hardware retains MIT notice and firmware GPL headers |
| Schematic | Pass with reviewed warnings | Zero ERC errors; eight exact warnings are allowlisted for intentional aliases, firmware-switched power, and frozen symbols |
| Controller PCB | Pass | Zero DRC violations and zero unconnected items |
| Topre plate | Pass | Zero DRC violations and zero unconnected items under scoped plated-cutout rules |
| Bottom plate | Pass | Zero DRC violations and zero unconnected items under scoped mounting-barrel rules |
| Netlist contract | Pass | 34 sensors, eight row buses, ten mux routes, ADC, peak hold, power, and split nets asserted |
| Firmware | Pass | Default and diagnostic keymaps lint and compile to RP2040 CE UF2 on regular upstream QMK |
| Behavioral model | Pass | Mapping, threshold dimensions, hysteresis, drift, rapid taps, and simultaneous-key tests |
| Manufacturing output | Pass | Gerbers, separate PTH/NPTH drills, BOM, placement CSV, renders, UF2s, and checksums regenerate and pass structure checks |
| JLCPCB wired package | Pass | Filtered 38-placement BOM/CPL, top and bottom paste, mixed-assembly Gerbers, plate ZIPs, assembly drawings, and portable checksums |
| Absolute EC analog margin | Pending physical data | Real dome/spring capacitance and assembled parasitics are not available before fabrication |
| Physical keyboard | Pending fabrication | Requires assembly, ADC capture, threshold calibration, and functional testing |

The project is therefore **ready for informed prototype review**, not proven
production hardware. The generated package is intentionally ignored by Git so
it is always rebuilt from source.
