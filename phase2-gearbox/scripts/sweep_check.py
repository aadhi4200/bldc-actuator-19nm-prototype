import numpy as np
from profile import cycloid
R,RP,E,N=34.0,3.0,1.5,10
x,y=cycloid(R,RP,E,N,n=7200)
print("disc profile r: min %.3f  max %.3f"%(np.hypot(x,y).min(),np.hypot(x,y).max()))
worst={"housing_bore_r34":9,"ring_pins":9,"output_pins":9}
for th in np.linspace(0,2*np.pi,721):
  for ph in (0,np.pi):
    r=ph-th/9; c,s=np.cos(r),np.sin(r)
    X=x*c-y*s+E*np.cos(th+ph); Y=x*s+y*c+E*np.sin(th+ph)
    rr=np.hypot(X,Y); worst["housing_bore_r34"]=min(worst["housing_bore_r34"],34-rr.max())
    for i in range(N):
        a=2*np.pi*i/N; d=np.hypot(X-R*np.cos(a),Y-R*np.sin(a)).min()-RP; worst["ring_pins"]=min(worst["ring_pins"],d)
    # output pins Ø5 at r23 rotating -th/9 vs disc holes Ø8.3 centred at disc's own frame
    for i in range(6):
        a=2*np.pi*i/6
        hx=23*np.cos(a+r)+E*np.cos(th+ph); hy=23*np.sin(a+r)+E*np.sin(th+ph)    # hole centre (disc frame)
        px=23*np.cos(a-th/9 + (ph if False else 0)); py=23*np.sin(a-th/9)
        # disc B (ph=0): holes at a+r ; disc A rotated 180 -> holes set is same 6-fold, pick nearest pin
        dmin=min(np.hypot(hx-23*np.cos(b-th/9),hy-23*np.sin(b-th/9)) for b in 2*np.pi*np.arange(6)/6)
        worst["output_pins"]=min(worst["output_pins"],8.3/2-(dmin+2.5))
for k,v in worst.items(): print(f"min radial clearance disc vs {k:18s}: {v:+.3f} mm")
