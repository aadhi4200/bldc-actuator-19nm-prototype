"""BLDC actuator v1 motor core: single source of truth for all dimensions (mm, degrees).

Change a value here and re-run `python scripts/build_all.py` to regenerate every DXF and STEP file.
Values come from the v1 plan (24N28P outrunner, 0.7 mm air gap). They are design values, not measured parts.
"""

# FROZEN (2026-11-24): stator and rotor dimensions below are fixed by the owner for v1
# (80 mm stator OD, 52 mm bore, tooth/slot geometry, 0.7 mm air gap, rotor rings and magnets).
# Do not change them; test-stand and gearbox parts must fit around them.

# --- Stator (24 slots, 1 mm mild steel laser-cut plates) ---
SLOTS = 24
STATOR_OD = 80.0
STATOR_BORE = 52.0
YOKE = 3.5                  # radial yoke thickness above the bore
SLOT_DEPTH = 8.2            # yoke top -> underside of tooth shoe
TOOTH_WIDTH = 4.8           # parallel-sided tooth body
SLOT_OPENING = 2.0          # parallel-sided opening between tooth shoes
NOTCH_W = 3.0               # bore alignment notches (under teeth 1 and 13)
NOTCH_D = 1.2
NOTCH_TEETH = (1, 13)
PLATE_T = 1.0
STACK_PLATES = 18           # 18 mm stack

# --- Rotor (28 poles) ---
POLES = 28
AIR_GAP = 0.7
ROTOR_RING_OD = 93.4
RING_LENGTH = 20.0          # solid lathe-turned mild steel ring

# Final rotor: 28 arc magnets, N48SH preferred (N42SH minimum)
ARC_MAG_T = 3.0
ARC_MAG_L = 18.0
ARC_POLE_ARC = 0.85         # fraction of pole pitch
FINAL_RING_ID = 87.4

# Test rotor: 56 x 10x5x2 mm N35 blocks (2 per pole axially), bench only
BLOCK_L, BLOCK_W, BLOCK_T = 10.0, 5.0, 2.0   # axial, tangential, radial
BLOCKS_PER_POLE = 2
TEST_RING_ID = 85.4

STEEL_DENSITY = 7.85e-3     # g/mm^3 (mild steel)

# --- Derived ---
R_OD = STATOR_OD / 2
R_BORE = STATOR_BORE / 2
R_YOKE = R_BORE + YOKE
R_SHOE = R_YOKE + SLOT_DEPTH
STACK_L = STACK_PLATES * PLATE_T
R_MAG_IN = R_OD + AIR_GAP
