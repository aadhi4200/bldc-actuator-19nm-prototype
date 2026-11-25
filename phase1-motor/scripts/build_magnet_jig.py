"""Removable gluing jig for the N35 test rotor (56 x 10x5x2 blocks, 2 per pole, 28 poles).

The test ring sits on the jig's base, centred by an outer lip. 28 fingers rise inside the ring and leave
one pocket per pole, so neighbouring magnets cannot snap together while the epoxy cures. N / S marks on the
base show which way each pocket's inner face must point. After curing, push the jig out axially.

Usage (from the repo root): python phase1-motor/scripts/build_magnet_jig.py
Coordinates match the other parts: ring z = -1..19, magnets z = -1..19.
"""
import math

import cadquery as cq

import params as P
from build_all import block_offset
from paths import step, to_f360
NAME = "bldc_v1_magnet_jig_test_rotor_28pocket_print"

RING_Z0 = (P.STACK_L - P.RING_LENGTH) / 2          # -1
RING_IR = P.TEST_RING_ID / 2                        # 42.7
FINGER_RO = RING_IR - 0.15                          # clears the ring bore so the jig slides out
FINGER_RI = block_offset() - 0.05 - 0.6             # 0.6 mm wall inside the magnets' inner face
POCKET_W = P.BLOCK_W + 0.2                          # 5.2 mm: 0.1 mm per side for print tolerance
FINGER_H = P.BLOCKS_PER_POLE * P.BLOCK_L - 1.0      # 19 mm: stops 1 mm short of the ring top
BASE_T, BASE_RI, BASE_RO = 3.0, 30.0, 52.0
LIP_IR, LIP_H = P.ROTOR_RING_OD / 2 + 0.15, 5.0     # centres the ring on its OD
MARK_R, MARK_H, MARK_SIZE = 36.5, 0.6, 3.2


def jig():
    zb = RING_Z0 - BASE_T
    base = cq.Workplane().workplane(offset=zb).circle(BASE_RO).circle(BASE_RI).extrude(BASE_T)
    lip = (cq.Workplane().workplane(offset=RING_Z0).circle(BASE_RO).circle(LIP_IR).extrude(LIP_H))
    fingers = cq.Workplane().workplane(offset=RING_Z0).circle(FINGER_RO).circle(FINGER_RI).extrude(FINGER_H)
    pitch = 360 / P.POLES
    for k in range(P.POLES):
        pocket = (cq.Workplane().workplane(offset=RING_Z0 - 0.01)
                  .center(block_offset() + 1.0, 0).rect(6.0, POCKET_W).extrude(FINGER_H + 1)
                  .rotate((0, 0, 0), (0, 0, 1), k * pitch))
        fingers = fingers.cut(pocket)
    # pockets cut right through: only fingers remain between poles, magnets sit on the ring bore
    body = base.union(lip).union(fingers)
    for k in range(P.POLES):
        a = math.radians(k * pitch)
        txt = (cq.Workplane().workplane(offset=RING_Z0)
               .text("N" if k % 2 == 0 else "S", MARK_SIZE, MARK_H, halign="center", valign="center")
               .rotate((0, 0, 0), (0, 0, 1), k * pitch - 90)
               .translate((MARK_R * math.cos(a), MARK_R * math.sin(a), 0)))
        body = body.union(txt)
    return body


def main():
    j = jig()
    cq.exporters.export(j, str(step("print", NAME)))
    to_f360(step("print", NAME), "print")
    print(f"{NAME}.step  finger r {FINGER_RI:.2f}..{FINGER_RO:.2f}, pocket {POCKET_W} mm, "
          f"finger height {FINGER_H} mm")
    return j


if __name__ == "__main__":
    main()
