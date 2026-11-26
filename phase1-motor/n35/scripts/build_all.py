"""Variant N35: 20 mm stack + 28 x 20x5x2 N35 blocks, in the actuator v2 (flipped motor) layout.

Builds: stator plate DXF (+ flat backup) and 24-plate tabbed sheet, stator plate and 20 mm stack STEP,
magnet block, one-piece steel rotor, stator hub, motor can, back plate, back cover, a motor assembly
and a full actuator assembly (gearbox parts taken unchanged from phase2-gearbox/scripts/build_v2.py),
plus clearance checks including the winding end turns.

Usage (Python 3.10+, from the repo root):
    pip install -r phase1-motor/n35/scripts/requirements.txt
    python phase1-motor/n35/scripts/build_all.py

Coordinates: mm, Z = actuator axis, same origin as phase2-gearbox (output face at z = -5).
Tooth 1 and pole 1 (N) on +X.
"""
import math
import os
import sys
from pathlib import Path

import cadquery as cq

import params as P
from paths import DXF, DXF_FLAT, PREV, step, to_f360
from stator import pol, stator_outer, stator_bore, stator_solid, write_dxf

HERE = Path(__file__).resolve().parent
PHASE2 = HERE.parents[2] / "phase2-gearbox" / "scripts"

NAMES = {
    "plate": "bldc_v1_stator_plate_24N28P_80mm_ms1mm",
    "stack": f"bldc_n35_stator_stack_24N28P_80mm_{P.STACK_L:g}mm",
    "block": f"bldc_n35_magnet_block_{P.BLOCK_L:g}x{P.BLOCK_W:g}x{P.BLOCK_T:g}_{P.BLOCK_GRADE}_x{P.POLES}",
    "rotor": f"act_n35_07_rotor_one_piece_steel_{P.ROTOR_BORE:g}bore_20mm",
    "hub": "act_n35_10_stator_hub_20mm",
    "can": "act_n35_06_motor_can_20mm",
    "bp": "act_n35_11_back_plate",
    "bc": "act_n35_12_back_cover",
    "asm_motor": "act_n35_motor_assembly_20mm_N35",
    "asm_act": "act_n35_assembly_flipped_motor_cycloidal_20mm_N35",
}


def cyl(d, h, z=0.0, x=0.0, y=0.0):
    return cq.Workplane().circle(d / 2).extrude(h).translate((x, y, z))


def ring_z(od, id_, z0, z1):
    return cyl(od, z1 - z0, z0).cut(cyl(id_, z1 - z0, z0))


# ---------------------------------------------------------------- magnets
def block_r_in():
    """Flat block in the round bore: outer corners touch the bore, so the face centre sits inside."""
    rb = P.ROTOR_BORE / 2
    return math.sqrt(rb**2 - (P.BLOCK_W / 2) ** 2) - P.BLOCK_T


def block(angle_deg):
    b = (cq.Workplane().box(P.BLOCK_T, P.BLOCK_W, P.BLOCK_L, centered=(False, True, False))
         .translate((block_r_in(), 0, P.Z_STACK0)))
    return b.rotate((0, 0, 0), (0, 0, 1), angle_deg)


# ---------------------------------------------------------------- parts
def stack():
    return stator_solid(P.STACK_L).translate((0, 0, P.Z_STACK0))


def rotor():
    """One-piece EN8 / C45 rotor. Cam interface (boss, spigot, 5 x M3, shaft pilot) as phase2 part 07."""
    r = cyl(P.ROTOR_OD, P.Z_ROTOR_TOP - 34, 34)                                   # cup, floor z34..37
    r = r.cut(cyl(P.MAGNET_SEAT_ID, P.Z_STACK0 - P.Z_FLOOR_TOP, P.Z_FLOOR_TOP))   # ledge z37..42
    r = r.cut(cyl(P.ROTOR_BORE, P.Z_ROTOR_TOP - P.Z_STACK0, P.Z_STACK0))          # magnet bore z42..62
    r = r.union(cyl(38, 6, 33)).cut(cyl(20, 2, 33))                               # boss + Ø20 spigot recess
    r = r.union(cyl(10, P.Z_SHAFT_TIP - 25, 25))                                  # integral Ø10 shaft
    for i in range(5):
        a = 2 * math.pi * i / 5 + math.pi / 2
        x, y = 15 * math.cos(a), 15 * math.sin(a)
        r = r.cut(cyl(3.4, 6, 33, x, y)).cut(cyl(6.5, 2.5, 36.5, x, y))           # M3 DIN 7984, counterbored
    for i in range(5):
        a = 2 * math.pi * i / 5 + math.pi / 2 + math.pi / 5
        r = r.cut(cyl(16, 3, 34, 31 * math.cos(a), 31 * math.sin(a)))             # lightening holes
    r = r.edges(cq.selectors.NearestToPointSelector((0, 0, P.Z_SHAFT_TIP))).chamfer(0.5)
    return r


HUB_TOP = P.Z_BACK_PLATE
SHOULDER_D = 56.0          # stator stop above the stack (on the yoke, inside the end turns)


def hub():
    """Al 6061: stator seat Ø51.9 z42..62, Ø56 stop z62..67, bore Ø26 J7 for 2 x 6000, 4 x M4 tapped top."""
    h = cyl(51.9, P.Z_STACK1 - P.Z_STACK0, P.Z_STACK0).union(cyl(SHOULDER_D, HUB_TOP - P.Z_STACK1, P.Z_STACK1))
    h = h.cut(cyl(26, HUB_TOP - P.Z_STACK0, P.Z_STACK0))
    zmid = (P.Z_STACK0 + HUB_TOP) / 2
    h = h.union(cyl(26, 2, zmid - 1).cut(cyl(22, 2, zmid - 1)))
    for i in range(4):
        a = 2 * math.pi * i / 4
        h = h.cut(cyl(3.3, 8, HUB_TOP - 8, 22 * math.cos(a), 22 * math.sin(a)))
    return h


CAN_OD, CAN_ID, BOLT_PCD = 106.0, 96.5, 85.0


def can():
    zb = P.Z_BACK_PLATE
    c = cyl(CAN_OD, 5, 28).cut(cyl(42, 5, 28)).union(ring_z(CAN_OD, CAN_ID, 33, zb))
    for i in range(6):
        a = 2 * math.pi * i / 6 + math.pi / 6
        c = c.cut(cyl(2.5, 5, 28, BOLT_PCD / 2 * math.cos(a), BOLT_PCD / 2 * math.sin(a)))
    for i in range(6):
        a = 2 * math.pi * i / 6
        c = c.cut(cyl(2.5, 8, zb - 8, 50.6 * math.cos(a), 50.6 * math.sin(a)))
    return c


def back_plate():
    zb, t = P.Z_BACK_PLATE, P.BACK_PLATE_T
    b = cyl(CAN_OD, t, zb).cut(cyl(14, t, zb))
    for i in range(6):
        a = 2 * math.pi * i / 6
        b = b.cut(cyl(3.4, t, zb, 50.6 * math.cos(a), 50.6 * math.sin(a)))
    for i in range(4):
        a = 2 * math.pi * i / 4
        x, y = 22 * math.cos(a), 22 * math.sin(a)
        b = b.cut(cyl(4.4, t, zb, x, y)).cut(cq.Workplane().add(
            cq.Solid.makeCone(2.2, 4.3, 2.1, cq.Vector(x, y, zb + t - 2.1), cq.Vector(0, 0, 1))))
    for i in range(3):
        a = 2 * math.pi * i / 3 + math.pi / 4
        b = b.cut(cyl(2.05, t, zb, 17 * math.cos(a), 17 * math.sin(a)))          # M2.5 encoder standoffs
    b = b.cut(cq.Workplane().center(35, 0).slot2D(12, 5, 90).extrude(t).translate((0, 0, zb)))  # phase leads
    return b


def back_cover():
    z0 = P.Z_BACK_PLATE + P.BACK_PLATE_T
    c = cyl(CAN_OD, 11.5, z0).cut(cyl(CAN_OD - 5, 9.5, z0))
    c = c.cut(cq.Workplane().center(50, 0).rect(14, 8).extrude(6).translate((0, 0, z0)))
    for i in range(6):
        a = 2 * math.pi * i / 6 + math.pi / 6
        c = c.cut(cyl(3.4, 11.5, z0, 50.6 * math.cos(a), 50.6 * math.sin(a)))
    return c


def end_turns():
    """Envelope of the winding end turns (assumed) above and below the stack, for clearance checks."""
    r0, r1 = P.END_TURN_R
    lo = ring_z(2 * r1, 2 * r0, P.Z_STACK0 - P.END_TURN, P.Z_STACK0)
    hi = ring_z(2 * r1, 2 * r0, P.Z_STACK1, P.Z_STACK1 + P.END_TURN)
    return lo.union(hi)


def bearing_6000(z0):
    return ring_z(26, 10, z0, z0 + 8)


# ---------------------------------------------------------------- gearbox (unchanged, from phase2)
def gearbox():
    """Run the phase2 v2 script up to its own motor parts and return the unchanged gearbox parts."""
    sys.path.insert(0, str(PHASE2))
    sys.modules.pop("profile", None)            # phase2's profile.py, not the stdlib profiler
    src = (PHASE2 / "build_v2.py").read_text().split("parts={")[0]
    cwd = os.getcwd()
    tmp = HERE / "_tmp_phase2"
    tmp.mkdir(exist_ok=True)
    os.chdir(tmp)
    ns = {}
    try:
        exec(src, ns)
    finally:
        os.chdir(cwd)
        for f in tmp.rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(tmp.rglob("*"), reverse=True):
            d.rmdir()
        tmp.rmdir()
    E = ns["E"]
    disc = ns["disc"]
    pins = cq.Workplane()
    for i in range(ns["N"]):
        a = 2 * math.pi * i / ns["N"]
        pins = pins.union(cyl(6, 16, 12, ns["R"] * math.cos(a), ns["R"] * math.sin(a)))
    opins = cq.Workplane()
    for i in range(ns["OP_N"]):
        a = 2 * math.pi * i / ns["OP_N"]
        opins = opins.union(cyl(5, 25, 2, ns["OP_R"] * math.cos(a), ns["OP_R"] * math.sin(a)))
    return {
        "housing_pin_ring": ns["housing"],
        "cycloid_disc_B": disc.translate((E, 0, 12.5)),
        "cycloid_disc_A": disc.rotate((0, 0, 0), (0, 0, 1), 180).translate((-E, 0, 20)),
        "output_flange": ns["flange"],
        "bearing_retainer": ns["ret"],
        "eccentric_cam_v2": ns["cam"],
        "ring_pins_x10": pins,
        "output_pins_x6": opins,
    }


# ---------------------------------------------------------------- checks
def overlap(a, b):
    r = a.intersect(b)
    return round(r.val().Volume(), 3) if r.solids().size() else 0.0


def checks(parts, mags, gb):
    rot = {"rotor": parts["rotor"], "magnets": mags, "cam": gb["eccentric_cam_v2"]}
    stat = {"stator": parts["stack"], "end_turns": end_turns(), "hub": parts["hub"], "can": parts["can"],
            "back_plate": parts["bp"], "back_cover": parts["bc"], "housing": gb["housing_pin_ring"],
            "ring_pins": gb["ring_pins_x10"]}
    bad = [(a, b, overlap(x, y)) for a, x in rot.items() for b, y in stat.items()
           if not (a == "cam" and b in ("housing", "ring_pins")) and overlap(x, y) > 0]
    bad += [("rotor", "cam", overlap(parts["rotor"], gb["eccentric_cam_v2"]))] \
        if overlap(parts["rotor"], gb["eccentric_cam_v2"]) > 0 else []
    bad += [("rotor", "magnets", overlap(parts["rotor"], mags))] if overlap(parts["rotor"], mags) > 0.01 else []
    lines = [
        f"overlaps: {bad if bad else 'none'}",
        f"air gap magnets -> stator: {block_r_in() - P.R_OD:.2f} mm at block centre",
        f"end turns -> rotor floor: {P.Z_STACK0 - P.END_TURN - P.Z_FLOOR_TOP:.1f} mm; "
        f"end turns -> back plate: {P.Z_BACK_PLATE - (P.Z_STACK1 + P.END_TURN):.1f} mm (end turns assumed {P.END_TURN:g} mm)",
        f"end turns -> magnet seat ledge (radial): {P.MAGNET_SEAT_ID / 2 - P.END_TURN_R[1]:.1f} mm; "
        f"end turns -> hub stop (radial): {P.END_TURN_R[0] - SHOULDER_D / 2:.1f} mm",
        f"rotor OD -> can ID: {(CAN_ID - P.ROTOR_OD) / 2:.2f} mm; hub bottom -> rotor boss top: {P.Z_STACK0 - 39:.1f} mm",
        f"gap between neighbouring blocks (inner edge): "
        f"{2 * math.pi * block_r_in() / P.POLES - P.BLOCK_W:.2f} mm",
    ]
    return lines


# ---------------------------------------------------------------- previews
def previews(parts, mags):
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

    # top view
    pitch = 360 / P.POLES
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    for ax, lim in zip(axes, (None, (P.R_OD - 4, P.R_OD + 7))):
        draw(ax, stator_outer(), color="k", lw=0.8)
        draw(ax, stator_bore(), color="k", lw=0.8)
        for r in (P.ROTOR_OD / 2, P.ROTOR_BORE / 2):
            draw(ax, [("A", r, 0, 360)], color="0.4", lw=0.8)
        ri, hw = block_r_in(), P.BLOCK_W / 2
        for k in range(P.POLES):
            a = math.radians(k * pitch)
            ca, sa = math.cos(a), math.sin(a)
            pts = [(ri, -hw), (ri + P.BLOCK_T, -hw), (ri + P.BLOCK_T, hw), (ri, hw), (ri, -hw)]
            ax.plot([x * ca - y * sa for x, y in pts], [x * sa + y * ca for x, y in pts],
                    color="tab:red" if k % 2 == 0 else "tab:blue", lw=1)
        ax.set_aspect("equal")
        ax.axis("off")
        if lim:
            ax.set_xlim(lim[0] * math.cos(0.05), lim[1])
            ax.set_ylim(-5, 5)
            ax.set_title(f"Air gap at tooth 1 (+X): {block_r_in() - P.R_OD:.2f} mm at block centre")
        else:
            ax.set_title("Variant N35: 24N28P, 80 mm stator, 28 x 20x5x2 N35 blocks (red N / blue S)")
    fig.savefig(PREV / "bldc_n35_top_view.png", dpi=110, bbox_inches="tight")
    plt.close(fig)

    # axial section (XZ plane, x >= 0)
    plane = cq.Face.makePlane(400, 400, basePnt=cq.Vector(0, 0, 0), dir=cq.Vector(0, 1, 0))
    fig, ax = plt.subplots(figsize=(8, 9))
    style = {"stack": ("0.45", "Stator 20 mm"), "rotor": ("0.25", "Rotor (steel)"), "mags": ("tab:red", "N35 blocks"),
             "hub": ("tab:cyan", "Stator hub"), "can": ("0.65", "Can"), "bp": ("tab:olive", "Back plate"),
             "bc": ("0.8", "Back cover"), "et": ("tab:orange", "End turns (assumed)")}
    solids = dict(parts)
    solids["mags"] = mags
    solids["et"] = end_turns()
    for key, (col, label) in style.items():
        sec = solids[key].val().intersect(plane)
        first = True
        for f in sec.Faces():
            for w in [f.outerWire()] + f.innerWires():
                pts = [w.positionAt(t / 400) for t in range(401)]
                xs, zs = [p.x for p in pts], [p.z for p in pts]
                if max(xs) < -1e-6:
                    continue
                ax.fill(xs, zs, color=col, alpha=0.6, lw=0.5, ec="k", label=label if first else None)
                first = False
    ax.set_xlim(0, 56)
    ax.set_ylim(22, 86)
    ax.set_aspect("equal")
    ax.set_xlabel("radius (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_title("Variant N35 motor section (gearbox below z 33 unchanged)")
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    ax.grid(alpha=0.3)
    fig.savefig(PREV / "bldc_n35_motor_section.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- main
def main():
    for d in (DXF, DXF_FLAT, PREV):
        d.mkdir(parents=True, exist_ok=True)

    loops = [stator_outer(), stator_bore()]
    write_dxf(DXF / f"{NAMES['plate']}.dxf", loops)
    write_dxf(DXF_FLAT / f"{NAMES['plate']}_flat.dxf", loops, flat=True)

    parts = {"stack": stack(), "rotor": rotor(), "hub": hub(), "can": can(), "bp": back_plate(), "bc": back_cover()}
    blocks = [block(k * 360 / P.POLES) for k in range(P.POLES)]
    mags = blocks[0]
    for b in blocks[1:]:
        mags = mags.union(b)

    cq.exporters.export(stator_solid(P.PLATE_T), str(step("laser_cut", NAMES["plate"])))
    cq.exporters.export(parts["stack"], str(step("laser_cut", NAMES["stack"])))
    cq.exporters.export(blocks[0], str(step("bought", NAMES["block"])))
    for key in ("rotor", "hub", "can", "bp", "bc"):
        cq.exporters.export(parts[key], str(step("machined", NAMES[key])))
        to_f360(step("machined", NAMES[key]), "machined")

    gb = gearbox()

    steel, alu, dark = cq.Color(0.55, 0.55, 0.6), cq.Color(0.78, 0.78, 0.8), cq.Color(0.3, 0.3, 0.33)
    red, blue = cq.Color(0.85, 0.15, 0.15), cq.Color(0.15, 0.3, 0.85)
    zmid = (P.Z_STACK0 + HUB_TOP) / 2

    def motor(a):
        a.add(parts["stack"], name="stator_stack_20mm", color=steel)
        a.add(parts["rotor"], name="rotor_07_one_piece", color=dark)
        for k, b in enumerate(blocks):
            a.add(b, name=f"magnet_P{k + 1:02d}_{'N' if k % 2 == 0 else 'S'}", color=red if k % 2 == 0 else blue)
        a.add(parts["hub"], name="stator_hub_10", color=alu)
        a.add(bearing_6000(P.Z_STACK0), name="bearing_6000_lower", color=steel)
        a.add(bearing_6000(HUB_TOP - 8), name="bearing_6000_upper", color=steel)
        a.add(parts["bp"], name="back_plate_11", color=alu)
        return a

    m = motor(cq.Assembly(name=NAMES["asm_motor"]))
    m.export(str(step("assemblies", NAMES["asm_motor"])))
    act = motor(cq.Assembly(name=NAMES["asm_act"]))
    act.add(parts["can"], name="motor_can_06", color=alu)
    act.add(parts["bc"], name="back_cover_12", color=alu)
    for nm, p in gb.items():
        act.add(p, name=nm, color=steel if "pins" in nm else alu)
    act.export(str(step("assemblies", NAMES["asm_act"])))
    for key in ("asm_motor", "asm_act"):
        to_f360(step("assemblies", NAMES[key]), "assemblies")
    to_f360(DXF / f"{NAMES['plate']}.dxf", "sketches", f"{NAMES['plate']}_sketch.dxf")

    import build_tabbed_sheet
    body, w, h = build_tabbed_sheet.build()
    build_tabbed_sheet.write_r12(body, DXF / f"{NAMES['plate']}_x24_tabbed_sheet_{w:.0f}x{h:.0f}.dxf")

    previews(parts, mags)

    v_rot = parts["rotor"].val().Volume()
    v_mag = P.POLES * P.BLOCK_L * P.BLOCK_W * P.BLOCK_T
    print(f"stack {parts['stack'].val().Volume() * P.STEEL_DENSITY:.0f} g, rotor {v_rot * P.STEEL_DENSITY:.0f} g "
          f"+ magnets {v_mag * P.NDFEB_DENSITY:.0f} g")
    print(f"sheet {w:.0f} x {h:.0f} mm (24 plates)")
    bb = act.toCompound().BoundingBox()
    print(f"actuator envelope: Ø{bb.xlen:.1f} x {bb.zlen:.1f} mm (z {bb.zmin:.1f} .. {bb.zmax:.1f})")
    for line in checks(parts, mags, gb):
        print(line)


if __name__ == "__main__":
    main()
