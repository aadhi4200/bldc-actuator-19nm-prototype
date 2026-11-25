import cadquery as cq, numpy as np, os
from profile import cycloid
OUT="out_v2"; os.makedirs(OUT, exist_ok=True)
# ---- key parameters (mm) ----
N=10; R=34.0; RP=3.0; E=1.5            # 10 ring pins Ø6 on Ø68, ecc 1.5 -> 9 lobes, 9:1
DISC_T=7.0; DISC_BORE=32.0              # 6804 bearing 20x32x7
OP_N=6; OP_R=23.0; OP_D=5.0             # 6 output pins Ø5 on Ø46
OP_HOLE=OP_D+2*E+0.3                    # 8.3
H_OD=94.0; PIN_BORE=69.0; BOLT_PCD=85.0
BRG_OD=78.0; BRG_W=10.0                 # 6812 60x78x10 output bearing
def cyl(d,h,z=0,x=0,y=0): return cq.Workplane().circle(d/2).extrude(h).translate((x,y,z))

# ---- cycloid disc (z 0..7, centred) ----
x,y = cycloid(R,RP,E,N,n=720)
pts=list(zip(x,y))
disc=(cq.Workplane().spline(pts,periodic=True).close().extrude(DISC_T)
      .faces(">Z").workplane().hole(DISC_BORE))
holes=cq.Workplane().polarArray(OP_R,0,360,OP_N).circle(OP_HOLE/2).extrude(DISC_T)
disc=disc.cut(holes)
# lightening + index mark
disc=disc.cut(cyl(1.5,DISC_T,0,0,DISC_BORE/2+1.5))

# ---- housing: z0..10 bearing seat, 10..12 shoulder, 12..28 pin ring ----
H_TOP=28.0
housing=cyl(H_OD,H_TOP)
housing=housing.cut(cyl(BRG_OD,BRG_W,0)).cut(cyl(66,2,BRG_W)).cut(cyl(PIN_BORE,16,12))
for i in range(N):
    a=2*np.pi*i/N
    housing=housing.cut(cyl(2*RP,16,12,R*np.cos(a),R*np.sin(a)))   # pin pockets, press/slip Ø6 dowels
for i in range(6):
    a=2*np.pi*i/6+np.pi/6
    housing=housing.cut(cyl(3.4,H_TOP,0,BOLT_PCD/2*np.cos(a),BOLT_PCD/2*np.sin(a)))

# ---- output flange: plate z-5..0 Ø64, hub z0..10 Ø60 ----
flange=cyl(64,5,-5).union(cyl(60,BRG_W,0))
flange=flange.cut(cyl(19,5,5)).cut(cyl(12,15,-5))            # 6800 pocket (10x19x5) + clearance
for i in range(OP_N):
    a=2*np.pi*i/OP_N
    flange=flange.cut(cyl(OP_D,8,2,OP_R*np.cos(a),OP_R*np.sin(a)))  # press-fit pins, 8 deep
for i in range(4):
    a=2*np.pi*i/4+np.pi/4
    flange=flange.cut(cyl(2.5,8,2,14*np.cos(a),14*np.sin(a)))  # M3 tap/insert for retainer
for i in range(6):
    a=2*np.pi*i/6+np.pi/6
    flange=flange.cut(cyl(4.2,10,-5,25*np.cos(a),25*np.sin(a)))  # M5 output holes (tap) on Ø50

# ---- retainer washer z10..11.5 (clamps 6812 inner race) ----
ret=cyl(64,1.5,10).cut(cyl(13,1.5,10))
for i in range(OP_N):
    a=2*np.pi*i/OP_N; ret=ret.cut(cyl(OP_D+0.2,1.5,10,OP_R*np.cos(a),OP_R*np.sin(a)))
for i in range(4):
    a=2*np.pi*i/4+np.pi/4; ret=ret.cut(cyl(3.4,1.5,10,14*np.cos(a),14*np.sin(a)))


# ======================= v2: FLIPPED MOTOR =======================
TOL=0
# ---- 05 cam v2: journal, lobes, neck, Ø38 flange z29..33 (5xM3 on Ø30), Ø20 spigot z33..35, Ø10 shaft bore z25..35
cam=(cyl(10,9.5,3).union(cyl(20,7,12.5,E,0)).union(cyl(16,0.5,19.5)).union(cyl(20,7,20,-E,0))
     .union(cyl(16,2,27)).union(cyl(38,4,29)).union(cyl(20,2,33)))
cam=cam.cut(cyl(10,10,25))                                       # rotor shaft pilot bore
for i in range(5):
    a=2*np.pi*i/5+np.pi/2; cam=cam.cut(cyl(2.5,4,29,15*np.cos(a),15*np.sin(a)))   # M3 tap, blind 4 from top... through flange
# ---- 06 motor can: bottom plate z28..33 Ø106 (Ø42 hole), wall ID96.5 z33..60.5
CAN_OD=106; CAN_ID=96.5; ZBP=60.5
can=cyl(CAN_OD,5,28).cut(cyl(42,5,28)).union(cyl(CAN_OD,ZBP-33,33).cut(cyl(CAN_ID,ZBP-33,33)))
for i in range(6):
    a=2*np.pi*i/6+np.pi/6; can=can.cut(cyl(2.5,5,28,BOLT_PCD/2*np.cos(a),BOLT_PCD/2*np.sin(a)))        # M3 tap, bolts from output side
for i in range(6):
    a=2*np.pi*i/6; can=can.cut(cyl(2.5,8,ZBP-8,50.6*np.cos(a),50.6*np.sin(a)))                         # M3 tap for back plate
# ---- 07 rotor hub (Al): spigot recess Ø20x2, boss Ø38 z33..39, web Ø93.4 z34..37, register Ø87.4 z37..39
rh=cyl(38,6,33).union(cyl(93.4,3,34)).union(cyl(87.4,2,37).cut(cyl(80,2,37)))
rh=rh.cut(cyl(20,2,33)).cut(cyl(10,6,33))
for i in range(5):
    a=2*np.pi*i/5+np.pi/2; x,y=15*np.cos(a),15*np.sin(a)
    rh=rh.cut(cyl(3.4,6,33,x,y)).cut(cyl(6.5,2.5,36.5,x,y))       # M3 low-head (DIN 7984) counterbored flush
for i in range(5):
    a=2*np.pi*i/5+np.pi/2+np.pi/5; rh=rh.cut(cyl(16,3,34,31*np.cos(a),31*np.sin(a)))   # lightening
# ---- 08 rotor ring (mild steel) 93.4/87.4 x 22, z37..59
ring=cyl(93.4,22,37).cut(cyl(87.4,22,37))
# ---- 09 shaft Ø10 steel z25..67.5
shaft=cyl(10,42.5,25)
# ---- 10 stator hub (Al) Ø51.9 z40..60.5, bore Ø26 with Ø22 shoulder z49.5..51.5, 4xM4 tap top
hub=cyl(51.9,20.5,40).cut(cyl(26,20.5,40)).union(cyl(26,2,49.5).cut(cyl(22,2,49.5)))
for i in range(4):
    a=2*np.pi*i/4; hub=hub.cut(cyl(3.3,8,52.5,22*np.cos(a),22*np.sin(a)))
# ---- 11 back plate (Al) Ø106 z60.5..65.5
bp=cyl(CAN_OD,5,ZBP).cut(cyl(14,5,ZBP))
for i in range(6):
    a=2*np.pi*i/6; bp=bp.cut(cyl(3.4,5,ZBP,50.6*np.cos(a),50.6*np.sin(a)))
for i in range(4):
    a=2*np.pi*i/4; x,y=22*np.cos(a),22*np.sin(a)
    bp=bp.cut(cyl(4.4,5,ZBP,x,y)).cut(cq.Workplane().add(cq.Solid.makeCone(2.2,4.3,2.1,cq.Vector(x,y,ZBP+5-2.1),cq.Vector(0,0,1))))  # c'sunk from top
for i in range(3):
    a=2*np.pi*i/3+np.pi/4; bp=bp.cut(cyl(2.05,5,ZBP,17*np.cos(a),17*np.sin(a)))        # M2.5 tap for encoder PCB standoffs
bp=bp.cut(cq.Workplane().center(35,0).slot2D(12,5,90).extrude(5).translate((0,0,ZBP)))   # phase-lead slot
# ---- 12 back cover (Al or MJF) cup Ø106, z65.5..77, cable notch
bc=cyl(CAN_OD,11.5,65.5).cut(cyl(CAN_OD-5,9.5,65.5)).cut(cq.Workplane().center(50,0).rect(14,8).extrude(6).translate((0,0,65.5)))
for i in range(6):
    a=2*np.pi*i/6+np.pi/6; bc=bc.cut(cyl(3.4,11.5,65.5,50.6*np.cos(a),50.6*np.sin(a)))

parts={"01_housing_pin_ring":housing,"02_cycloid_disc_x2":disc,"03_output_flange":flange,"04_bearing_retainer":ret,
       "05_eccentric_cam_v2":cam,"06_motor_can":can,"07_rotor_hub":rh,"08_rotor_ring_mild_steel":ring,"09_shaft_10mm":shaft,
       "10_stator_hub":hub,"11_back_plate":bp,"12_back_cover":bc}
for n,p in parts.items():
    cq.exporters.export(p,f"{OUT}/{n}.step"); cq.exporters.export(p,f"{OUT}/{n}.stl",tolerance=0.01,angularTolerance=0.1)
    cq.exporters.export(p,f"{OUT}/{n}.svg",opt={"projectionDir":(0,0,1),"showHidden":False,"width":500,"height":500,"marginLeft":20,"marginTop":20})
    bb=p.val().BoundingBox(); print(f"{n:28s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  z{bb.zmin:5.1f}..{bb.zmax:5.1f}")

# ---- static clearance checks: rotating input group vs stationary parts, and vs output group
def V(a,b):
    r=a.intersect(b); return round(r.val().Volume(),3) if r.solids().size() else 0
stator=cyl(80,18,40).cut(cyl(52,18,40))      # envelope
mags=cyl(87.4,18,40).cut(cyl(81.4,18,40))
rot_in={"cam":cam,"rotor_hub":rh,"ring":ring,"shaft":shaft,"mags":mags}
stat={"housing":housing,"can":can,"hub":hub,"stator":stator,"back_plate":bp,"back_cover":bc}
pins=cq.Workplane()
for i in range(N):
    a=2*np.pi*i/N; pins=pins.union(cyl(6,16,12,R*np.cos(a),R*np.sin(a)))
stat["ring_pins"]=pins
bad=[(a,b,V(x,y)) for a,x in rot_in.items() for b,y in stat.items() if V(x,y)>0]
dB=disc.translate((E,0,12.5)); dA=disc.rotate((0,0,0),(0,0,1),180).translate((-E,0,20))
for nm,d in [("discA",dA),("discB",dB)]:
    for b,y in {"can":can,"rotor_hub":rh,"cam_flange":cyl(38,4,29)}.items():
        if V(d,y)>0: bad.append((nm,b,V(d,y)))
print("overlaps:",bad if bad else "none")
print("gap magnets->stator radial: %.2f mm, ring OD->can ID: %.2f mm"%((81.4-80)/2,(CAN_ID-93.4)/2))
