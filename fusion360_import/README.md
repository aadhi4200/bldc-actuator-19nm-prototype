# Importing into Fusion 360

All files are in **mm**. They are copies of the files in `../step` and `../dxf`; regenerate with `scripts/build_all.py`, which refreshes this folder too.

| File | Use in Fusion |
|---|---|
| `bldc_v1_motor_core_final_rotor.step` | Full motor core with the final rotor: stator stack, ring and 28 magnets as separate components |
| `bldc_v1_motor_core_test_rotor.step` | Same with the test rotor (56 block magnets) |
| `bldc_v1_stator_plate_24N28P_80mm_ms1mm.step` | One lamination as a body |
| `bldc_v1_stator_plate_24N28P_80mm_ms1mm_sketch.dxf` | Stator outline to insert as an editable sketch |

## STEP (assemblies or parts)

1. **File → Open → Open from my computer…**, pick the `.step` file. Fusion uploads and translates it (wait for the Data Panel to finish).
2. Open the translated design. Each part appears as a component in the Browser (`stator_stack`, `rotor_ring`, `magnet_P01_N`, …).
3. To use it inside another design: **Insert → Insert into current design** from the Data Panel, or right-click the design → **Insert into current design**.

Alternative: drag the file into the **Data Panel** → **Upload**.

## DXF (as a sketch)

1. **Insert → Insert DXF**.
2. **Plane/sketch:** XY plane. **Units: Millimeter** (R12 DXF carries no units, so set this by hand).
3. Leave **Single sketch** on and **Position** at the origin, so tooth 1 stays on +X.
4. Click **OK**, then **Extrude** the profile 1 mm (one plate) or 18 mm (stack).

## Orientation

Z = motor axis, origin at the centre of the stack's bottom face, tooth 1 on +X. Fusion's default is Y-up: if the motor lies on its side, pick **Z up** under Preferences → General → Default modeling orientation before importing, or rotate the component.
