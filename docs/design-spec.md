# Revision A design specification

Status: draft, defaults accepted on 2026-08-08.

## Product definition

Revision A is a wired, split, 34-key electrocapacitive keyboard. Its physical
layout follows the Ferris Sweep family. Its sensing cell and analog front end
are based on the manufactured Tako Rev1 design and cross-checked against
Cipulot's current QMK EC implementations.

The term "Sweep-style" describes the key arrangement and silhouette. It does
not imply Choc spacing, a reversible PCB, a Pro Micro footprint, or a diode
switch matrix.

## Layout

- Two halves, 17 keys per half.
- Main matrix per half: 3 rows x 5 columns.
- Thumb cluster per half: 2 keys.
- Logical EC matrix per half: 4 rows x 5 columns, with three unused cells.
- Nominal center-to-center pitch: 19.05 mm unless physical EC parts require a
  different measured value.
- Separate left and right PCB outlines; no reversible sensor PCB.

## Electrical architecture

- One socketable, Pro-Micro-pin-compatible RP2040 module per half. AVR Pro
  Micros are electrically pin-compatible but are explicitly unsupported.
- One local EC analog front end per half.
- One 74HC4051 analog multiplexer and one OPA350 peak-hold stage per half.
- USB connection through the replaceable controller module on both halves.
- Reset, power, ADC, mux, row-drive, and split-transport test pads.
- QMK-supported RP2040 serial transport between halves.
- PJ-320A TRRS carries serial, 3.3 V, and ground as in the proven reference.
  It is not hot-plug safe; connect or disconnect it only with USB removed.

## Mechanical architecture

- Topre-compatible plate-mounted housings with conical springs and individual
  domes. NiZ compatibility is explicitly out of scope for Revision A.
- One Topre/OEM plate variant at 1.2 mm nominal thickness, matching the proven
  reference stack. Preserve its cutouts and housing orientation until measured
  parts justify a change.
- PCB, plate, and case must form a controlled compression stack; a bare PCB is
  not considered a functional keyboard assembly.
- Final plate cutouts and stack heights require measurements or authoritative
  drawings for the selected physical parts.

## Explicit non-goals for Revision A

- Wireless or batteries.
- Per-key or underglow lighting.
- Displays, encoders, pointing devices, or haptics.
- Hot-swap mechanical switches.
- Vial dynamic configuration before basic QMK sensing is stable.
- Commercial distribution.
- NiZ housings, sliders, domes, or plate compatibility.

The inherited display, battery-contact, and battery-switch footprints remain
in the frozen known-built geometry but are explicitly marked DNP. They are not
part of the Revision A BOM or firmware feature set.

## Change-control rule

The following proven EC elements may not be changed without an explicit design
decision and new verification evidence:

- sensor electrode geometry;
- copper and soldermask exclusions around the sensor;
- analog peak-hold and discharge topology;
- analog component values and device types;
- row excitation polarity and timing;
- ADC reference/supply arrangement;
- QMK raw-sample and calibration sequence;
- relevant PCB layer construction beneath the sensor.
