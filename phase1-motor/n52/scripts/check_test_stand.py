"""Check the test stand: valid solids, no overlaps, rotor-to-stator and end-turn clearances. Run from phase1-motor/n52/scripts."""
import itertools, cadquery as cq
import build_test_stand as T
parts, bu, bl, stack, ring_t, blocks = T.main()
from functools import reduce
mags = reduce(lambda a,b:a.union(b), blocks)
solids = {"hub":parts["hub"],"shaft":parts["shaft"],"spacer":parts["spacer"],"bell":parts["bell"],
 "circlip":parts["circlip"],"base":parts["base"],"brg_up":bu,"brg_lo":bl,"stack":stack,"ring":ring_t,"mags":mags}
for k,v in solids.items(): print(k,"valid",v.val().isValid(), round(v.val().Volume()))
print("--- overlaps > 0.01 mm^3")
for (a,A),(b,B) in itertools.combinations(solids.items(),2):
    v=A.intersect(B).val().Volume() if A.intersect(B).vals() else 0
    if v>0.01: print(a,b,round(v,3))
print("--- min distance rotor vs stator")
rot=["shaft","spacer","bell","ring","mags"]; sta=["hub","stack","base"]
for r in rot:
  for s in sta:
    d=solids[r].val().distance(solids[s].val())
    print(f"{r:7s}-{s:6s} {d:.3f}")
print("--- end-turn envelope (r 29.5-38.5, 4 mm above/below the stack) vs rotor")
env = (cq.Workplane().workplane(offset=-4).circle(38.5).circle(29.5).extrude(4)
       .union(cq.Workplane().workplane(offset=18).circle(38.5).circle(29.5).extrude(4)))
for r in rot+["base"]:
    print(f"{r:7s} {solids[r].val().distance(env.val()):.2f}")
