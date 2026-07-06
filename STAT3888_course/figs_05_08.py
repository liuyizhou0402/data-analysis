# -*- coding: utf-8 -*-
"""Figures for STAT3888 lectures 05-08 (GMM, hierarchical, PCA background, PCA)."""
import numpy as np
from slides import _mpl, savefig, CAT, BLUE, ACCENT, TEAL, GOLD, PURPLE, GREY, INK, MUTED
plt = _mpl()
import matplotlib.patches as mpatch
from matplotlib.patches import Ellipse
rng = np.random.default_rng(21)

# ============================================================ L05  GMM
def L05_soft_vs_hard():
    from sklearn.datasets import make_blobs
    from sklearn.cluster import KMeans
    from sklearn.mixture import GaussianMixture
    X,_=make_blobs(n_samples=350,centers=[(0,0),(3,2.6)],cluster_std=[1.3,1.0],random_state=3)
    fig,ax=plt.subplots(1,2,figsize=(9.6,4.2))
    km=KMeans(2,n_init=10,random_state=0).fit(X)
    for k in range(2): ax[0].scatter(X[km.labels_==k,0],X[km.labels_==k,1],color=CAT[k],s=16,edgecolor="w",lw=.3)
    ax[0].set_title("K-means: hard assignment")
    gm=GaussianMixture(2,random_state=0).fit(X); r=gm.predict_proba(X)[:,0]
    sc=ax[1].scatter(X[:,0],X[:,1],c=r,cmap="coolwarm",s=18,edgecolor="w",lw=.3)
    ax[1].set_title("GMM: soft probabilities")
    for a in ax:a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.colorbar(sc,ax=ax[1],fraction=.046,label="P(cluster 1)")
    fig.tight_layout(); return savefig(fig,"L05_soft_vs_hard.png")

def L05_1d_mixture():
    x=np.linspace(-4,10,500)
    from scipy.stats import norm
    comps=[(0.4,0,1.0,BLUE),(0.6,5,1.4,ACCENT)]
    data=np.concatenate([rng.normal(m,s,int(600*w)) for w,m,s,_ in comps])
    fig,ax=plt.subplots(figsize=(8.2,4.4))
    ax.hist(data,bins=45,density=True,color="#d9e2ec",edgecolor="w")
    mix=np.zeros_like(x)
    for w,m,s,c in comps:
        y=w*norm.pdf(x,m,s); mix+=y
        ax.plot(x,y,color=c,lw=2.4,ls="--",label=f"component μ={m}")
    ax.plot(x,mix,color=INK,lw=3,label="mixture density")
    ax.legend(fontsize=11); ax.set_title("A 1-D Gaussian mixture: sum of weighted bells")
    ax.set_xlabel("x"); ax.set_ylabel("density")
    fig.tight_layout(); return savefig(fig,"L05_1d_mixture.png")

def _ellipse(ax,mean,cov,color,nsig=2):
    vals,vecs=np.linalg.eigh(cov); order=vals.argsort()[::-1]; vals,vecs=vals[order],vecs[:,order]
    ang=np.degrees(np.arctan2(*vecs[:,0][::-1]))
    w,h=2*nsig*np.sqrt(vals)
    e=Ellipse(mean,w,h,angle=ang,fc=color,alpha=.18,ec=color,lw=2.2); ax.add_patch(e)

def L05_ellipses():
    from sklearn.mixture import GaussianMixture
    m1,m2=[0,0],[4,3]
    c1=[[1.6,1.0],[1.0,1.0]]; c2=[[1.0,-0.6],[-0.6,0.8]]
    X=np.vstack([rng.multivariate_normal(m1,c1,180),rng.multivariate_normal(m2,c2,180)])
    gm=GaussianMixture(2,covariance_type="full",random_state=0).fit(X)
    lab=gm.predict(X)
    fig,ax=plt.subplots(figsize=(7.0,4.8))
    for k in range(2):
        ax.scatter(X[lab==k,0],X[lab==k,1],color=CAT[k],s=16,edgecolor="w",lw=.3)
        _ellipse(ax,gm.means_[k],gm.covariances_[k],CAT[k])
        ax.scatter(*gm.means_[k],color=CAT[k],marker="X",s=180,edgecolor="k",lw=1.3,zorder=6)
    ax.set_title("GMM fits elliptical clusters (full covariance)")
    ax.set_xticks([]);ax.set_yticks([]);ax.grid(False)
    fig.tight_layout(); return savefig(fig,"L05_ellipses.png")

def L05_covtypes():
    fig,ax=plt.subplots(1,4,figsize=(11,3.0))
    covs=[("spherical",[[1,0],[0,1]]),("diagonal",[[1.8,0],[0,0.6]]),
          ("tied",[[1.2,0.7],[0.7,1.2]]),("full",[[1.5,-0.9],[-0.9,1.0]])]
    for a,(t,c) in zip(ax,covs):
        _ellipse(a,[0,0],np.array(c,float),BLUE)
        a.set_xlim(-3,3);a.set_ylim(-3,3);a.set_aspect("equal")
        a.set_title(t,fontsize=13); a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.suptitle("Covariance types: from restrictive (spherical) to flexible (full)",
                 fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L05_covtypes.png")

def L05_em():
    from scipy.stats import norm
    fig,ax=plt.subplots(1,3,figsize=(10.4,3.6))
    X=np.concatenate([rng.normal(0,1,120),rng.normal(4,1,120)])
    inits=[([-1,1],"Start (bad guess)"),([-.3,3],"After 1 EM step"),([0,4],"Converged")]
    xg=np.linspace(-4,8,300)
    for a,(mus,ttl) in zip(ax,inits):
        a.hist(X,bins=30,density=True,color="#dbe4ec",edgecolor="w")
        for m,c in zip(mus,[BLUE,ACCENT]):
            a.plot(xg,0.5*norm.pdf(xg,m,1),color=c,lw=2.4)
            a.axvline(m,color=c,ls=":",lw=1.5)
        a.set_title(ttl,fontsize=12); a.set_yticks([])
    fig.suptitle("EM alternates E-step (responsibilities) and M-step (refit)",
                 fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L05_em.png")

def L05_bic():
    from sklearn.datasets import make_blobs
    from sklearn.mixture import GaussianMixture
    X,_=make_blobs(n_samples=400,centers=4,cluster_std=1.0,random_state=5)
    ks=range(1,9); bics=[GaussianMixture(k,random_state=0).fit(X).bic(X) for k in ks]
    fig,ax=plt.subplots(figsize=(7.6,4.2))
    ax.plot(list(ks),bics,"o-",color=BLUE,lw=2,ms=8)
    kb=list(ks)[int(np.argmin(bics))]
    ax.scatter([kb],[min(bics)],s=200,facecolor="none",edgecolor=ACCENT,lw=2.6,zorder=5)
    ax.annotate(f"min BIC at k={kb}",(kb,min(bics)),(kb+.6,min(bics)+ (max(bics)-min(bics))*.2),
                color=ACCENT,fontweight="bold")
    ax.set_title("BIC picks the number of components"); ax.set_xlabel("k"); ax.set_ylabel("BIC (lower better)")
    fig.tight_layout(); return savefig(fig,"L05_bic.png")

def L05_responsibility():
    from sklearn.mixture import GaussianMixture
    X=np.vstack([rng.normal([0,0],.8,(40,2)),rng.normal([3,2],.8,(40,2)),rng.normal([1.5,1],1.2,(20,2))])
    gm=GaussianMixture(2,random_state=0).fit(X[:60]); R=gm.predict_proba(X)
    idx=np.argsort(R[:,0])
    fig,ax=plt.subplots(figsize=(7.8,3.6))
    ax.imshow(R[idx].T,aspect="auto",cmap="coolwarm")
    ax.set_yticks([0,1]);ax.set_yticklabels(["cluster 0","cluster 1"])
    ax.set_xlabel("observations (sorted)"); ax.set_title("Responsibilities: each point is shared across clusters")
    ax.grid(False)
    fig.tight_layout(); return savefig(fig,"L05_responsibility.png")

# ============================================================ L06  Hierarchical
def L06_dendro_big():
    from scipy.cluster.hierarchy import dendrogram, linkage
    from sklearn.datasets import make_blobs
    X,_=make_blobs(n_samples=22,centers=4,cluster_std=.7,random_state=6)
    Z=linkage(X,"ward")
    fig,ax=plt.subplots(figsize=(9.6,4.6))
    dendrogram(Z,ax=ax,color_threshold=.6*Z[:,2].max(),above_threshold_color=GREY)
    ax.axhline(.6*Z[:,2].max(),color=ACCENT,ls="--",lw=2)
    ax.text(1,.6*Z[:,2].max()+.2,"cut here → 4 clusters",color=ACCENT,fontweight="bold")
    ax.set_title("Dendrogram: read clusters at any height"); ax.set_xlabel("observations"); ax.set_ylabel("merge distance")
    fig.tight_layout(); return savefig(fig,"L06_dendro_big.png")

def L06_agglo_steps():
    fig,ax=plt.subplots(1,4,figsize=(11,3.0))
    pts=np.array([[0,0],[.6,.3],[3,2.5],[3.5,2.2],[1.6,3.2]])
    groups=[[[0],[1],[2],[3],[4]],[[0,1],[2],[3],[4]],[[0,1],[2,3],[4]],[[0,1,4],[2,3]]]
    for a,g in zip(ax,groups):
        for gi,members in enumerate(g):
            P=pts[members]
            a.scatter(P[:,0],P[:,1],color=CAT[gi%6],s=70,edgecolor="w",lw=.5,zorder=3)
            if len(members)>1:
                c=P.mean(0)
                for p in P: a.plot([c[0],p[0]],[c[1],p[1]],color=CAT[gi%6],lw=1.4,alpha=.6)
        a.set_title(f"{len(g)} clusters",fontsize=12)
        a.set_xlim(-.6,4.2);a.set_ylim(-.6,4);a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.suptitle("Agglomerative: start with singletons, merge the closest pair each step",
                 fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L06_agglo_steps.png")

def L06_linkages():
    from scipy.cluster.hierarchy import dendrogram, linkage
    from sklearn.datasets import make_blobs
    X,_=make_blobs(n_samples=30,centers=3,cluster_std=1.0,random_state=8)
    fig,ax=plt.subplots(1,4,figsize=(11,3.2))
    for a,m in zip(ax,["single","complete","average","ward"]):
        Z=linkage(X,m); dendrogram(Z,ax=a,no_labels=True,color_threshold=0,above_threshold_color=BLUE)
        a.set_title(m,fontsize=13); a.set_yticks([])
    fig.suptitle("Linkage choice reshapes the tree",fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L06_linkages.png")

def L06_linkage_defs():
    fig,ax=plt.subplots(1,3,figsize=(10,3.4))
    A=np.array([[0,0],[.4,.6],[.8,.1]]); B=np.array([[3,2],[3.4,2.5],[2.7,2.2]])
    defs=[("Single: nearest pair",lambda:(A[2],B[2])),
          ("Complete: farthest pair",lambda:(A[0],B[1])),
          ("Average: mean of all pairs",None)]
    for a,(t,f) in zip(ax,defs):
        a.scatter(A[:,0],A[:,1],color=BLUE,s=70,edgecolor="w",zorder=3)
        a.scatter(B[:,0],B[:,1],color=ACCENT,s=70,edgecolor="w",zorder=3)
        if f:
            p,q=f(); a.plot([p[0],q[0]],[p[1],q[1]],color=INK,lw=2.2,ls="--")
        else:
            for p in A:
                for q in B: a.plot([p[0],q[0]],[p[1],q[1]],color=GREY,lw=.7,alpha=.6)
        a.set_title(t,fontsize=12); a.set_xticks([]);a.set_yticks([]);a.grid(False)
        a.set_xlim(-.6,4);a.set_ylim(-.6,3.2)
    fig.tight_layout(); return savefig(fig,"L06_linkage_defs.png")

def L06_distmat():
    from sklearn.datasets import make_blobs
    from scipy.spatial.distance import squareform, pdist
    X,y=make_blobs(n_samples=18,centers=3,cluster_std=.5,random_state=2)
    o=np.argsort(y); D=squareform(pdist(X[o]))
    fig,ax=plt.subplots(figsize=(5.6,4.8))
    im=ax.imshow(D,cmap="viridis_r"); ax.set_title("Distance matrix (block structure = clusters)")
    ax.set_xticks([]);ax.set_yticks([]);ax.grid(False); fig.colorbar(im,fraction=.046)
    fig.tight_layout(); return savefig(fig,"L06_distmat.png")

def L06_chaining():
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.datasets import make_moons
    X,_=make_moons(n_samples=260,noise=.05,random_state=0)
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.0))
    for a,m in zip(ax,["single","ward"]):
        lab=AgglomerativeClustering(2,linkage=m).fit_predict(X)
        for k in range(2): a.scatter(X[lab==k,0],X[lab==k,1],color=CAT[k],s=16,edgecolor="w",lw=.3)
        a.set_title(f"{m} linkage"); a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.suptitle("Single linkage follows shapes (chaining); Ward prefers compact blobs",
                 fontsize=12.5,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L06_chaining.png")

# ============================================================ L07  PCA background
def L07_variance():
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.2))
    low=rng.normal(0,.4,150); ax[0].scatter(low,rng.normal(0,.4,150),color=BLUE,s=16,alpha=.7)
    ax[0].set_title("Low variance");
    hi=rng.normal(0,1.6,150); ax[1].scatter(hi,rng.normal(0,1.6,150),color=ACCENT,s=16,alpha=.7)
    ax[1].set_title("High variance")
    for a in ax:a.set_xlim(-5,5);a.set_ylim(-5,5);a.set_xticks([]);a.set_yticks([])
    fig.suptitle("Variance measures spread — PCA hunts directions of maximum spread",
                 fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L07_variance.png")

def L07_covariance():
    fig,ax=plt.subplots(1,3,figsize=(10.2,3.6))
    for a,(r,t) in zip(ax,[(-.85,"negative cov"),(0.0,"~zero cov"),(0.9,"positive cov")]):
        cov=[[1,r],[r,1]]; P=rng.multivariate_normal([0,0],cov,200)
        a.scatter(P[:,0],P[:,1],color=BLUE,s=14,alpha=.7)
        a.set_title(t,fontsize=12); a.set_xlim(-3.5,3.5);a.set_ylim(-3.5,3.5)
        a.set_xticks([]);a.set_yticks([])
    fig.suptitle("Covariance encodes how two variables move together",
                 fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L07_covariance.png")

def L07_eigen():
    cov=np.array([[2.0,1.2],[1.2,1.0]]); P=rng.multivariate_normal([0,0],cov,300)
    vals,vecs=np.linalg.eigh(np.cov(P.T)); order=vals.argsort()[::-1]; vals,vecs=vals[order],vecs[:,order]
    fig,ax=plt.subplots(figsize=(6.4,5.0))
    ax.scatter(P[:,0],P[:,1],color=GREY,s=14,alpha=.6)
    _ellipse(ax,[0,0],np.cov(P.T),BLUE)
    for i,(val,c,lab) in enumerate(zip(vals,[ACCENT,TEAL],["PC1","PC2"])):
        v=vecs[:,i]*np.sqrt(val)*2.2
        ax.annotate("",v,[0,0],arrowprops=dict(arrowstyle="-|>",color=c,lw=3))
        ax.text(v[0]*1.1,v[1]*1.1,lab,color=c,fontsize=15,fontweight="bold")
    ax.set_aspect("equal");ax.set_xticks([]);ax.set_yticks([]);ax.grid(False)
    ax.set_title("Eigenvectors of the covariance = principal axes")
    fig.tight_layout(); return savefig(fig,"L07_eigen.png")

def L07_projection():
    cov=np.array([[2.2,1.5],[1.5,1.4]]); P=rng.multivariate_normal([0,0],cov,120)
    vals,vecs=np.linalg.eigh(np.cov(P.T)); v=vecs[:,vals.argmax()]
    proj=(P@v)[:,None]*v
    fig,ax=plt.subplots(figsize=(6.4,5.0))
    L=v*4; ax.plot([-L[0],L[0]],[-L[1],L[1]],color=ACCENT,lw=2.4,zorder=1,label="PC1 direction")
    ax.scatter(P[:,0],P[:,1],color=BLUE,s=22,zorder=3,label="data")
    ax.scatter(proj[:,0],proj[:,1],color=TEAL,s=18,zorder=3,label="projection")
    for p,q in zip(P,proj): ax.plot([p[0],q[0]],[p[1],q[1]],color=GREY,lw=.6,alpha=.6)
    ax.legend(fontsize=11,loc="upper left");ax.set_aspect("equal")
    ax.set_xticks([]);ax.set_yticks([]);ax.grid(False)
    ax.set_title("PCA projects data onto the max-variance line")
    fig.tight_layout(); return savefig(fig,"L07_projection.png")

def L07_standardize():
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.2))
    x=rng.normal(0,1,200)*3; y=x*0.3+rng.normal(0,1,200)
    ax[0].scatter(x*30,y,color=BLUE,s=16,alpha=.7); ax[0].set_title("Before: variable 1 dominates")
    ax[0].set_xlabel("energy (kJ)");ax[0].set_ylabel("fibre (g)")
    ax[1].scatter((x-x.mean())/x.std(),(y-y.mean())/y.std(),color=ACCENT,s=16,alpha=.7)
    ax[1].set_title("After standardising"); ax[1].set_xlabel("z1");ax[1].set_ylabel("z2")
    ax[1].set_xlim(-4,4);ax[1].set_ylim(-4,4)
    fig.tight_layout(); return savefig(fig,"L07_standardize.png")

# ============================================================ L08  PCA
def _iris():
    from sklearn.datasets import load_iris
    d=load_iris(); return d.data, d.target, d.feature_names, d.target_names

def L08_scree():
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    X,y,fn,tn=_iris(); Z=StandardScaler().fit_transform(X)
    p=PCA().fit(Z); ev=p.explained_variance_ratio_
    fig,ax=plt.subplots(figsize=(7.6,4.2))
    ax.bar(range(1,len(ev)+1),ev,color=BLUE,alpha=.85,label="individual")
    ax.plot(range(1,len(ev)+1),np.cumsum(ev),"o-",color=ACCENT,lw=2,label="cumulative")
    ax.axhline(.9,color=GREY,ls="--"); ax.text(3.2,.92,"90%",color=GREY)
    ax.set_xlabel("principal component"); ax.set_ylabel("proportion of variance")
    ax.set_title("Scree plot: how much variance each PC captures"); ax.legend(fontsize=11)
    fig.tight_layout(); return savefig(fig,"L08_scree.png")

def L08_scores():
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    X,y,fn,tn=_iris(); Z=StandardScaler().fit_transform(X); S=PCA(2).fit_transform(Z)
    fig,ax=plt.subplots(figsize=(7.2,4.6))
    for k,name in enumerate(tn):
        ax.scatter(S[y==k,0],S[y==k,1],color=CAT[k],s=26,edgecolor="w",lw=.4,label=name)
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.legend(fontsize=11)
    ax.set_title("PCA scores: 4-D data shown in 2-D, groups separate")
    fig.tight_layout(); return savefig(fig,"L08_scores.png")

def L08_biplot():
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    X,y,fn,tn=_iris(); Z=StandardScaler().fit_transform(X); p=PCA(2).fit(Z); S=p.transform(Z)
    fig,ax=plt.subplots(figsize=(7.4,5.0))
    ax.scatter(S[:,0],S[:,1],color=GREY,s=16,alpha=.5)
    load=p.components_.T*3.2
    labs=["sepal len","sepal wid","petal len","petal wid"]
    for i,lab in enumerate(labs):
        ax.annotate("",load[i],[0,0],arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=2))
        ax.text(load[i,0]*1.12,load[i,1]*1.12,lab,color=ACCENT,fontsize=11,fontweight="bold",ha="center")
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_title("Biplot: scores + variable loadings")
    fig.tight_layout(); return savefig(fig,"L08_biplot.png")

def L08_loadings():
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    X,y,fn,tn=_iris(); Z=StandardScaler().fit_transform(X); p=PCA().fit(Z)
    fig,ax=plt.subplots(figsize=(7.2,3.8))
    L=p.components_[:3]
    im=ax.imshow(L,cmap="coolwarm",vmin=-.8,vmax=.8,aspect="auto")
    ax.set_xticks(range(4));ax.set_xticklabels(["sepal L","sepal W","petal L","petal W"])
    ax.set_yticks(range(3));ax.set_yticklabels(["PC1","PC2","PC3"])
    for i in range(3):
        for j in range(4): ax.text(j,i,f"{L[i,j]:.2f}",ha="center",va="center",fontsize=10)
    ax.set_title("Loadings: how variables build each PC"); ax.grid(False); fig.colorbar(im,fraction=.046)
    fig.tight_layout(); return savefig(fig,"L08_loadings.png")

def L08_reconstruction():
    from sklearn.decomposition import PCA
    from sklearn.datasets import load_digits
    d=load_digits(); img=d.data[7]
    fig,ax=plt.subplots(1,5,figsize=(11,2.6))
    ax[0].imshow(img.reshape(8,8),cmap="gray_r"); ax[0].set_title("original\n(64 dims)",fontsize=11)
    for a,k in zip(ax[1:],[2,5,10,20]):
        p=PCA(k).fit(d.data); rec=p.inverse_transform(p.transform(img[None]))
        a.imshow(rec.reshape(8,8),cmap="gray_r"); a.set_title(f"{k} PCs",fontsize=11)
    for a in ax:a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.suptitle("PCA as compression: reconstruct a digit from few components",
                 fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L08_reconstruction.png")

def L08_maxvar():
    cov=np.array([[2.5,1.6],[1.6,1.4]]); P=rng.multivariate_normal([0,0],cov,200)
    angs=np.linspace(0,np.pi,60); vars=[np.var(P@np.array([np.cos(a),np.sin(a)])) for a in angs]
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.2))
    ax[0].scatter(P[:,0],P[:,1],color=GREY,s=14,alpha=.6)
    best=angs[int(np.argmax(vars))]; v=np.array([np.cos(best),np.sin(best)])*4
    ax[0].plot([-v[0],v[0]],[-v[1],v[1]],color=ACCENT,lw=2.6)
    ax[0].set_aspect("equal");ax[0].set_xticks([]);ax[0].set_yticks([]);ax[0].grid(False)
    ax[0].set_title("PC1 = direction maximising variance")
    ax[1].plot(np.degrees(angs),vars,color=BLUE,lw=2.4)
    ax[1].axvline(np.degrees(best),color=ACCENT,ls="--",lw=2)
    ax[1].set_xlabel("projection angle (°)");ax[1].set_ylabel("variance of projection")
    ax[1].set_title("Variance vs direction")
    fig.tight_layout(); return savefig(fig,"L08_maxvar.png")

ALL = [L05_soft_vs_hard,L05_1d_mixture,L05_ellipses,L05_covtypes,L05_em,L05_bic,L05_responsibility,
       L06_dendro_big,L06_agglo_steps,L06_linkages,L06_linkage_defs,L06_distmat,L06_chaining,
       L07_variance,L07_covariance,L07_eigen,L07_projection,L07_standardize,
       L08_scree,L08_scores,L08_biplot,L08_loadings,L08_reconstruction,L08_maxvar]
if __name__=="__main__":
    print("\n".join(f() for f in ALL))
