# Importing into Fusion 360

Only the files you open or print. All in **mm**, copies of the files in `../step` and `../dxf`; `../scripts/build_all.py` regenerates this folder too. Everything else (single parts, motor core only, bought parts) is in `../step/`.

| Folder / file | Use in Fusion |
|---|---|
| `1_assemblies/bldc_v1_test_stand_assembly_test_rotor.step` | **Start here.** Complete test stand with the N35 test rotor: base plate, hub, 2 × 6000ZZ, circlip, shaft, spacer, stator stack, rotor ring, 56 magnets, bell, each a named component |
| `1_assemblies/bldc_v1_test_stand_assembly_final_rotor.step` | Same with the final rotor (28 arc magnets) |
| `2_print_parts/bldc_v1_test_stand_hub_51.95x30_nylon.step` | Hub, for printing (MJF nylon) |
| `2_print_parts/bldc_v1_rotor_bell_98.4_nylon.step` | Rotor bell, for printing (nylon) |
| `2_print_parts/bldc_v1_magnet_jig_test_rotor_28pocket_print.step` | Magnet gluing jig, for printing (PLA or PETG) |
| `3_sketches/bldc_v1_stator_plate_24N28P_80mm_ms1mm_sketch.dxf` | Stator outline to insert as an editable sketch |

## STEP (assemblies or parts)

1. **File → Open → Open from my computer…**, pick the `.step` file. Fusion uploads and translates it (wait for the Data Panel to finish).
2. Open the translated design. Each part appears as a component in the Browser (`hub`, `shaft`, `stator_stack`, `rotor_bell`, `magnet_P01_N`, …).
3. To use it inside another design: right-click it in the Data Panel → **Insert into current design**.

Alternative: drag the file into the **Data Panel** → **Upload**.

## DXF (as a sketch)

1. **Insert → Insert DXF**.
2. **Plane/sketch:** XY plane. **Units: Millimeter** (R12 DXF carries no units, so set this by hand).
3. Leave **Single sketch** on and **Position** at the origin, so tooth 1 stays on +X.
4. Click **OK**, then **Extrude** the profile 1 mm (one plate) or 18 mm (stack).

## Orientation

Z = motor axis, origin at the centre of the stator stack's bottom face, tooth 1 on +X. Fusion's default is Y-up: if the model lies on its side, set **Z up** under Preferences → General → Default modeling orientation before importing, or rotate the component.

## Replacing an older import

If you imported earlier versions (from the old flat `step/` or `fusion360_import/` folders), delete them in Fusion and import these. The geometry of the stator, rotor and magnets is unchanged (frozen); the test stand parts are the current design.
