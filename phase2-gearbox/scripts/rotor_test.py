import cadquery as cq, numpy as np
def cyl(d,h,z=0,x=0,y=0): return cq.Workplane().circle(d/2).extrude(h).translate((x,y,z))
# one-piece rotor (EN8 / C45 steel): ring z34..59 (back iron), web z34..37, boss Ø38 z33..39, shaft Ø10 z25..67.5
r=cyl(93.4,25,34).cut(cyl(85.4,22,37))          # cup: floor z34..37, wall to z59
r=r.union(cyl(38,6,33)).cut(cyl(20,2,33))         # boss + Ø20 spigot recess
r=r.union(cyl(10,42.5,25))                        # integral shaft (pilot z25..33, bearings + magnet above)
for i in range(5):
    a=2*np.pi*i/5+np.pi/2; x,y=15*np.cos(a),15*np.sin(a)
    r=r.cut(cyl(3.4,6,33,x,y)).cut(cyl(6.5,2.5,36.5,x,y))
for i in range(5):
    a=2*np.pi*i/5+np.pi/2+np.pi/5; r=r.cut(cyl(16,3,34,31*np.cos(a),31*np.sin(a)))
r=r.edges(cq.selectors.NearestToPointSelector((0,0,67.5))).chamfer(0.5)
cq.exporters.export(r,"out_v2/07b_rotor_one_piece_TEST_85.4bore.step"); cq.exporters.export(r,"out_v2/07b_rotor_one_piece_TEST_85.4bore.stl",tolerance=0.01,angularTolerance=0.1)
cq.exporters.export(r,"out_v2/07b_rotor_one_piece_TEST_85.4bore.svg",opt={"projectionDir":(0,0,1),"showHidden":False,"width":500,"height":500,"marginLeft":20,"marginTop":20})
v=r.val().Volume(); print("vol %.1f cm3, mass steel %.0f g (+ magnets ~%.0f g)"%(v/1000,v*7.85e-3,28*3*8*18*7.5e-3))
# clearance re-check vs fixed parts and cam

