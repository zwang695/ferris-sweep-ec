# JLCPCB wired prototype package

Run `./scripts/generate-jlcpcb` to create the upload-ready files under
`production/generated/jlcpcb/`. The package is for the wired Revision A only.
It does not populate controllers, controller sockets, optional feedback
jumpers, display/wireless parts, battery parts, sensor electrodes, or mounting
holes.

## Upload files

Create three JLCPCB orders:

| Order | Upload | Service |
|---|---|---|
| Controller/sensor panel | `controller-gerbers.zip`, then `controller-bom.csv` and `controller-cpl.csv` | Standard PCBA, both sides, mixed SMT/THT |
| Topre plate | `topre-plate-gerbers.zip` | PCB only |
| Bottom plate | `bottom-plate-gerbers.zip` | PCB only |

The controller Gerber is already a complete customer panel containing one left
and one right PCB. Declare **two different designs**, do not ask JLCPCB to
panelize it again, and choose **Complete file / proceed with my own files** when
the assembly uploader asks how to interpret panel placement data.

## Controller order settings

- FR-4, 2 layers, 230.7946 x 97.8403 mm as detected from the Gerbers.
- 1.6 mm finished thickness, 1 oz copper.
- ENIG surface finish; default ENIG gold thickness is acceptable.
- Customer panel, two different designs, mouse-bite separation.
- Standard PCBA, assemble both top and bottom sides.
- Select the lowest prototype PCB quantity offered and assemble at least two
  panels if required by the service minimum.
- Remove the JLCPCB order number. Do not permit an order number, label, or
  silkscreen addition over any exposed EC sensor electrode.
- Select Confirm Production File if offered.
- Do not order a separate stencil unless you personally want one; PCBA includes
  the production stencil process.

At BOM review, all 38 designators must match. Do not substitute a different
package for any part. Stock can change, so confirm each MPN, JLCPCB part number,
package, and quantity in the order UI.

## Plate orders

Topre plate:

- FR-4, 2 layers, 111.7465 x 97.8403 mm.
- **1.2 mm** finished thickness, 1 oz copper, ENIG.
- One design; order the minimum quantity offered. Two identical boards are
  needed per keyboard and one is flipped for the opposite hand.

Bottom plate:

- FR-4, 2 layers, 114.0803 x 97.8403 mm.
- 1.6 mm finished thickness, 1 oz copper, ENIG.
- One design; order the minimum quantity offered. Two identical boards are
  needed per keyboard and one is flipped for the opposite hand.

For both plate orders, preserve all routed internal cutouts, plated rings, and
separate PTH/NPTH drill files. Reject CAM requests to close or move them.

## Required placement review

JLCPCB requires the customer to confirm rotations in its placement viewer.
Compare it with `controller-assembly-top.pdf` and
`controller-assembly-bottom.pdf` before paying. In particular:

- `U2`: 90 degrees; `U102`: 270 degrees.
- `U3`: 0 degrees; `U103`: 180 degrees.
- The pin-1 indicator for every IC must agree with the PDF and PCB copper.
- `J1` and `J101` must face outward toward their matching board edges.
- `RSW1` and `RSW101` must sit flat inside their outlines.

Stop and correct the CPL rather than approving a visibly rotated IC or jack.

## Intentionally not installed by JLCPCB

- `U1`, `U101`: socketable RP2040 CE controllers.
- `JP1`, `JP101`: optional op-amp feedback/gain resistors.
- `DISP1`, `DISP101`, `PSW1`, `PSW101`, and all `BAT_HOLE*` references.
- `SW1` through `SW17` and `SW101` through `SW117`: these are bare EC sensor
  electrodes, not switches to purchase.
- All `H*` references: mechanical holes, not components.

The controller footprints provide two 12-pin, 2.54 mm rows per half. After
PCBA, install four 1x12 female socket strips on the keyboard and matching male
pins on the two controllers, or ask a local electronics technician to do it.
The normal JLCPCB upload package deliberately does not pretend those two
separate socket strips are a single placeable `U1` component.

Finally, connect or disconnect TRRS only while both halves are unpowered.
