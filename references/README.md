# Reference policy

Third-party design files are admitted only after their source, revision, hash,
and license are recorded in `reference-audit.md`. The original Cipulot EC60 and
CorneECRevival GitHub URLs were unavailable during project initialization, so
unidentified mirrors must not silently become design authority.

Expected references:

- Ferris Sweep: physical key coordinates and ergonomic outline only.
- Corne EC Revival: split EC topology and mechanical variants.
- EC60: sensor, analog front end, STM32, USB, and calibration implementation.
- Another Cipulot EC board: independent cross-check of repeated circuitry.
- Current QMK `keyboards/cipulot/common`: firmware behavior and configuration
  contract.
- ST and analog-multiplexer manufacturer documentation: pin and electrical
  validation.
