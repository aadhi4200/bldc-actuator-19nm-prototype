# Variant N35: importing into Fusion 360

All files in **mm**, copies of `../step/`. Z = actuator axis; output face at the bottom (z −5 … 0), back cover at the top (z 83.5).

| File | What | Make | Material |
|---|---|---|---|
| `1_assemblies/act_n35_assembly_flipped_motor_cycloidal_20mm_N35.step` | **Start here.** Full actuator: N35 motor (20 mm stack) + unchanged cycloidal gearbox, Ø106 × 88.5 mm. View only | — | — |
| `1_assemblies/act_n35_motor_assembly_20mm_N35.step` | Motor only, for the bench test | — | — |
| `2_machined_parts/act_n35_07_rotor_one_piece_steel_85.4bore_20mm.step` | Rotor: cup + boss + Ø10 shaft, Ø85.4 × 20 magnet bore, Ø82 seat ledge | 1 | EN8 / C45 steel |
| `2_machined_parts/act_n35_10_stator_hub_20mm.step` | Stator hub: Ø51.9 seat, Ø56 stator stop, bores for 2 × 6000 | 1 | Al 6061-T6 |
| `2_machined_parts/act_n35_06_motor_can_20mm.step` | Motor can, wall to z 67 | 1 | Al 6061-T6 |
| `2_machined_parts/act_n35_11_back_plate.step` | Back plate (same as v2 part 11, z 67 … 72) | 1 | Al 6061-T6 |
| `2_machined_parts/act_n35_12_back_cover.step` | Back cover (same as v2 part 12, z 72 … 83.5) | 1 | Al 6061-T6 or print |
| `3_sketches/bldc_v1_stator_plate_24N28P_80mm_ms1mm_sketch.dxf` | Stator plate outline (same as N52) | — | — |

Gearbox parts 01–05 are unchanged: use `phase2-gearbox/fusion360_import/2_machined_parts/`.

## Import

1. **File → Open → Open from my computer…**, pick the `.step` file, wait for the Data Panel to translate it.
2. Open the design. Each body appears as a named component (magnets `magnet_P01_N` … `magnet_P28_S`).
3. If the model lies on its side, set **Z up** under Preferences → General → Default modeling orientation.
