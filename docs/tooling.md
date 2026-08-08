# Tooling and repeatable commands

No PCB-design experience is required to run or inspect the current checks.
Editing the design still benefits from learning KiCad's schematic and PCB
editors, but the release gates are command-line driven.

## Software

- Git, Python 3, GNU Make, and `rsync`.
- KiCad 10.0.x. This workspace uses the official Flatpak package so the GUI
  and `kicad-cli` stay on the same version.
- QMK CLI plus the ARM GNU toolchain. `qmk setup` installs/checks the normal
  QMK development prerequisites for your OS.
- A text editor. No third-party Python packages are required by this project.

On a Linux system with Flatpak:

```sh
flatpak install flathub org.kicad.KiCad
python3 -m pip install --user qmk
qmk setup
```

The project wrapper is `./scripts/kicad-cli`; KiCad also ships a real CLI, but
the wrapper selects the Flatpak installation used for this baseline.

## Main commands

```sh
./scripts/check-hardware
./scripts/check-models
./scripts/check-firmware
./scripts/generate-production
./scripts/check-all
```

`check-all` is the normal command. It writes ignored reports and fabrication
artifacts under `production/generated/`. The committed design sources remain
under `hardware/`, `mechanical/`, and `firmware/`.

## What I can help change

I can modify and verify the schematic, PCB, custom design rules, footprints,
plate files, QMK scanner/keymaps, tests, BOM, Gerbers, and documentation. I can
also analyze ADC logs after assembly and derive per-key thresholds. Your
unavoidable interventions are choosing/buying the physical Topre parts,
ordering and assembling the boards, taking measurements, and connecting real
hardware for final calibration.
