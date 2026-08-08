# Mechanical

This directory will contain canonical key coordinates, PCB outline sources,
the Topre/OEM plate, and stack drawings. Sweep geometry is a layout input; EC
housing cutouts and compression dimensions come from the proven reference and
selected Topre-compatible physical parts.

Revision A uses a 1.2 mm nominal plate. NiZ compatibility and its separate
plate stack are out of scope.

The active plate is in `topre-plate/`. One plate file represents one half;
fabrication requires two copies, with one flipped for the opposite hand. Its
housing cutouts, mounting holes, and key coordinates are retained from the
known-built Tako Rev1 Topre/OEM plate.

The matching lower enclosure PCB is in `bottom-plate/`. It is likewise a
single-half file to be fabricated twice. Its controller, display, TRRS, and
mounting cutouts follow the same pinned Tako Rev1 mechanical stack.
