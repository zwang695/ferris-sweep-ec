# Ferris Sweep EC Revision A

Revision A is a 34-key split electrocapacitive keyboard derived from the
MIT-licensed ssbb Tako Rev1 hardware. It targets a Pro-Micro-pin-compatible
RP2040 module and uses a custom QMK matrix scanner for its OPA350/74HC4051 EC
front end.

Build from an upstream QMK checkout with this keyboard directory installed:

```sh
qmk compile -kb ferris_sweep_ec/rev_a -km default -e CONVERT_TO=rp2040_ce
```

Do not substitute an ATmega32U4 Pro Micro. Enable the QMK console during
bring-up to inspect raw sensor values and tune thresholds.
