"""Phase 1 motor test stand: hub, 2 x 6000ZZ, shaft, spacer, rotor bell, circlip, base plate,
plus full assemblies with the test and final rotors.

Usage (from the repo root):  python phase1-motor/n52/scripts/build_test_stand.py
Coordinates match build_all.py: mm, Z = motor axis, origin = centre of the stator stack's bottom face.
"""
import cadquery as cq

import params as P
from build_all import (NAMES, stator_solid, ring, arc_magnet, block_magnet, block_offset)
from paths import step, to_f360

# ---------------------------------------------------------------- test stand parameters
BRG_ID, BRG_OD, BRG_W = 10.0, 26.0, 8.0        # 6000ZZ
SHAFT_D = 10.0
HUB_SEAT_D = 51.95                              # slip fit in the 52.0 stator bore
RIB_W, RIB_H = 2.9, 1.15                        # key ribs into the 3.0 x 1.2 bore notches
HUB_TOP = P.STACK_L                             # z = 18
SHOULDER_D, SHOULDER_T = 58.0, 1.5              # stator rests on this (under the yoke only)
NECK_D = 40.0
FLANGE_D, FLANGE_T = 56.0, 4.0
HUB_BOTTOM = -12.0                              # pedestal keeps winding end turns clear of the base
BORE_STEP_D = 20.0                              # shoulder between bearings: touches outer races only
UPPER_BRG_TOP = HUB_TOP - 0.5
LOWER_BRG_BOT = HUB_BOTTOM + 1.0
M4_PCD, M4_INSERT_D, M4_INSERT_DEPTH = 44.0, 5.6, 6.0   # heat-set inserts from below
SPACER_OD, SPACER_ID, SPACER_T = 14.0, 10.0, 8.0   # 8 mm keeps the bell 7.5 mm above the stack (end-turn clearance)
BELL_OD, BELL_SKIRT_ID, BELL_LIP_ID = 98.4, 93.6, 88.0
BELL_LIP_T, BELL_DISC_T = 1.5, 3.5
BOSS_D, BOSS_H = 20.0, 7.5
BASE_W, BASE_T = 130.0, 6.0
BASE_HOLE_D = 20.0
LEAD_HOLE_D, LEAD_HOLE_R = 8.0, 33.0
CORNER_HOLE_D, CORNER_HOLE_OFF = 5.5, 55.0

RING_Z0 = (P.STACK_L - P.RING_LENGTH) / 2       # -1
RING_TOP = RING_Z0 + P.RING_LENGTH              # 19
SPACER_Z0 = UPPER_BRG_TOP
BELL_DISC_Z0 = SPACER_Z0 + SPACER_T             # bell sits on the spacer
BELL_LIP_Z0 = RING_Z0 - BELL_LIP_T
SHAFT_TOP = BELL_DISC_Z0 + BELL_DISC_T + BOSS_H - 0.5
CIRCLIP_T = 1.0
SHAFT_BOT = LOWER_BRG_BOT - CIRCLIP_T - 1.5


def cyl(d, z0, h):
    return cq.Workplane().workplane(offset=z0).circle(d / 2).extrude(h)


def hub():
    h = cyl(HUB_SEAT_D, 0, HUB_TOP)
    for ang in (0, 180):  # key ribs under teeth 1 and 13
        rib = (cq.Workplane().workplane(offset=0)
               .center(HUB_SEAT_D / 2 + RIB_H / 2 - 0.2, 0).rect(RIB_H + 0.4, RIB_W).extrude(HUB_TOP)
               .rotate((0, 0, 0), (0, 0, 1), ang))
        h = h.union(rib)
    h = h.union(cyl(SHOULDER_D, -SHOULDER_T, SHOULDER_T))
    h = h.union(cyl(NECK_D, HUB_BOTTOM + FLANGE_T, -SHOULDER_T - (HUB_BOTTOM + FLANGE_T)))
    h = h.union(cyl(FLANGE_D, HUB_BOTTOM, FLANGE_T))
    # bores: upper bearing, lower bearing, step between them
    h = h.cut(cyl(BRG_OD, UPPER_BRG_TOP - BRG_W, HUB_TOP - (UPPER_BRG_TOP - BRG_W) + 1))
    h = h.cut(cyl(BRG_OD, HUB_BOTTOM - 1, LOWER_BRG_BOT + BRG_W - HUB_BOTTOM + 1))
    h = h.cut(cyl(BORE_STEP_D, HUB_BOTTOM, HUB_TOP - HUB_BOTTOM))
    # heat-set insert holes for 4 x M4 from the base plate, at 45 deg so they miss the ribs
    pts = [(M4_PCD / 2 * c, M4_PCD / 2 * s) for c, s in ((0.7071, 0.7071), (-0.7071, 0.7071),
                                                          (-0.7071, -0.7071), (0.7071, -0.7071))]
    h = h.cut(cq.Workplane().workplane(offset=HUB_BOTTOM).pushPoints(pts)
              .circle(M4_INSERT_D / 2).extrude(M4_INSERT_DEPTH))
    return h


def bearing(z0):
    outer = cyl(BRG_OD, z0, BRG_W).cut(cyl(BRG_OD - 4.5, z0, BRG_W))
    inner = cyl(BRG_ID + 4.5, z0, BRG_W).cut(cyl(BRG_ID, z0, BRG_W))
    shield = cyl(BRG_OD - 4.5, z0 + 0.3, BRG_W - 0.6).cut(cyl(BRG_ID + 4.5, z0, BRG_W))
    return outer.union(inner).union(shield)


def shaft():
    s = cyl(SHAFT_D, SHAFT_BOT, SHAFT_TOP - SHAFT_BOT)
    groove_z = LOWER_BRG_BOT - CIRCLIP_T
    s = s.cut(cyl(SHAFT_D, groove_z, CIRCLIP_T).cut(cyl(9.4, groove_z, CIRCLIP_T)))  # DIN 471 groove
    flat_z0 = BELL_DISC_Z0 + BELL_DISC_T
    s = s.cut(cq.Workplane().workplane(offset=flat_z0).center(SHAFT_D / 2, 0)
              .rect(1.0, SHAFT_D).extrude(BOSS_H))  # 0.5 mm flat for the set screw
    return s


def circlip():
    z = LOWER_BRG_BOT - CIRCLIP_T
    return cyl(15.0, z, CIRCLIP_T).cut(cyl(9.4, z, CIRCLIP_T))


def spacer():
    return cyl(SPACER_OD, SPACER_Z0, SPACER_T).cut(cyl(SPACER_ID, SPACER_Z0, SPACER_T))


def bell():
    top = BELL_DISC_Z0 + BELL_DISC_T
    b = cyl(BELL_OD, BELL_LIP_Z0, top - BELL_LIP_Z0)
    b = b.cut(cyl(BELL_SKIRT_ID, RING_Z0, BELL_DISC_Z0 - RING_Z0))      # pocket for the ring
    b = b.cut(cyl(BELL_LIP_ID, BELL_LIP_Z0, BELL_LIP_T))                 # lip the ring sits on
    b = b.union(cyl(BOSS_D, top, BOSS_H))
    b = b.cut(cyl(SHAFT_D, BELL_DISC_Z0, BELL_DISC_T + BOSS_H))
    # M3 set screw, tapping hole 2.5 mm, radial in the boss on +X (onto the shaft flat)
    b = b.cut(cq.Workplane("YZ").workplane(offset=0).center(0, top + BOSS_H / 2)
              .circle(1.25).extrude(BOSS_D))
    return b


def base_plate():
    z0 = HUB_BOTTOM - BASE_T
    p = cq.Workplane().workplane(offset=z0).rect(BASE_W, BASE_W).extrude(BASE_T)
    p = p.cut(cyl(BASE_HOLE_D, z0, BASE_T))
    pts = [(M4_PCD / 2 * c, M4_PCD / 2 * s) for c, s in ((0.7071, 0.7071), (-0.7071, 0.7071),
                                                          (-0.7071, -0.7071), (0.7071, -0.7071))]
    p = p.cut(cq.Workplane().workplane(offset=z0).pushPoints(pts).circle(2.25).extrude(BASE_T))
    p = p.cut(cq.Workplane().workplane(offset=z0).pushPoints(pts).circle(4.0).extrude(3.0))  # cbore
    p = p.cut(cq.Workplane().workplane(offset=z0).center(LEAD_HOLE_R, 0)
              .circle(LEAD_HOLE_D / 2).extrude(BASE_T))
    o = CORNER_HOLE_OFF
    p = p.cut(cq.Workplane().workplane(offset=z0)
              .pushPoints([(o, o), (-o, o), (-o, -o), (o, -o)]).circle(CORNER_HOLE_D / 2).extrude(BASE_T))
    return p


PART_NAMES = {
    "hub": "bldc_v1_test_stand_hub_51.95x30_nylon",
    "bearing": "bldc_v1_bearing_6000ZZ_10x26x8",
    "shaft": f"bldc_v1_shaft_10x{0:.0f}_steel",
    "spacer": "bldc_v1_spacer_14x10x8",
    "bell": "bldc_v1_rotor_bell_98.4_nylon",
    "circlip": "bldc_v1_circlip_DIN471_10",
    "base": "bldc_v1_test_stand_base_plate_130x130x6",
    "asm_test": "bldc_v1_test_stand_assembly_test_rotor",
    "asm_final": "bldc_v1_test_stand_assembly_final_rotor",
}


def main():
    shaft_len = SHAFT_TOP - SHAFT_BOT
    PART_NAMES["shaft"] = f"bldc_v1_shaft_10x{shaft_len:.1f}_steel"
    parts = {"hub": hub(), "shaft": shaft(), "spacer": spacer(), "bell": bell(),
             "circlip": circlip(), "base": base_plate()}
    brg_up = bearing(UPPER_BRG_TOP - BRG_W)
    brg_lo = bearing(LOWER_BRG_BOT)
    where = {"hub": "print", "bell": "print", "shaft": "machined", "spacer": "machined",
             "base": "machined", "circlip": "bought"}
    for k, v in parts.items():
        cq.exporters.export(v, str(step(where[k], PART_NAMES[k])))
    cq.exporters.export(brg_up, str(step("bought", PART_NAMES["bearing"])))

    stack = stator_solid(P.STACK_L)
    ring_f = ring(P.ROTOR_RING_OD, P.FINAL_RING_ID, P.RING_LENGTH, RING_Z0)
    ring_t = ring(P.ROTOR_RING_OD, P.TEST_RING_ID, P.RING_LENGTH, RING_Z0)
    pitch = 360 / P.POLES
    arcs = [arc_magnet(k * pitch, (P.STACK_L - P.ARC_MAG_L) / 2) for k in range(P.POLES)]
    blk_z0 = (P.STACK_L - P.BLOCKS_PER_POLE * P.BLOCK_L) / 2
    blocks = [block_magnet(k * pitch, blk_z0 + j * P.BLOCK_L)
              for k in range(P.POLES) for j in range(P.BLOCKS_PER_POLE)]

    steel, nylon, alu = cq.Color(0.55, 0.55, 0.6), cq.Color(0.92, 0.92, 0.88), cq.Color(0.75, 0.75, 0.78)
    red, blue = cq.Color(0.85, 0.15, 0.15), cq.Color(0.15, 0.3, 0.85)
    for key, rng, mags, per in (("asm_test", ring_t, blocks, P.BLOCKS_PER_POLE), ("asm_final", ring_f, arcs, 1)):
        a = cq.Assembly(name=PART_NAMES[key])
        a.add(parts["base"], name="base_plate", color=alu)
        a.add(parts["hub"], name="hub", color=nylon)
        a.add(brg_lo, name="bearing_lower_6000ZZ", color=steel)
        a.add(brg_up, name="bearing_upper_6000ZZ", color=steel)
        a.add(parts["circlip"], name="circlip_DIN471", color=cq.Color(0.2, 0.2, 0.2))
        a.add(parts["shaft"], name="shaft", color=steel)
        a.add(parts["spacer"], name="spacer", color=steel)
        a.add(stack, name="stator_stack", color=steel)
        a.add(rng, name="rotor_ring", color=cq.Color(0.35, 0.35, 0.38))
        a.add(parts["bell"], name="rotor_bell", color=nylon)
        for idx, m in enumerate(mags):
            pole = idx // per
            nm = f"magnet_P{pole + 1:02d}_{'N' if pole % 2 == 0 else 'S'}" + ("" if per == 1 else f"_{idx % per + 1}")
            a.add(m, name=nm, color=red if pole % 2 == 0 else blue)
        a.export(str(step("assemblies", PART_NAMES[key])))
        to_f360(step("assemblies", PART_NAMES[key]), "assemblies")
    to_f360(step("print", PART_NAMES["hub"]), "print")
    to_f360(step("print", PART_NAMES["bell"]), "print")

    print(f"shaft length {shaft_len:.1f} mm (z {SHAFT_BOT:.1f} .. {SHAFT_TOP:.1f})")
    print(f"hub height {HUB_TOP - HUB_BOTTOM:.1f} mm, base plate top at z {HUB_BOTTOM:.1f}")
    print(f"rotor bottom z {BELL_LIP_Z0:.1f}: {BELL_LIP_Z0 - HUB_BOTTOM:.1f} mm above the base plate")
    return parts, brg_up, brg_lo, stack, ring_t, blocks


if __name__ == "__main__":
    main()
