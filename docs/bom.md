# Revision A build BOM

This is a wired, Topre-only build. Quantities below are for one complete split
keyboard (both halves). Exact manufacturer parts follow the known-built Tako
Rev1 where one was specified.

| Qty | Part | Package / note |
|---:|---|---|
| 2 | OPA350UA op amp | SOIC-8; TI OPA350 family |
| 2 | 74HC4051D analog mux | SOIC-16, 3.9 x 9.9 mm, 1.27 mm pitch |
| 4 | 100 nF capacitor | 0805, X7R or C0G, at least 6.3 V |
| 2 | 220 pF capacitor | 0805, C0G/NP0 preferred |
| 8 | 100 ohm resistor | 0805, 1% |
| 12 | 100 kohm resistor | 0805, 1% |
| 2 | 1 kohm resistor | 0805, 1% |
| 2 | 5.1 kohm resistor | 0805, 1% |
| 2 | Panasonic EVQPUC02K-compatible reset switch | PCB footprint is Panasonic EVQPUL/EVQPUC |
| 2 | PJ-320A TRRS jack | XKB Connectivity-compatible footprint |
| 2 | RP2040 Community Edition controller | Same model on both halves; USB-C recommended |
| 34 | Topre-compatible OEM housings | MX-compatible sliders required by housing orientation |
| 34 | MX-compatible Topre sliders | Match housings and keycaps |
| 34 | Topre domes | Select weight to preference |
| 34 | Conical springs | Match the dome family |
| 34 | Silencing rings, optional | Match slider/housing family |
| 16 | M2 x 6 mm standoffs | Maximum 3.4 mm outside diameter |
| 32 | M2 x 4 mm screws | For the outside plate stack |
| 12 | M1.6 x 6 mm standoffs | Six per half at the inner housing positions |
| 24 | M1.6 x 4 mm screws | For the inner plate stack |

The controller build target is QMK's `rp2040_ce` pinout. Compatible families
listed in the pinned QMK documentation include Liatris, Helios, Elite-Pi,
Frood, Sea-Picro EXT, and Splinky. Do not substitute an ATmega32U4 Pro Micro.
The SparkFun Pro Micro RP2040 uses a separate QMK converter target and is not
the locked Revision A firmware target.

## Do not populate

- `DISP1`, `DISP101`: display is outside Revision A scope.
- `PSW1`, `PSW101`: wireless/battery power switch.
- `BAT_HOLE+1`, `BAT_HOLE-1`, `BAT_HOLE+101`, `BAT_HOLE-101`: battery contacts.
- `JP1`, `JP101`: optional op-amp feedback/gain resistor; begin unpopulated,
  as in the reference build, and fit only during measured analog debugging.

The generated KiCad BOM excludes the first three groups automatically. The
sensor electrodes and mechanical mounting holes appear in source metadata but
are not purchased electronic components.
