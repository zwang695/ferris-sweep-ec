# Ferris Sweep EC

An open, 34-key (`3x5+2` per half) Topre electrocapacitive split keyboard using
Ferris Sweep-style geometry and the known-built Tako Rev1 sensing architecture.

## Tooling

KiCad 10.0.5 is installed through Flatpak. Use `./scripts/kicad-cli` for
schematic ERC, PCB DRC, exports, and renders. QMK CLI 1.2.0 is also available;
firmware is kept reproducible in this repository rather than depending on the
machine's existing QMK checkout.

This repository is an engineering project. Files under `production/` are not
released for fabrication until every check in `docs/verification-plan.md` has
passed and the release is explicitly tagged as a prototype.

## Revision A goals

- Functional wired electrocapacitive keyboard.
- Separate, non-reversible left and right PCBs.
- 19.05 mm nominal key pitch with Sweep-style column stagger.
- 17 keys per half: three rows of five plus two thumb keys.
- Socketable Pro-Micro-pin-compatible RP2040 controller and local EC sensing
  front end on each half.
- QMK firmware with raw ADC diagnostics for post-assembly threshold tuning.
- USB-C on both halves for flashing and independent bring-up.
- Wired serial split transport.
- No RGB, display, encoder, wireless, or Vial in Revision A.

## Repository layout

- `docs/` — requirements, decisions, reference audit, and verification plan.
- `hardware/` — KiCad project and project-local libraries.
- `mechanical/` — layout coordinates, plate, and compression-stack files.
- `firmware/` — QMK keyboard implementation and keymaps.
- `simulation/` — analog-front-end models and ADC stimulus traces.
- `tests/` — schematic, PCB, firmware, and generated-output checks.
- `references/` — pinned upstream metadata; third-party files retain their
  original licenses and are not copied here until their provenance is clear.
- `production/` — generated Gerbers, drills, BOM, and placement files.

## Status

Controller PCB, Topre plate, bottom plate, and upstream-QMK firmware now pass
the automated pre-fabrication checks. The project remains a prototype: static
checks and behavioral models cannot replace calibration with real domes,
springs, housings, and fabricated sensor electrodes.

Run `./scripts/check-all` for the complete automated gate. See
`docs/tooling.md`, `docs/verification-status.md`, `docs/bom.md`, and
`docs/bring-up.md` for setup, evidence, parts, and physical validation. The
Tako/Cipulot comparison is in `docs/ec-cross-check.md`.

For the wired JLCPCB fabrication and assembly package, run
`./scripts/generate-jlcpcb` and follow `production/jlcpcb/README.md`.
