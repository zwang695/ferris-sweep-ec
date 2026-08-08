# Prototype fabrication notes

These settings preserve the pinned Tako Rev1 electrical and mechanical stack.
This is a prototype package, not a production-qualified release.

## Order quantities

| File set | Quantity | Construction |
|---|---:|---|
| `controller/gerbers` | 1 panel | Two routed halves joined by mouse bites |
| `topre-plate/gerbers` | 2 | One plate per half; flip one during assembly |
| `bottom-plate/gerbers` | 2 | One bottom per half; flip one during assembly |

## Stack settings

- Controller/sensor PCB: 2-layer FR-4, 1.6 mm finished thickness, 1 oz / 35 um
  copper, soldermask both sides.
- Topre plate: 2-layer FR-4, **1.2 mm finished thickness**, 1 oz / 35 um
  copper. Do not let the fabricator substitute 1.6 mm.
- Bottom plate: 2-layer FR-4, 1.6 mm finished thickness, 1 oz / 35 um copper.
- ENIG is recommended for flat, oxidation-resistant exposed sensor and plate
  copper. Keep the finish consistent across prototypes because it can affect
  the EC baseline.
- Any normal soldermask color is acceptable; keep it consistent during A/B
  testing.

## Routing and review notes

- Preserve all internal Topre housing routes and the copper/mask rings around
  them. They are intentional; do not apply an automatic copper-to-edge repair.
- Preserve the controller panel mouse bites and route outline.
- Plated and non-plated drill files are separate. Submit both.
- The controller is not reversible. The panel contains distinct left and right
  halves; do not mirror either Gerber set.
- The Topre and bottom files each describe one half. Two identical fabricated
  copies are used, with one physically flipped for the opposite hand.
- Request an engineering question from the fab rather than accepting any CAM
  edit to sensor electrodes, cutouts, mounting holes, or panel tabs.
