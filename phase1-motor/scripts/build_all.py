"""Regenerate every DXF, STEP and preview for the BLDC actuator v1 motor core.

Usage (any OS with Python 3.10+):
    pip install -r scripts/requirements.txt
    python scripts/build_all.py

Coordinates (all files): mm, Z = motor axis, origin = centre of the stator stack's bottom face,
tooth 1 on +X, teeth numbered counter-clockwise seen from +Z.
"""
import math
from pathlib import Path

import cadquery as cq
import ezdxf

import params as P
from paths import DXF, DXF_FLAT, PREV, step, to_f360


NAMES = {
    "plate": "bldc_v1_stator_plate_24N28P_80mm_ms1mm",
    "stack": "bldc_v1_stator_stack_24N28P_80mm_18mm",
    "ring_final": "bldc_v1_rotor_ring_final_93.4x87.4x20_ms",
    "ring_test": "bldc_v1_rotor_ring_test_93.4x85.4x20_ms",
    "arc_magnet": "bldc_v1_magnet_arc_final_3mm_x28",
    "block_magnet": f"bldc_v1_magnet_block_test_{P.BLOCK_L:g}x{P.BLOCK_W:g}x{P.BLOCK_T:g}_N35_x{P.POLES * P.BLOCKS_PER_POLE}",
    "asm_final": "bldc_v1_motor_core_final_rotor",
    "asm_test": "bldc_v1_motor_core_test_rotor",
}


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


def ring(od, id_, length, z0):
    return (cq.Workplane().workplane(offset=z0).circle(od / 2).circle(id_ / 2).extrude(length))


def arc_magnet(angle_deg, z0):
    half = 360 / P.POLES * P.ARC_POLE_ARC / 2
    r1, r2 = P.R_MAG_IN, P.R_MAG_IN + P.ARC_MAG_T
    m = (cq.Workplane().workplane(offset=z0)
         .moveTo(*pol(r1, -half)).lineTo(*pol(r2, -half))
         .threePointArc(pol(r2, 0), pol(r2, half)).lineTo(*pol(r1, half))
         .threePointArc(pol(r1, 0), pol(r1, -half)).close().extrude(P.ARC_MAG_L))
    return m.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def block_offset():
    # Flat block in a concave ring: outer corners touch the ring ID, so the face centre sits slightly inside.
    r_ring = P.TEST_RING_ID / 2
    outer = math.sqrt(r_ring**2 - (P.BLOCK_W / 2) ** 2)
    return outer - P.BLOCK_T  # radius of the block's inner face centre


def block_magnet(angle_deg, z0):
    r_in = block_offset()
    b = (cq.Workplane().box(P.BLOCK_T, P.BLOCK_W, P.BLOCK_L, centered=(False, True, False))
         .translate((r_in, 0, z0)))
    return b.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def union_all(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out.union(p)
    return out


def previews():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def draw(ax, segs, **kw):
        for sg in segs:
            if sg[0] == "L":
                ax.plot([sg[1][0], sg[2][0]], [sg[1][1], sg[2][1]], **kw)
            else:
                _, r, a1, a2 = sg
                span = (a2 - a1) % 360 or 360
                n = max(2, int(span / 0.5))
                xs, ys = zip(*[pol(r, a1 + span * k / n) for k in range(n + 1)])
                ax.plot(xs, ys, **kw)

    pitch = 360 / P.POLES
    half = pitch * P.ARC_POLE_ARC / 2
    for tag, ring_id in (("final", P.FINAL_RING_ID), ("test", P.TEST_RING_ID)):
        fig, axes = plt.subplots(1, 2, figsize=(14, 7))
        for ax, lim in zip(axes, (None, (P.R_OD - 4, P.R_OD + 7))):
            draw(ax, stator_outer(), color="k", lw=0.8)
            draw(ax, stator_bore(), color="k", lw=0.8)
            for r in (P.ROTOR_RING_OD / 2, ring_id / 2):
                draw(ax, [("A", r, 0, 360)], color="0.4", lw=0.8)
            for k in range(P.POLES):
                c = "tab:red" if k % 2 == 0 else "tab:blue"
                a = k * pitch
                if tag == "final":
                    r1, r2 = P.R_MAG_IN, P.R_MAG_IN + P.ARC_MAG_T
                    draw(ax, [("A", r1, a - half, a + half), ("A", r2, a - half, a + half),
                              ("L", pol(r1, a - half), pol(r2, a - half)),
                              ("L", pol(r1, a + half), pol(r2, a + half))], color=c, lw=1)
                else:
                    ri, hw = block_offset(), P.BLOCK_W / 2
                    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                    pts = [(ri, -hw), (ri + P.BLOCK_T, -hw), (ri + P.BLOCK_T, hw), (ri, hw), (ri, -hw)]
                    xs = [x * ca - y * sa for x, y in pts]
                    ys = [x * sa + y * ca for x, y in pts]
                    ax.plot(xs, ys, color=c, lw=1)
            ax.set_aspect("equal")
            ax.axis("off")
            if lim:
                ax.set_xlim(lim[0] * math.cos(0.05), lim[1])
                ax.set_ylim(-5, 5)
                ax.set_title("Air gap detail at tooth 1 (+X)")
            else:
                ax.set_title(f"24N28P, 80 mm stator, {tag} rotor (red N / blue S), tooth 1 on +X")
        fig.savefig(PREV / f"bldc_v1_top_view_{tag}_rotor.png", dpi=110, bbox_inches="tight")
        plt.close(fig)


def main():
    for d in (DXF, DXF_FLAT, PREV):
        d.mkdir(parents=True, exist_ok=True)

    # DXF (cut files: R12, LINE + ARC/CIRCLE only, single layer CUT, no reference geometry)
    plate_loops = [stator_outer(), stator_bore()]
    ring_final = [[("C", P.ROTOR_RING_OD / 2)], [("C", P.FINAL_RING_ID / 2)]]
    ring_test = [[("C", P.ROTOR_RING_OD / 2)], [("C", P.TEST_RING_ID / 2)]]
    for key, loops in (("plate", plate_loops), ("ring_final", ring_final), ("ring_test", ring_test)):
        write_dxf(DXF / f"{NAMES[key]}.dxf", loops)
        write_dxf(DXF_FLAT / f"{NAMES[key]}_flat.dxf", loops, flat=True)

    # Parts
    ring_z0 = (P.STACK_L - P.RING_LENGTH) / 2
    plate = stator_solid(P.PLATE_T)
    stack = stator_solid(P.STACK_L)
    rf = ring(P.ROTOR_RING_OD, P.FINAL_RING_ID, P.RING_LENGTH, ring_z0)
    rt = ring(P.ROTOR_RING_OD, P.TEST_RING_ID, P.RING_LENGTH, ring_z0)
    pitch = 360 / P.POLES
    mag_z0 = (P.STACK_L - P.ARC_MAG_L) / 2
    arcs = [arc_magnet(k * pitch, mag_z0) for k in range(P.POLES)]
    blk_z0 = (P.STACK_L - P.BLOCKS_PER_POLE * P.BLOCK_L) / 2
    blocks = [block_magnet(k * pitch, blk_z0 + j * P.BLOCK_L)
              for k in range(P.POLES) for j in range(P.BLOCKS_PER_POLE)]

    cq.exporters.export(plate, str(step("laser_cut", NAMES["plate"])))
    cq.exporters.export(stack, str(step("laser_cut", NAMES["stack"])))
    cq.exporters.export(rf, str(step("machined", NAMES["ring_final"])))
    cq.exporters.export(rt, str(step("machined", NAMES["ring_test"])))
    cq.exporters.export(arcs[0], str(step("bought", NAMES["arc_magnet"])))
    cq.exporters.export(blocks[0], str(step("bought", NAMES["block_magnet"])))

    # Assemblies with named components (Fusion 360 imports each as a component)
    steel, n_col, s_col = cq.Color(0.55, 0.55, 0.6), cq.Color(0.85, 0.15, 0.15), cq.Color(0.15, 0.3, 0.85)
    for key, rng, mags, label in (("asm_final", rf, arcs, "arc"), ("asm_test", rt, blocks, "block")):
        a = cq.Assembly(name=NAMES[key])
        a.add(stack, name="stator_stack", color=steel)
        a.add(rng, name="rotor_ring", color=cq.Color(0.35, 0.35, 0.38))
        per = 1 if label == "arc" else P.BLOCKS_PER_POLE
        for idx, m in enumerate(mags):
            pole = idx // per
            col = n_col if pole % 2 == 0 else s_col
            nm = f"magnet_P{pole + 1:02d}_{'N' if pole % 2 == 0 else 'S'}" + ("" if per == 1 else f"_{idx % per + 1}")
            a.add(m, name=nm, color=col)
        a.export(str(step("assemblies", NAMES[key])))

    to_f360(DXF / f"{NAMES['plate']}.dxf", "sketches", f"{NAMES['plate']}_sketch.dxf")

    previews()

    # Report
    vol = stack.val().Volume()
    print(f"stator stack volume {vol:.0f} mm^3 -> {vol * P.STEEL_DENSITY:.0f} g mild steel")
    pitch_s = 360 / P.SLOTS
    rs, ry, hw = P.R_SHOE, P.R_YOKE, P.TOOTH_WIDTH / 2
    slot_area = math.radians(pitch_s) / 2 * (rs**2 - ry**2) - 2 * (
        # area of the tooth half-bodies between ry and rs (approx. as parallel strip)
        hw * (rs - ry))
    print(f"slot area (approx) {slot_area:.1f} mm^2")
    print(f"min air gap, test blocks {block_offset() - P.R_OD:.3f} mm; final arcs {P.AIR_GAP:.2f} mm")


def build_everything():
    """Motor core, test stand, magnet jig and tabbed sheet in one run."""
    main()
    import build_test_stand, build_magnet_jig, build_tabbed_sheet
    build_test_stand.main()
    build_magnet_jig.main()
    body, w, h = build_tabbed_sheet.build()
    build_tabbed_sheet.write_r12(body, DXF / f"{NAMES['plate']}_x20_tabbed_sheet_{w:.0f}x{h:.0f}.dxf")


if __name__ == "__main__":
    build_everything()
