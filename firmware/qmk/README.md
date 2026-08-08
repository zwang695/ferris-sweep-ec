# QMK firmware overlay

`keyboards/ferris_sweep_ec` is the project-owned QMK keyboard directory. It is
derived from the GPL-licensed ssbb Tako firmware pinned in the reference audit,
then ported to the current upstream QMK APIs. Original copyright and license
headers are preserved in each source file. The ssbb fork is a provenance and
regression reference, not a final build dependency.

The initial compile target is:

```sh
qmk compile -kb ferris_sweep_ec/rev_a -km default -e CONVERT_TO=rp2040_ce
```

The firmware remains diagnostic-first: console output exposes raw EC readings
so thresholds can be checked and calibrated once physical hardware exists.
The `diagnostic` keymap provides a plain one-layer position map and builds as a
separate UF2; the custom matrix prints the same raw readings in both builds.
