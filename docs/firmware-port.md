# Upstream QMK port

Revision A builds on regular upstream QMK. No QMK core fork is required.

## Why the ssbb fork is still recorded

Tako's keyboard directory was not merged into upstream QMK, so the ssbb fork
is the authoritative source for its known-working RP2040 EC scan sequence,
split-hand pin mapping, and thresholds. Pinning it makes that provenance
reproducible; it does not make it a runtime or build dependency.

## Local changes for current upstream QMK

- migrated legacy `setPin*`/`writePin*` calls to current `gpio_*` APIs;
- migrated the split-side global `isLeftHand` to `is_keyboard_left()`;
- adopted `keyboard.json` as the leaf build marker;
- moved conditional make logic into `post_rules.mk`;
- updated retired mouse keycode aliases;
- retained the keyboard-local ADC and custom matrix implementation.

## Verified baseline

- Upstream: `qmk/qmk_firmware`
- Commit: `9caa5f871ddb9813c7370708be62d7a3e1cfeb75`
- Target: `ferris_sweep_ec/rev_a:default`
- Converter: `rp2040_ce`
- Result: UF2 linked successfully and `qmk lint` passed on 2026-08-08.
