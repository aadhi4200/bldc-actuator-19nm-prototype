"""Draw previews/bldc_v1_test_stand_section.png (cut through the motor axis). Run from phase1-motor/scripts."""
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import cadquery as cq
import build_test_stand as T
from functools import reduce
parts, bu, bl, stack, ring_t, blocks = T.main()
mags = reduce(lambda a,b:a.union(b), blocks)
items=[("base_plate",parts["base"],"#b8bcc4"),("hub (nylon)",parts["hub"],"#e8e4d0"),("6000ZZ",bu,"#6b7a8f"),("",bl,"#6b7a8f"),
 ("shaft",parts["shaft"],"#4a5568"),("spacer",parts["spacer"],"#2d3748"),("circlip",parts["circlip"],"#111"),
 ("stator stack",stack,"#8a8f99"),("rotor ring",ring_t,"#555b66"),("N35 blocks",mags,"#c0392b"),("bell (nylon)",parts["bell"],"#f3efe0")]
fig,ax=plt.subplots(figsize=(11,6))
for name,wp,col in items:
    half=wp.intersect(cq.Workplane().box(400,200,400,centered=(True,False,True)).translate((0,-200,0)))
    for f in half.faces().vals():
        n=f.normalAt(); c=f.Center()
        if abs(abs(n.y)-1)>1e-6 or abs(c.y)>1e-6: continue
        def P(w): return [(v.x,v.z) for v in [w.positionAt(t/300) for t in range(301)]]
        ax.add_patch(Polygon(P(f.outerWire()),closed=True,fc=col,ec="k",lw=0.4,label=name)); name=""
        for iw in f.innerWires(): ax.add_patch(Polygon(P(iw),closed=True,fc="white",ec="k",lw=0.4))
# end-turn envelope
for sx in (1,-1):
  for z0 in (-4,18):
    ax.add_patch(Polygon([(sx*29.5,z0),(sx*38.5,z0),(sx*38.5,z0+4),(sx*29.5,z0+4)],fc="#d4882b",alpha=0.5,ec="none",label="winding end turns (est.)" if (sx==1 and z0==-4) else ""))
ax.set_xlim(-70,70); ax.set_ylim(-20,40); ax.set_aspect("equal"); ax.grid(alpha=0.2)
ax.set_xlabel("x (mm)"); ax.set_ylabel("z (mm)")
ax.set_title("BLDC v1 test stand: section through the motor axis (test rotor)")
h,l=ax.get_legend_handles_labels(); ax.legend([a for a,b in zip(h,l) if b],[b for b in l if b],fontsize=7,loc="upper right",ncol=2)
fig.savefig("../previews/bldc_v1_test_stand_section.png",dpi=110,bbox_inches="tight")
