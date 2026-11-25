import numpy as np
def cycloid(R=34.0, rp=3.0, e=1.5, N=10, n=1800, clr=0.10):
    rp = rp + clr  # running clearance
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    psi = np.arctan2(np.sin((1-N)*t), R/(e*N) - np.cos((1-N)*t))
    x = R*np.cos(t) - rp*np.cos(t+psi) - e*np.cos(N*t)
    y = -R*np.sin(t) + rp*np.sin(t+psi) + e*np.sin(N*t)
    return x, y
if __name__ == "__main__":
    x,y = cycloid()
    r = np.hypot(x,y); print("rmin %.3f rmax %.3f"%(r.min(), r.max()))
    # curvature sign check (no cusps/self-intersection)
    dx,dy = np.gradient(x),np.gradient(y); ddx,ddy=np.gradient(dx),np.gradient(dy)
    k=(dx*ddy-dy*ddx)/(dx**2+dy**2)**1.5
    print("min radius of curvature (concave part) %.2f mm"%(1/np.abs(k[k<0]).max() if (k<0).any() else np.inf), "convex min %.2f"%(1/k[k>0].max()))
