"""Draw previews/bldc_v1_magnet_jig_top_view.png. Run from phase1-motor/n52/scripts."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
import cadquery as cq

import params as P
import build_magnet_jig as J
from build_all import ring, block_magnet
from paths import PREV


def draw_slice(ax, wp, z, col, max_area=None):
    sl = wp.intersect(cq.Workplane().workplane(offset=z - 0.01).rect(300, 300).extrude(0.02))
    for f in sl.faces().vals():
        if abs(abs(f.normalAt().z) - 1) > 1e-6 or abs(f.Center().z - (z - 0.01)) > 1e-3:
            continue
        if max_area and f.Area() > max_area:
            continue
        verts, codes = [], []
        for i, w in enumerate([f.outerWire()] + f.innerWires()):
            pts = [(v.x, v.y) for v in [w.positionAt(t / 240) for t in range(241)]]
            area = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:]))
            if (i == 0) != (area > 0):      # outline counter-clockwise, holes clockwise
                pts = pts[::-1]
            verts += pts
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MPath(verts, codes), fc=col, ec="k", lw=0.4))


def main():
    jig = J.jig()
    rt = ring(P.ROTOR_RING_OD, P.TEST_RING_ID, P.RING_LENGTH, J.RING_Z0)
    pitch = 360 / P.POLES
    fig, axs = plt.subplots(1, 2, figsize=(13, 6.5))
    views = ((axs[0], "Jig with the test ring and N35 blocks (cut at z = 5 mm)", (-55, 55, -55, 55)),
             (axs[1], "Detail: fingers between pockets, N / S marks on the base", (28, 50, -11, 11)))
    for ax, title, lim in views:
        draw_slice(ax, jig, -1.3, "#e4e1d3")                 # base
        draw_slice(ax, jig, -0.7, "#7a786e", max_area=50)    # raised N / S letters
        draw_slice(ax, jig, 3.0, "#b8b4a2")                  # lip
        draw_slice(ax, jig, 5, "#b8b4a2")                    # fingers
        draw_slice(ax, rt, 5, "#555b66")
        for k in range(P.POLES):
            draw_slice(ax, block_magnet(k * pitch, J.RING_Z0), 5, "#c0392b" if k % 2 == 0 else "#2e6db4")
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=10)
        ax.axis("off")
        ax.set_xlim(lim[0], lim[1])
        ax.set_ylim(lim[2], lim[3])
    fig.savefig(str(PREV / "bldc_v1_magnet_jig_top_view.png"), dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    main()
