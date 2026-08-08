# Design decision log

## D-001: 34-key layout

- Decision: `3x5+2` per half.
- Reason: user requested Ferris Sweep style.
- Status: accepted.

## D-002: proven EC architecture

- Decision: derive sensing hardware from Cipulot EC references and current QMK
  EC code instead of designing a new capacitive-sensing method.
- Reason: minimize first-revision electrical risk.
- Status: accepted.

## D-003: controller family

- Decision: use a socketable Pro-Micro-pin-compatible RP2040 module for
  Revision A; do not fit an ATmega32U4 Pro Micro.
- Reason: the manufactured and supported Tako Rev1 uses this arrangement. Its
  author explicitly warns against building the integrated-STM32 Rev0. A
  replaceable module removes USB, crystal, regulator, boot, and fine-pitch MCU
  assembly from the first custom PCB while retaining a QMK-capable ADC.
- Status: accepted from reference evidence; revisit an integrated STM32 only
  after a working Revision A exists.

## D-004: separate PCBs

- Decision: separate, non-reversible left and right sensor PCBs.
- Reason: avoid compromises in sensor-side copper, analog routing, and assembly.
- Status: accepted.

## D-005: primary electrical reference

- Decision: use `ssbb/tako` Rev1 as the primary hardware reference and use
  current `qmk/qmk_firmware` Cipulot EC boards plus the ssbb Tako QMK fork as
  independent firmware/topology cross-checks.
- Reason: Tako Rev1 is MIT-licensed, 34-key, split, built in hardware, and
  explicitly credits Cipulot. It already uses a 4x5 logical matrix per half,
  OPA350 peak hold, and one 74HC4051 per half.
- Status: accepted.

## D-006: do not inherit reference violations

- Decision: recreate/clean the project in KiCad 10 and require clean ERC and
  DRC instead of declaring the imported reference reports acceptable.
- Reason: KiCad 10 reports six ERC errors and nine DRC errors on the untouched
  Tako Rev1 source, alongside warnings caused by missing/renamed libraries.
  The source has no unconnected PCB items, but its reports are not a release
  baseline for this project.
- Status: accepted.

## D-007: upstream QMK is the build target

- Decision: compile Revision A against a pinned commit of the regular
  `qmk/qmk_firmware` repository. Keep `ssbb/qmk_firmware` only as the
  known-working Tako reference.
- Reason: EC needs a custom analog matrix scanner, but it does not require QMK
  core changes. The local keyboard driver was ported to current GPIO,
  split-hand, metadata, and keycode APIs; it compiles to RP2040 UF2 and passes
  `qmk lint` on upstream commit
  `9caa5f871ddb9813c7370708be62d7a3e1cfeb75`.
- Status: accepted and build-verified.

## D-008: Topre-only mechanical stack

- Decision: Revision A supports Topre-compatible/OEM-style EC parts only. Use
  the reference 1.2 mm plate stack and do not create a NiZ plate variant.
- Reason: user selected Topre and explicitly removed the NiZ requirement;
  maintaining one proven stack reduces mechanical and sensing uncertainty.
- Status: accepted.

## D-009: retain the proven wired split link

- Decision: retain Tako Rev1's PJ-320A TRRS serial/power link for Revision A.
- Reason: replacing it would change a proven routed connector, bottom-plate
  cutout, power path, and firmware transport. It must never be hot-plugged.
- Status: accepted for the prototype; a keyed connector is a future revision.

## D-010: RP2040 Community Edition controller contract

- Decision: lock firmware and pins to QMK's `rp2040_ce` Pro Micro converter,
  while allowing any mechanically compatible controller implementing that
  pinout.
- Reason: this preserves GPIO 27 as the F6 ADC input, VBUS detection for split
  use, and the known-working physical module footprint without depending on a
  single small vendor's stock.
- Status: accepted and compile-verified.

## D-011: copied two-layer stack

- Decision: use two-layer, 35 um copper FR-4: 1.6 mm for the sensor PCB and
  bottom plate, and 1.2 mm for the Topre plate.
- Reason: these are the known-built Tako Rev1 stack values; the 1.2 mm housing
  plate is mechanically critical.
- Status: accepted and recorded in fabrication notes.

## Open decisions

- Exact Topre-compatible dome weight, spring, housing, and MX-compatible
  slider vendor.
- Exact RP2040 CE controller vendor/model for the first parts order.
