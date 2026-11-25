# Phase 1: BLDC Motor (v1 motor core CAD)

CAD for the v1 motor of the DIY 9:1, 19 Nm BLDC actuator: a 24N28P outrunner with an 80 mm laminated mild steel stator and a 0.7 mm air gap.

Design record: [ADR 0002 in engineering-assistant](https://github.com/aadhi4200/engineering-assistant/blob/main/decisions/0002-bldc-v1-motor-design.md).
Status: **Phase 1 not started.** These are design files. Nothing has been cut, built or measured.

## Folders

| Folder | Contents |
|---|---|
| `dxf/` | Laser-cut files: DXF R12, `LINE` + `ARC`/`CIRCLE` only, one layer `CUT`, mm, no reference geometry |
| `dxf/backup_flat/` | Same outlines with arcs split into 0.5° straight lines, for viewers that misread arcs |
| `step/` | 3D models: single parts and two motor-core assemblies |
| `fusion360_import/` | Ready-to-import copies for Fusion 360, plus [import steps](fusion360_import/README.md) |
| `previews/` | Top views with the air-gap detail |
| `animation/` | `bldc_v1_rotor_flux_animation.html`: how the teeth's changing magnetism turns the rotor (download and open in a browser) |
| `scripts/` | Generator: every file above is rebuilt from `params.py` |

## Files

| File | What | Qty to make |
|---|---|---|
| `dxf/bldc_v1_stator_plate_24N28P_80mm_ms1mm.dxf` | Stator lamination, 1 mm mild steel | 20 (18 + 2 spare) |
| `dxf/bldc_v1_stator_plate_24N28P_80mm_ms1mm_x20_tabbed_sheet_351x434.dxf` | Optional: all 20 plates nested on one 351 × 434 mm sheet, held by 0.8 mm tabs on teeth 7 and 19. Snap out, file the stubs, true the stack OD (built by `scripts/build_tabbed_sheet.py`) | 1 sheet |
| `dxf/bldc_v1_rotor_ring_final_93.4x87.4x20_ms.dxf` | Final rotor back-iron ring profile | 1 ring (lathe-turned solid, 20 mm long; DXF is the profile reference) |
| `dxf/bldc_v1_rotor_ring_test_93.4x85.4x20_ms.dxf` | Test rotor back-iron ring profile | 1 ring (as above) |
| `step/bldc_v1_stator_plate_24N28P_80mm_ms1mm.step` | One plate | |
| `step/bldc_v1_stator_stack_24N28P_80mm_18mm.step` | 18 mm stack as one solid | |
| `step/bldc_v1_rotor_ring_final_93.4x87.4x20_ms.step` / `..._test_93.4x85.4x20_ms.step` | Rotor rings | |
| `step/bldc_v1_magnet_arc_final_3mm_x28.step` | One final arc magnet (N48SH preferred, N42SH min) | 28 |
| `step/bldc_v1_magnet_block_test_10x5x2_N35_x56.step` | One test block magnet | 56 |
| `step/bldc_v1_motor_core_final_rotor.step` | Stack + final ring + 28 arc magnets (named components) | |
| `step/bldc_v1_motor_core_test_rotor.step` | Stack + test ring + 56 block magnets (named components) | |
| `step/bldc_v1_test_stand_assembly_test_rotor.step` | **Full test stand**: base plate, hub, 2 × 6000ZZ, circlip, shaft, spacer, stator, test rotor, bell | |
| `step/bldc_v1_test_stand_assembly_final_rotor.step` | Same with the final rotor | |
| `step/bldc_v1_test_stand_hub_51.95x30_nylon.step` | Hub: stator seat, key ribs, 2 bearing bores, M4 heat-set insert holes (print in MJF nylon) | 1 |
| `step/bldc_v1_rotor_bell_98.4_nylon.step` | Rotor bell: holds the ring on a bottom lip, M3 set-screw boss (print in nylon) | 1 |
| `step/bldc_v1_test_stand_base_plate_130x130x6.step` | Base plate: shaft clearance hole, 4 × M4 counterbored on 44 PCD, wire hole, 4 × Ø5.5 corner holes | 1 |
| `step/bldc_v1_shaft_10x49.5_steel.step` | Ø10 × 49.5 mm steel shaft with DIN 471 groove and set-screw flat | 1 |
| `step/bldc_v1_spacer_14x10x8.step` | Spacer between the upper bearing inner race and the bell | 1 |
| `step/bldc_v1_bearing_6000ZZ_10x26x8.step`, `step/bldc_v1_circlip_DIN471_10.step` | Bought parts, for reference | 2, 1 |

## Key dimensions (from `scripts/params.py`)

**Frozen for v1 (2026-11-24):** the stator and rotor dimensions below are fixed. Other parts (test stand, housing, gearbox) are designed around them.

| Item | Value |
|---|---|
| Stator | 80 mm OD, 52 mm bore, 3.5 mm yoke, 24 teeth × 4.8 mm, slot depth 8.2 mm, slot opening 2.0 mm, slot area ≈32.8 mm² |
| Alignment notches | 3 × 1.2 mm in the bore under teeth 1 and 13 |
| Stack | 18 × 1 mm, ≈283 g mild steel (calculated) |
| Final rotor | 28 arc magnets, 3 mm thick, 18 mm long, inner R 40.7 mm, 85 % pole arc; ring 93.4 × 87.4 × 20 mm |
| Test rotor | 56 × 10×5×2 mm N35 blocks, 2 per pole axially; ring 93.4 × 85.4 × 20 mm |
| Air gap | 0.70 mm (final arcs); 0.63 mm minimum with the flat test blocks, whose corners touch the ring bore |

## Test stand (section)

![Test stand section](previews/bldc_v1_test_stand_section.png)

| Item | Value |
|---|---|
| Hub | Stator seat Ø51.95 × 18 mm (z 0…18) with 2 key ribs 2.9 × 1.15 mm; shoulder Ø58 × 1.5 (stator rests on it, under the yoke only); neck Ø40; base flange Ø56 × 4; total 30 mm (z −12…18) |
| Bearings | 2 × 6000ZZ in Ø26 bores: upper z 9.5…17.5, lower z −11…−3; Ø20 step between them touches the outer races only. Nylon hub: slip fit + Loctite 638 |
| Hub fixing | 4 × M4 heat-set inserts (Ø5.6 × 6 deep) from below, on 44 mm PCD at 45° |
| Shaft | Ø10 × 49.5 mm (z −13.5…36), DIN 471 circlip under the lower bearing, 0.5 mm flat for the M3 set screw |
| Spacer | 14 × 10 × 8 mm on the upper bearing inner race |
| Bell | Ø98.4, ring pocket Ø93.6, lip Ø88 under the ring, top disc 3.5 mm at z 25.5, boss Ø20 × 7.5 with radial M3 (tap Ø2.5) |
| Base plate | 130 × 130 × 6 (top at z −12): Ø20 centre hole, 4 × M4 counterbored, Ø8 wire hole at x = 33, 4 × Ø5.5 corner holes |
| Clearances (checked by `scripts/check_test_stand.py`) | Magnets–stator 0.63 mm (test) / 0.70 mm (final); bell–winding end turns ≥ 3.5 mm (end turns assumed 4 mm); rotor–base plate 9.5 mm; no overlapping parts |

## Coordinates

mm. Z = motor axis. Origin = centre of the stator stack's bottom face (stack z = 0…18). Tooth 1 on +X, teeth numbered counter-clockwise seen from +Z. Rings and test magnets span z = −1…19, arc magnets z = 0…18. Pole 1 (N) is centred on +X.

## Regenerate

```bash
# Windows PowerShell, WSL2 or Ubuntu (Python 3.10+), from the repo root
pip install -r phase1-motor/scripts/requirements.txt
python phase1-motor/scripts/build_all.py          # motor core, DXF, previews
python phase1-motor/scripts/build_test_stand.py   # test stand parts + assemblies
python phase1-motor/scripts/build_tabbed_sheet.py # optional 20-plate tabbed sheet
```

## Not included yet

Housing and cooling (and the gearbox, which is Phase 2).

## Changes from earlier zips

- Rebuilt from the v1 plan values with a parametric script (the earlier `BLDC_v1_24N28P_files.zip` was not available).
- "Leg" naming removed: the project now targets robot arm joints, so the 87.4 mm ID ring is the **final** rotor ring.
- Test stand redesigned from the plan values: the hub became a 30 mm pedestal (was 19.5 mm) so the winding end turns clear the base plate; spacer 8 mm (was 3.5 mm) so the bell clears the end turns above the stack; shaft 49.5 mm (was 39 mm).
- All files use one scheme: `bldc_v1_<part>_<key dims>_<material>`.
