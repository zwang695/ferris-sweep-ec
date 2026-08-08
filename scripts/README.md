# Project scripts

- `kicad-cli` runs KiCad 10 through Flatpak.
- `check-hardware` runs ERC, three DRCs, parity, and netlist assertions.
- `check-models` runs mapping and ADC-classifier behavioral tests.
- `check-firmware` lints and builds default/diagnostic UF2s on pinned upstream
  QMK.
- `generate-production` regenerates Gerbers, drills, BOM, placement, renders,
  and checksums.
- `generate-jlcpcb` creates the filtered wired-only JLCPCB PCBA/plate upload
  package, assembly drawings, and checksums.
- `check-all` runs the complete automated pre-fabrication gate.

The `import-tako-*` scripts are provenance-preserving baseline importers, not
normal build steps. They refuse to overwrite the active Revision A sources.

Examples:

```sh
./scripts/kicad-cli version
./scripts/check-all
./scripts/generate-jlcpcb
```

The Flatpak sandbox may request permission to access the project directory.
