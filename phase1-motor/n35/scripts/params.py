"""BLDC actuator, Phase 1, variant N35: single source of truth for all dimensions (mm, degrees).

Variant N35 (2026-11-26): 20 mm stator stack (20 x 1 mm plates) and one rotor with
28 x 20x5x2 mm N35 blocks (one per pole, magnetised through the 2 mm), aligned with the stack.
Stator plate geometry, 24N28P, 0.7 mm design air gap and winding are the same as variant N52.

Change a value here and re-run `python phase1-motor/n35/scripts/build_all.py`.
Design values only: nothing has been cut or measured.
"""

# --- Stator (24 slots, 1 mm mild steel laser-cut plates) - same plate as n52 ---
SLOTS = 24
STATOR_OD = 80.0
STATOR_BORE = 52.0
YOKE = 3.5
SLOT_DEPTH = 8.2
TOOTH_WIDTH = 4.8
SLOT_OPENING = 2.0
NOTCH_W = 3.0
NOTCH_D = 1.2
NOTCH_TEETH = (1, 13)
PLATE_T = 1.0
STACK_PLATES = 20           # 20 mm stack (n52: 18)

# --- Rotor (28 poles), N35 blocks ---
POLES = 28
AIR_GAP = 0.7               # design gap; flat blocks give 0.63 mm at the block centre
BLOCK_L, BLOCK_W, BLOCK_T = 20.0, 5.0, 2.0   # axial, tangential, radial
BLOCK_GRADE = "N35"
BLOCKS_PER_POLE = 1
ROTOR_OD = 93.4
ROTOR_BORE = 85.4           # magnet bore (flat 2 mm blocks, corners touch the bore)
MAGNET_SEAT_ID = 82.0       # ledge under the magnets: sets their axial position

# --- Winding end turns (assumed, for clearance) ---
END_TURN = 4.0              # axial overhang above and below the stack
END_TURN_R = (29.5, 38.2)   # radial band of the end turns (yoke top .. shoe)
CLEAR = 1.0                 # minimum clearance kept to end turns

STEEL_DENSITY = 7.85e-3     # g/mm^3
NDFEB_DENSITY = 7.5e-3

# --- Derived ---
R_OD = STATOR_OD / 2
R_BORE = STATOR_BORE / 2
R_YOKE = R_BORE + YOKE
R_SHOE = R_YOKE + SLOT_DEPTH
STACK_L = STACK_PLATES * PLATE_T

# --- Actuator v2 axial layout for this variant (z, mm; same origin as phase2-gearbox) ---
# Gearbox, cam and the rotor's cam interface (boss z33..39, floor z34..37) are unchanged.
Z_FLOOR_TOP = 37.0
Z_STACK0 = Z_FLOOR_TOP + CLEAR + END_TURN          # 42: stator bottom (end turns clear the floor by 1 mm)
Z_STACK1 = Z_STACK0 + STACK_L                      # 62
Z_ROTOR_TOP = Z_STACK1                             # rotor wall top = magnet top
Z_BACK_PLATE = Z_STACK1 + END_TURN + CLEAR         # 67: back plate bottom (end turns clear by 1 mm)
BACK_PLATE_T = 5.0
Z_SHAFT_TIP = Z_BACK_PLATE + BACK_PLATE_T + 2.0    # 74
