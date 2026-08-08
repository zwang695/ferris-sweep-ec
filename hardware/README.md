# Hardware

`rev-a/` contains the active KiCad 10 design. It starts as a mechanically
imported, renamed copy of the pinned MIT-licensed Tako Rev1 source. The import
is reproducible with `scripts/import-tako-rev1`; subsequent changes are made in
the active source and reviewed against the imported baseline.

The upstream project commit and all other references are pinned in
`references/reference-audit.md`. The original MIT text is retained as
`hardware/LICENSE.tako.MIT`.

The project-level ERC, DRC, firmware, and mechanical gates in
`docs/verification-plan.md` now pass. Revision A is suitable for an informed
prototype review; physical Topre signal margin remains unproven until a real
dome, spring, housing, and fabricated sensor stack are measured.
