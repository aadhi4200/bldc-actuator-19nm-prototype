# Actuator v2: importing into Fusion 360

All files in **mm**, copies of `../step/`. Units: mm. Z = actuator axis; the output face is at the bottom (z = −5 … 0), the back cover at the top (≈ z 77).

| Folder / file | What | Make | Material |
|---|---|---|---|
| `1_assemblies/act_v2_assembly_flipped_motor_cycloidal.step` | **Start here.** Complete actuator v2: cycloidal gearbox + flipped motor, 27 bodies, Ø106 × 82 mm. View only | — | — |
| `2_machined_parts/act_v2_01_housing_pin_ring.step` | Housing with the 10 ring-pin pockets (bore Ø69) | 1 | Al 6061-T6 |
| `2_machined_parts/act_v2_02_cycloid_disc_x2.step` | Cycloid disc, 9 lobes, 7 mm | **2** | Al 7075-T6 |
| `2_machined_parts/act_v2_03_output_flange.step` | Output flange, Ø64, 6 × M5 on Ø50 | 1 | Al 6061-T6 |
| `2_machined_parts/act_v2_04_bearing_retainer.step` | Bearing retainer, 1.5 mm | 1 | Al 6061-T6 |
| `2_machined_parts/act_v2_05_eccentric_cam_v2.step` | Eccentric cam with the Ø38 rotor flange | 1 | Al 7075-T6 |
| `2_machined_parts/act_v2_06_motor_can.step` | Motor can, Ø106 | 1 | Al 6061-T6 |
| `2_machined_parts/act_v2_07_rotor_one_piece_steel.step` | **Final rotor**, one piece: cup + hub + Ø10 shaft, Ø87.4 magnet bore | 1 | EN8 / C45 steel |
| `2_machined_parts/act_v2_07b_rotor_one_piece_TEST_85.4bore.step` | **Test rotor**, same with Ø85.4 bore for 28 × 20×5×2 N35 blocks | 1 | EN8 / C45 steel |
| `2_machined_parts/act_v2_10_stator_hub.step` | Stator hub, Ø51.9 seat, bores for 2 × 6000 | 1 | Al 6061-T6 |
| `2_machined_parts/act_v2_11_back_plate.step` | Back plate (stator hub, encoder PCB) | 1 | Al 6061-T6 |
| `2_machined_parts/act_v2_12_back_cover.step` | Back cover | 1 | Al 6061-T6 |

Bought: bearings 6812, 2 × 6804, 6800, 2 × 6000; 10 × Ø6 × 16 dowel pins; 6 × Ø5 × 25 dowel pins; Ø6 × 2.5 diametric encoder magnet; screws per [../README.md](../README.md).

**Fits:** send every machined part with its page of [`../drawings/act_v2_drawings.pdf`](../drawings/act_v2_drawings.pdf). The STEP files are nominal sizes; the drawings carry the bearing and pin fits (J7 / N7 / k6 / H7).

## Import

1. **File → Open → Open from my computer…**, pick the `.step` file, wait for the Data Panel to finish translating.
2. Open the design. The assembly's bodies appear as components in the Browser.
3. To combine with the Phase 1 stator: open the assembly, then right-click a Phase 1 file in the Data Panel → **Insert into current design** (both use mm; check the Z position of the stator, which sits at z 40 … 58 in v2).

If the model lies on its side, set **Z up** under Preferences → General → Default modeling orientation, or rotate the component.
