"""Generate figures for STAT3888 lectures 01-04."""
import numpy as np
from slides import _mpl, savefig, CAT, BLUE, ACCENT, TEAL, GOLD, PURPLE, GREY, INK, MUTED
plt = _mpl()
rng = np.random.default_rng(7)

def L01_super_vs_unsuper():
    fig, ax = plt.subplots(1, 2, figsize=(9.4, 4.2))
    # unsupervised
    for c, mu in zip([BLUE, ACCENT, TEAL], [(0,0),(3.2,2.6),(3.0,-2.4)]):
        p = rng.normal(mu, 0.7, (40,2))
        ax[0].scatter(p[:,0], p[:,1], color=GREY, s=26, edgecolor="w", lw=.5)
    ax[0].set_title("Unsupervised\n(no labels — find structure)")
    # supervised
    for c, mu in zip([BLUE, ACCENT, TEAL], [(0,0),(3.2,2.6),(3.0,-2.4)]):
        p = rng.normal(mu, 0.7, (40,2))
        ax[1].scatter(p[:,0], p[:,1], color=c, s=26, edgecolor="w", lw=.5)
    ax[1].set_title("Supervised\n(labels known — learn the boundary)")
    for a in ax:
        a.set_xticks([]); a.set_yticks([]); a.grid(False)
    fig.tight_layout()
    return savefig(fig, "L01_super_vs_unsuper.png")

def L01_pipeline():
    fig, ax = plt.subplots(figsize=(9.6, 2.8))
    stages = ["Raw data\n(nutrition survey)", "Clean &\nexplore", "Model\n(SL / UL)",
              "Evaluate\n& select", "Communicate\n& decide"]
    cols = [GREY, BLUE, ACCENT, TEAL, GOLD]
    x = np.linspace(0.5, 9.1, len(stages))
    for i,(xi,s,c) in enumerate(zip(x, stages, cols)):
        ax.add_patch(plt.Rectangle((xi-0.78,0.3),1.56,1.4, fc=c, ec="none", alpha=.92, zorder=2))
        ax.text(xi,1.0,s,ha="center",va="center",color="white",fontsize=11,fontweight="bold",zorder=3)
        if i < len(stages)-1:
            ax.annotate("", (x[i+1]-0.85,1.0),(xi+0.85,1.0),
                        arrowprops=dict(arrowstyle="-|>",color=INK,lw=2))
    ax.set_xlim(-0.2,9.9); ax.set_ylim(0,2.1); ax.axis("off")
    fig.tight_layout()
    return savefig(fig, "L01_pipeline.png")

def L02_missingness():
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    n, p = 30, 8
    M = (rng.random((n,p)) < np.array([.02,.03,.25,.05,.4,.02,.1,.06])).astype(float)
    M[10:18, 4] = 1  # block of missing -> MAR pattern
    ax.imshow(M, aspect="auto", cmap=plt.matplotlib.colors.ListedColormap([ "#eaf0f6", ACCENT]))
    ax.set_xticks(range(p)); ax.set_xticklabels([f"V{i+1}" for i in range(p)])
    ax.set_yticks([]); ax.set_ylabel("respondents")
    ax.set_title("Missing-data map  (red = missing)")
    ax.grid(False)
    fig.tight_layout()
    return savefig(fig, "L02_missingness.png")

def L02_scaling():
    fig, ax = plt.subplots(1, 2, figsize=(9.4, 4.2))
    energy = rng.normal(9000, 1800, 120)          # kJ
    vitc   = rng.normal(75, 25, 120)              # mg
    ax[0].scatter(energy, vitc, color=BLUE, s=22, alpha=.8, edgecolor="w", lw=.4)
    ax[0].set_title("Raw scales differ wildly")
    ax[0].set_xlabel("Energy (kJ)"); ax[0].set_ylabel("Vitamin C (mg)")
    ze = (energy-energy.mean())/energy.std(); zv=(vitc-vitc.mean())/vitc.std()
    ax[1].scatter(ze, zv, color=ACCENT, s=22, alpha=.8, edgecolor="w", lw=.4)
    ax[1].set_title("After standardising (z-scores)")
    ax[1].set_xlabel("Energy (SD units)"); ax[1].set_ylabel("Vitamin C (SD units)")
    ax[1].set_xlim(-3.5,3.5); ax[1].set_ylim(-3.5,3.5)
    fig.tight_layout()
    return savefig(fig, "L02_scaling.png")

def L03_clusters():
    from sklearn.datasets import make_blobs
    X,_ = make_blobs(n_samples=260, centers=[(0,0),(4,4),(5,-1)], cluster_std=[.8,1.0,.7], random_state=3)
    fig, ax = plt.subplots(1,2, figsize=(9.4,4.2))
    ax[0].scatter(X[:,0],X[:,1], color=GREY, s=20, edgecolor="w", lw=.4)
    ax[0].set_title("What we see")
    from sklearn.cluster import KMeans
    lab = KMeans(3, n_init=10, random_state=0).fit_predict(X)
    for k in range(3):
        ax[1].scatter(X[lab==k,0],X[lab==k,1], color=CAT[k], s=20, edgecolor="w", lw=.4)
    ax[1].set_title("What clustering proposes")
    for a in ax: a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.tight_layout()
    return savefig(fig, "L03_clusters.png")

def L03_withinbetween():
    fig, ax = plt.subplots(figsize=(6.6,4.4))
    A = rng.normal((0,0),.6,(30,2)); B = rng.normal((3.4,2.2),.6,(30,2))
    ax.scatter(A[:,0],A[:,1],color=BLUE,s=26,edgecolor="w",lw=.5)
    ax.scatter(B[:,0],B[:,1],color=ACCENT,s=26,edgecolor="w",lw=.5)
    for P,c in [(A,BLUE),(B,ACCENT)]:
        m=P.mean(0); ax.scatter(*m,color=c,marker="X",s=200,edgecolor="k",lw=1.2,zorder=5)
    mA,mB=A.mean(0),B.mean(0)
    ax.annotate("",mB,mA,arrowprops=dict(arrowstyle="<->",color=INK,lw=2))
    ax.text((mA[0]+mB[0])/2,(mA[1]+mB[1])/2+.3,"between",fontweight="bold",color=INK,ha="center")
    ax.plot([mA[0],A[0,0]],[mA[1],A[0,1]],color=BLUE,lw=1.5,ls="--")
    ax.text(A[0,0]-.2,A[0,1],"within",color=BLUE,fontweight="bold",ha="right")
    ax.set_xticks([]);ax.set_yticks([]);ax.grid(False)
    ax.set_title("Good clusters: small within, large between")
    fig.tight_layout()
    return savefig(fig,"L03_withinbetween.png")

def L04_iterations():
    from sklearn.datasets import make_blobs
    X,_ = make_blobs(n_samples=220, centers=[(0,0),(4,3.5),(5,-1)], cluster_std=.8, random_state=1)
    fig, ax = plt.subplots(1,3, figsize=(10.4,3.7))
    C = np.array([[-1,2],[1,-1],[3,0]], float)  # bad init on purpose
    def assign(X,C):
        d=((X[:,None,:]-C[None])**2).sum(-1); return d.argmin(1)
    steps=[(0,"Initialise centres"),(1,"Iteration 1"),(6,"Converged")]
    Ccur=C.copy()
    hist={}
    lab=assign(X,Ccur); hist[0]=(Ccur.copy(),lab)
    for t in range(1,7):
        for k in range(3):
            if (lab==k).any(): Ccur[k]=X[lab==k].mean(0)
        lab=assign(X,Ccur); hist[t]=(Ccur.copy(),lab)
    for a,(t,ttl) in zip(ax,steps):
        Cc,lb=hist[t]
        for k in range(3):
            a.scatter(X[lb==k,0],X[lb==k,1],color=CAT[k],s=14,edgecolor="w",lw=.3)
            a.scatter(*Cc[k],color=CAT[k],marker="X",s=190,edgecolor="k",lw=1.3,zorder=6)
        a.set_title(ttl); a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.suptitle("Lloyd's algorithm: assign → update → repeat", fontsize=14, fontweight="bold", color=INK)
    fig.tight_layout()
    return savefig(fig,"L04_iterations.png")

def L04_elbow():
    from sklearn.datasets import make_blobs
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    X,_ = make_blobs(n_samples=300, centers=4, cluster_std=.9, random_state=5)
    ks=range(1,9); wss=[]; sil=[]
    for k in ks:
        km=KMeans(k,n_init=10,random_state=0).fit(X); wss.append(km.inertia_)
        sil.append(silhouette_score(X,km.labels_) if k>1 else np.nan)
    fig, ax = plt.subplots(1,2, figsize=(9.4,4.0))
    ax[0].plot(list(ks),wss,"o-",color=BLUE,lw=2,ms=7)
    ax[0].scatter([4],[wss[3]],s=180,facecolor="none",edgecolor=ACCENT,lw=2.5,zorder=5)
    ax[0].annotate("elbow ≈ 4",(4,wss[3]),(5,wss[3]+wss[0]*.12),color=ACCENT,fontweight="bold")
    ax[0].set_title("Elbow: within-cluster SS"); ax[0].set_xlabel("k"); ax[0].set_ylabel("WSS")
    ax[1].plot(list(ks)[1:],sil[1:],"o-",color=TEAL,lw=2,ms=7)
    ax[1].scatter([4],[sil[3]],s=180,facecolor="none",edgecolor=ACCENT,lw=2.5,zorder=5)
    ax[1].set_title("Silhouette (higher = better)"); ax[1].set_xlabel("k"); ax[1].set_ylabel("mean silhouette")
    fig.tight_layout()
    return savefig(fig,"L04_elbow.png")

def L04_failure():
    from sklearn.datasets import make_moons
    from sklearn.cluster import KMeans
    X,_ = make_moons(n_samples=300, noise=.06, random_state=0)
    lab=KMeans(2,n_init=10,random_state=0).fit_predict(X)
    fig, ax = plt.subplots(figsize=(6.4,4.2))
    for k in range(2):
        ax.scatter(X[lab==k,0],X[lab==k,1],color=CAT[k],s=20,edgecolor="w",lw=.4)
    ax.set_title("K-means assumes round blobs —\nit splits the moons the wrong way")
    ax.set_xticks([]);ax.set_yticks([]);ax.grid(False)
    fig.tight_layout()
    return savefig(fig,"L04_failure.png")

if __name__ == "__main__":
    outs = [f() for f in [L01_super_vs_unsuper,L01_pipeline,L02_missingness,L02_scaling,
            L03_clusters,L03_withinbetween,L04_iterations,L04_elbow,L04_failure]]
    print("\n".join(outs))
