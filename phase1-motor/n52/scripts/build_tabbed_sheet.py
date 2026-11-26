"""Nested, tabbed sheet: 20 stator plates (4 x 5) held in a frame by micro-joint tabs.

Tabs sit on the tips of teeth 7 (+Y) and 19 (-Y) of each plate, away from the bore notches
(teeth 1 and 13). Break the plates out after delivery, file the stubs, then true the stack OD.

Usage: python phase1-motor/n52/scripts/build_tabbed_sheet.py
"""
import math
from pathlib import Path

import cadquery as cq
import ezdxf

import params as P
from build_all import stator_solid, NAMES
from paths import DXF

COLS, ROWS = 4, 5
GAP = 3.0          # gap between plates and between plates and frame (= tab length)
FRAME = 8.0        # frame border width
TAB_W = 0.8        # tab (micro-joint) width; ask the shop for their preferred value
ROOT = Path(__file__).resolve().parent.parent


def build():
    pitch = P.STATOR_OD + GAP
    inner_w = COLS * P.STATOR_OD + (COLS + 1) * GAP
    inner_h = ROWS * P.STATOR_OD + (ROWS + 1) * GAP
    outer_w, outer_h = inner_w + 2 * FRAME, inner_h + 2 * FRAME
    t = P.PLATE_T

    frame = (cq.Workplane().rect(outer_w, outer_h).extrude(t)
             .cut(cq.Workplane().rect(inner_w, inner_h).extrude(t)))
    body = frame
    plate = stator_solid(t)
    x0 = -inner_w / 2 + GAP + P.R_OD
    y0 = -inner_h / 2 + GAP + P.R_OD
    for c in range(COLS):
        for r in range(ROWS):
            x, y = x0 + c * pitch, y0 + r * pitch
            body = body.union(plate.translate((x, y, 0)))
            # tab above and below each plate (overlap 0.3 mm into the parts so they fuse)
            for sgn in (1, -1):
                ty = y + sgn * (P.R_OD + GAP / 2)
                tab = cq.Workplane().center(x, ty).rect(TAB_W, GAP + 0.6).extrude(t)
                body = body.union(tab)
    return body, outer_w, outer_h


def write_r12(body, path):
    face = body.faces("<Z").val()
    doc = ezdxf.new("R12", units=0)
    msp = doc.modelspace()
    for e in face.Edges():
        g = e.geomType()
        if g == "LINE":
            a, b = e.startPoint(), e.endPoint()
            msp.add_line((a.x, a.y), (b.x, b.y), dxfattribs={"layer": "CUT"})
        elif g == "CIRCLE":
            circ = e._geomAdaptor().Circle()
            c = circ.Location()
            r = circ.Radius()
            a, b = e.startPoint(), e.endPoint()
            if (a - b).Length < 1e-6:
                msp.add_circle((c.X(), c.Y()), r, dxfattribs={"layer": "CUT"})
                continue
            ang = lambda p: math.degrees(math.atan2(p.y - c.Y(), p.x - c.X()))
            # cut faces are seen from -Z on the bottom face; orient arcs CCW in XY
            mid = e.positionAt(0.5)
            a1, a2, am = ang(a), ang(b), ang(mid)
            span = (a2 - a1) % 360
            if not ((am - a1) % 360 < span):
                a1, a2 = a2, a1
            msp.add_arc((c.X(), c.Y()), r, a1 % 360, a2 % 360, dxfattribs={"layer": "CUT"})
        else:
            raise ValueError(f"unexpected edge type {g}")
    doc.saveas(path)


if __name__ == "__main__":
    body, w, h = build()
    out = DXF / f"{NAMES['plate']}_x20_tabbed_sheet_{w:.0f}x{h:.0f}.dxf"
    write_r12(body, out)
    print(out.name, f"sheet {w:.0f} x {h:.0f} mm")
