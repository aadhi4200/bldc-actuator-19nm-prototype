import numpy as np, cadquery as cq
src=open("build_v2.py").read().split("parts={")[0]
exec(src)
rot1=cq.importers.importStep("out_v2/07_rotor_one_piece_steel.step")
def V(a,b):
    q=a.intersect(b); return q.val().Volume() if q.solids().size() else 0.0
def place(th,ph,z):
    return disc.rotate((0,0,0),(0,0,1),np.degrees(ph-th/9)).translate((E*np.cos(th+ph),E*np.sin(th+ph),z))
pins=cq.Workplane()
for i in range(N):
    a=2*np.pi*i/N; pins=pins.union(cyl(6,16,12,R*np.cos(a),R*np.sin(a)))
worst={}
for th in np.radians(np.arange(0,360,15)):
    dB=place(th,0,12.5); dA=place(th,np.pi,20)
    rr=lambda w: w.rotate((0,0,0),(0,0,1),np.degrees(th))
    oo=lambda w: w.rotate((0,0,0),(0,0,1),-np.degrees(th)/9)
    op=cq.Workplane()
    for i in range(6):
        a=2*np.pi*i/6; op=op.union(cyl(5,25,2,23*np.cos(a),23*np.sin(a)))
    others={"housing":housing,"ring_pins":pins,"can":can,"retainer":oo(ret),"output_flange":oo(flange),"output_pins":oo(op),
            "cam_flange":rr(cyl(38,4,29)),"rotor":rr(rot1)}
    for nm,d in (("discA",dA),("discB",dB)):
        for k,o in others.items():
            worst[(nm,k)]=max(worst.get((nm,k),0),V(d,o))
    worst[("discA","discB")]=max(worst.get(("discA","discB"),0),V(dA,dB))
bad={k:v for k,v in worst.items() if v>1e-6}
print("checked 24 positions x", len(worst),"pairs ->", "NO contact anywhere" if not bad else bad)
