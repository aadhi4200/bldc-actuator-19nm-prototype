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

## Key dimensions (from `scripts/params.py`)

| Item | Value |
|---|---|
| Stator | 80 mm OD, 52 mm bore, 3.5 mm yoke, 24 teeth × 4.8 mm, slot depth 8.2 mm, slot opening 2.0 mm, slot area ≈32.8 mm² |
| Alignment notches | 3 × 1.2 mm in the bore under teeth 1 and 13 |
| Stack | 18 × 1 mm, ≈283 g mild steel (calculated) |
| Final rotor | 28 arc magnets, 3 mm thick, 18 mm long, inner R 40.7 mm, 85 % pole arc; ring 93.4 × 87.4 × 20 mm |
| Test rotor | 56 × 10×5×2 mm N35 blocks, 2 per pole axially; ring 93.4 × 85.4 × 20 mm |
| Air gap | 0.70 mm (final arcs); 0.63 mm minimum with the flat test blocks, whose corners touch the ring bore |

## Coordinates

mm. Z = motor axis. Origin = centre of the stator stack's bottom face (stack z = 0…18). Tooth 1 on +X, teeth numbered counter-clockwise seen from +Z. Rings and test magnets span z = −1…19, arc magnets z = 0…18. Pole 1 (N) is centred on +X.

## Regenerate

```bash
# Windows PowerShell, WSL2 or Ubuntu (Python 3.10+), from the repo root
pip install -r phase1-motor/scripts/requirements.txt
python phase1-motor/scripts/build_all.py
```

## Not included yet

Test stand parts (hub, base plate, shaft, spacer, rotor bell), the gearbox and the housing.

## Changes from earlier zips

- Rebuilt from the v1 plan values with a parametric script (the earlier `BLDC_v1_24N28P_files.zip` was not available).
- "Leg" naming removed: the project now targets robot arm joints, so the 87.4 mm ID ring is the **final** rotor ring.
- All files use one scheme: `bldc_v1_<part>_<key dims>_<material>`.
