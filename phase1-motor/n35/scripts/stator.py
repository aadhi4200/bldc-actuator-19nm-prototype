"""Stator plate profile (same 24-slot plate as variant n52) and DXF writer.

Coordinates: mm, Z = motor axis, tooth 1 on +X, teeth numbered counter-clockwise seen from +Z.
"""
import math

import cadquery as cq
import ezdxf

import params as P


def pol(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


def asind(x):
    return math.degrees(math.asin(x))


# ---------------------------------------------------------------- stator profile
# Segments: ("L", p1, p2) or ("A", r, a1, a2) = CCW arc about the origin from a1 to a2 (degrees).
def stator_outer():
    pitch = 360 / P.SLOTS
    hw, ho = P.TOOTH_WIDTH / 2, P.SLOT_OPENING / 2
    segs = []
    for i in range(P.SLOTS):
        t = i * pitch                      # tooth (i+1) centre
        s = t + pitch / 2                  # slot centre after it
        n = t + pitch                      # next tooth centre
        a_tip0 = t - pitch / 2 + asind(ho / P.R_OD)
        a_tip1 = s - asind(ho / P.R_OD)
        segs.append(("A", P.R_OD, a_tip0, a_tip1))                                  # tooth tip
        segs.append(("L", pol(P.R_OD, a_tip1), pol(P.R_SHOE, s - asind(ho / P.R_SHOE))))  # opening side
        segs.append(("A", P.R_SHOE, t + asind(hw / P.R_SHOE), s - asind(ho / P.R_SHOE)))  # shoe underside
        segs.append(("L", pol(P.R_SHOE, t + asind(hw / P.R_SHOE)), pol(P.R_YOKE, t + asind(hw / P.R_YOKE))))
        segs.append(("A", P.R_YOKE, t + asind(hw / P.R_YOKE), n - asind(hw / P.R_YOKE)))  # slot bottom
        segs.append(("L", pol(P.R_YOKE, n - asind(hw / P.R_YOKE)), pol(P.R_SHOE, n - asind(hw / P.R_SHOE))))
        segs.append(("A", P.R_SHOE, s + asind(ho / P.R_SHOE), n - asind(hw / P.R_SHOE)))
        segs.append(("L", pol(P.R_SHOE, s + asind(ho / P.R_SHOE)), pol(P.R_OD, s + asind(ho / P.R_OD))))
    return segs


def stator_bore():
    pitch = 360 / P.SLOTS
    hn = P.NOTCH_W / 2
    r2 = P.R_BORE + P.NOTCH_D
    centres = sorted((k - 1) * pitch for k in P.NOTCH_TEETH)
    segs = []
    for j, c in enumerate(centres):
        nxt = centres[(j + 1) % len(centres)] + (360 if j == len(centres) - 1 else 0)
        a0, a1 = c - asind(hn / P.R_BORE), c + asind(hn / P.R_BORE)
        b0, b1 = c - asind(hn / r2), c + asind(hn / r2)
        segs.append(("L", pol(P.R_BORE, a0), pol(r2, b0)))
        segs.append(("A", r2, b0, b1))
        segs.append(("L", pol(r2, b1), pol(P.R_BORE, a1)))
        segs.append(("A", P.R_BORE, a1, nxt - asind(hn / P.R_BORE)))
    return segs


# ---------------------------------------------------------------- DXF writers
def write_dxf(path, loops, flat=False):
    doc = ezdxf.new("R12", units=0)
    msp = doc.modelspace()
    for segs in loops:
        for s in segs:
            if s[0] == "L":
                msp.add_line(s[1], s[2], dxfattribs={"layer": "CUT"})
            elif s[0] == "A":
                _, r, a1, a2 = s
                if not flat:
                    msp.add_arc((0, 0), r, a1 % 360, a2 % 360, dxfattribs={"layer": "CUT"})
                else:
                    span = (a2 - a1) % 360 or 360
                    n = max(2, math.ceil(span / 0.5))
                    pts = [pol(r, a1 + span * k / n) for k in range(n + 1)]
                    for p, q in zip(pts, pts[1:]):
                        msp.add_line(p, q, dxfattribs={"layer": "CUT"})
            elif s[0] == "C":
                if not flat:
                    msp.add_circle((0, 0), s[1], dxfattribs={"layer": "CUT"})
                else:
                    write_seg_flat_circle(msp, s[1])
    doc.saveas(path)


def write_seg_flat_circle(msp, r):
    n = 720
    pts = [pol(r, 360 * k / n) for k in range(n + 1)]
    for p, q in zip(pts, pts[1:]):
        msp.add_line(p, q, dxfattribs={"layer": "CUT"})


# ---------------------------------------------------------------- 3D
def wire_from(segs):
    edges = []
    for s in segs:
        if s[0] == "L":
            edges.append(cq.Edge.makeLine(cq.Vector(*s[1], 0), cq.Vector(*s[2], 0)))
        else:
            _, r, a1, a2 = s
            edges.append(cq.Edge.makeCircle(r, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a1, a2))
    return cq.Wire.assembleEdges(edges)


def stator_solid(height):
    face = cq.Face.makeFromWires(wire_from(stator_outer()), [wire_from(stator_bore())])
    return cq.Workplane().add(cq.Solid.extrudeLinear(face, cq.Vector(0, 0, height)))
