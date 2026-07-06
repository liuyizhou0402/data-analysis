"""Extra figures for full 60-min pptx lectures 01-04."""
import numpy as np
from slides import _mpl, savefig, CAT, BLUE, ACCENT, TEAL, GOLD, PURPLE, GREY, INK, MUTED
plt = _mpl()
import matplotlib.patches as mp
rng = np.random.default_rng(11)

def L01_venn():
    fig, ax = plt.subplots(figsize=(7.6,5.2))
    circ = [((-.5,.4),BLUE,"Statistics /\nMaths"),((.5,.4),ACCENT,"Computer\nScience"),((0,-.55),TEAL,"Domain\nexpertise")]
    for (x,y),c,t in circ:
        ax.add_patch(plt.Circle((x,y),1.05,fc=c,alpha=.32,ec=c,lw=2))
    ax.text(-.95,.75,"Statistics\n& Maths",ha="center",fontsize=13,fontweight="bold",color=BLUE)
    ax.text(.95,.75,"Computer\nScience",ha="center",fontsize=13,fontweight="bold",color=ACCENT)
    ax.text(0,-1.15,"Domain expertise\n(nutrition)",ha="center",fontsize=13,fontweight="bold",color=TEAL)
    ax.text(0,.62,"ML",ha="center",fontsize=13,fontweight="bold",color=INK)
    ax.text(-.62,-.15,"data\nproc.",ha="center",fontsize=10,color=INK)
    ax.text(.62,-.15,"analysis",ha="center",fontsize=10,color=INK)
    ax.text(0,.05,"Data\nScience",ha="center",fontsize=14,fontweight="bold",color=INK)
    ax.set_xlim(-2,2);ax.set_ylim(-1.9,1.7);ax.set_aspect("equal");ax.axis("off")
    fig.tight_layout(); return savefig(fig,"L01_venn.png")

def L01_reg_vs_class():
    fig,ax=plt.subplots(1,2,figsize=(9.6,4.2))
    x=np.linspace(0,10,60); y=1.5*x+3+rng.normal(0,2.5,60)
    ax[0].scatter(x,y,color=BLUE,s=22,alpha=.8,edgecolor="w",lw=.4)
    ax[0].plot(x,1.5*x+3,color=ACCENT,lw=2.5)
    ax[0].set_title("Regression: predict a number"); ax[0].set_xlabel("fibre intake"); ax[0].set_ylabel("glucose")
    from sklearn.datasets import make_blobs
    X,yl=make_blobs(n_samples=120,centers=[(1,1),(4,4)],cluster_std=1.0,random_state=2)
    ax[1].scatter(X[yl==0,0],X[yl==0,1],color=BLUE,s=24,edgecolor="w",lw=.4,label="healthy")
    ax[1].scatter(X[yl==1,0],X[yl==1,1],color=ACCENT,s=24,edgecolor="w",lw=.4,label="at-risk")
    xx=np.linspace(-2,7,10); ax[1].plot(xx,6.2-xx,color=INK,lw=2,ls="--")
    ax[1].set_title("Classification: predict a label"); ax[1].legend(loc="upper right",fontsize=11)
    ax[1].set_xlabel("BMI (z)"); ax[1].set_ylabel("waist (z)")
    fig.tight_layout(); return savefig(fig,"L01_reg_vs_class.png")

def L01_overfit():
    fig,ax=plt.subplots(figsize=(7.4,4.6))
    x=np.sort(rng.uniform(0,1,22)); y=np.sin(2*np.pi*x)+rng.normal(0,.25,22)
    xg=np.linspace(0,1,200)
    for deg,c,lab,w in [(1,GREY,"underfit (deg 1)",2),(3,TEAL,"good (deg 3)",2.6),(14,ACCENT,"overfit (deg 14)",2)]:
        cf=np.polyfit(x,y,deg); ax.plot(xg,np.polyval(cf,xg),color=c,lw=w,label=lab)
    ax.scatter(x,y,color=INK,s=28,zorder=5,edgecolor="w")
    ax.set_ylim(-2,2);ax.legend(fontsize=11,loc="upper right")
    ax.set_title("Under- vs over-fitting: the central tension"); ax.set_xlabel("x"); ax.set_ylabel("y")
    fig.tight_layout(); return savefig(fig,"L01_overfit.png")

def L02_boxplot():
    fig,ax=plt.subplots(figsize=(7.2,4.4))
    data=[rng.normal(75,18,200)]; data[0]=np.append(data[0],[220,240,5]) # outliers
    bp=ax.boxplot(data,vert=False,widths=.5,patch_artist=True,
                  boxprops=dict(facecolor="#dbe7f0",edgecolor=BLUE,lw=1.6),
                  medianprops=dict(color=ACCENT,lw=2.4),
                  flierprops=dict(marker="o",markerfacecolor=ACCENT,markeredgecolor="none",markersize=7,alpha=.8),
                  whiskerprops=dict(color=BLUE,lw=1.6),capprops=dict(color=BLUE,lw=1.6))
    ax.set_yticks([]); ax.set_xlabel("Vitamin C (mg)")
    ax.set_title("Boxplot flags outliers via the IQR rule")
    ax.annotate("outliers > Q3 + 1.5·IQR",(230,1.28),(150,1.35),color=ACCENT,fontweight="bold",
                arrowprops=dict(arrowstyle="->",color=ACCENT))
    fig.tight_layout(); return savefig(fig,"L02_boxplot.png")

def L02_logtx():
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.0))
    x=rng.lognormal(3,1,400)
    ax[0].hist(x,bins=30,color=BLUE,alpha=.85,edgecolor="w")
    ax[0].set_title("Skewed intake (raw)"); ax[0].set_xlabel("supplement dose")
    ax[1].hist(np.log(x),bins=30,color=TEAL,alpha=.85,edgecolor="w")
    ax[1].set_title("After log transform"); ax[1].set_xlabel("log(dose)")
    fig.tight_layout(); return savefig(fig,"L02_logtx.png")

def L03_distances():
    fig,ax=plt.subplots(figsize=(6.6,4.6))
    a,b=np.array([1,1]),np.array([5,4])
    ax.plot([a[0],b[0]],[a[1],b[1]],color=ACCENT,lw=2.6,label="Euclidean")
    ax.plot([a[0],b[0],b[0]],[a[1],a[1],b[1]],color=BLUE,lw=2.6,ls="--",label="Manhattan")
    ax.scatter(*a,s=120,color=INK,zorder=5); ax.scatter(*b,s=120,color=INK,zorder=5)
    ax.text(a[0]-.1,a[1]-.4,"A",fontsize=15,fontweight="bold"); ax.text(b[0]+.1,b[1]+.1,"B",fontsize=15,fontweight="bold")
    ax.text(2.6,3.0,"√Σ(x−y)²",color=ACCENT,fontweight="bold")
    ax.text(3,.5,"Σ|x−y|",color=BLUE,fontweight="bold")
    ax.set_xlim(0,6.5);ax.set_ylim(0,5.5);ax.legend(fontsize=12,loc="upper left")
    ax.set_title("Two ways to measure distance")
    fig.tight_layout(); return savefig(fig,"L03_distances.png")

def L03_dendro():
    from scipy.cluster.hierarchy import dendrogram, linkage
    from sklearn.datasets import make_blobs
    X,_=make_blobs(n_samples=14,centers=3,cluster_std=.6,random_state=4)
    Z=linkage(X,"ward")
    fig,ax=plt.subplots(figsize=(7.4,4.4))
    dendrogram(Z,ax=ax,color_threshold=.7*Z[:,2].max(),
               above_threshold_color=GREY)
    ax.set_title("A dendrogram: nested groups (preview of L06)")
    ax.set_xlabel("observations"); ax.set_ylabel("merge distance")
    fig.tight_layout(); return savefig(fig,"L03_dendro.png")

def L04_voronoi():
    from sklearn.datasets import make_blobs
    from sklearn.cluster import KMeans
    X,_=make_blobs(n_samples=300,centers=4,cluster_std=1.0,random_state=8)
    km=KMeans(4,n_init=10,random_state=0).fit(X)
    fig,ax=plt.subplots(figsize=(6.6,4.8))
    h=.03; xx,yy=np.meshgrid(np.arange(X[:,0].min()-1,X[:,0].max()+1,h),
                             np.arange(X[:,1].min()-1,X[:,1].max()+1,h))
    Z=km.predict(np.c_[xx.ravel(),yy.ravel()]).reshape(xx.shape)
    from matplotlib.colors import ListedColormap
    ax.imshow(Z,extent=(xx.min(),xx.max(),yy.min(),yy.max()),origin="lower",
              cmap=ListedColormap([ "#e7eef5","#fbe6e0","#e2f1ee","#fbf1dc"]),aspect="auto",alpha=.9)
    for k in range(4):
        ax.scatter(X[km.labels_==k,0],X[km.labels_==k,1],color=CAT[k],s=16,edgecolor="w",lw=.3)
        ax.scatter(*km.cluster_centers_[k],color=CAT[k],marker="X",s=190,edgecolor="k",lw=1.3,zorder=6)
    ax.set_title("K-means carves space into Voronoi cells")
    ax.set_xticks([]);ax.set_yticks([]);ax.grid(False)
    fig.tight_layout(); return savefig(fig,"L04_voronoi.png")

def L04_kmeanspp():
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.2))
    from sklearn.datasets import make_blobs
    X,_=make_blobs(n_samples=240,centers=[(0,0),(6,0),(3,5)],cluster_std=.7,random_state=6)
    # random (clumped) init vs spread k-means++ init
    ax[0].scatter(X[:,0],X[:,1],color=GREY,s=14,edgecolor="w",lw=.3)
    ri=X[rng.choice(len(X),3,replace=False)]
    ax[0].scatter(ri[:,0],ri[:,1],color=ACCENT,marker="X",s=200,edgecolor="k",lw=1.3)
    ax[0].set_title("Random init: can clump together")
    ax[1].scatter(X[:,0],X[:,1],color=GREY,s=14,edgecolor="w",lw=.3)
    pp=np.array([[0,0],[6,0],[3,5]],float)
    ax[1].scatter(pp[:,0],pp[:,1],color=TEAL,marker="X",s=200,edgecolor="k",lw=1.3)
    ax[1].set_title("k-means++: spread apart")
    for a in ax:a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.tight_layout(); return savefig(fig,"L04_kmeanspp.png")

if __name__=="__main__":
    outs=[f() for f in [L01_venn,L01_reg_vs_class,L01_overfit,L02_boxplot,L02_logtx,
          L03_distances,L03_dendro,L04_voronoi,L04_kmeanspp]]
    print("\n".join(outs))
