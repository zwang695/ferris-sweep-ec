# Production outputs

Do not fabricate files merely because they appear here. A manufacturing package
is releasable only after all gates in `docs/verification-plan.md` pass and its
directory is explicitly marked as a prototype release.

`fabrication-notes.md` records the intended order quantities, thicknesses, and
the CAM features that must not be automatically altered.

`jlcpcb/` contains the reviewed wired-only part map and exact order procedure.
Run `scripts/generate-jlcpcb` for upload-ready controller PCBA and plate ZIPs.
