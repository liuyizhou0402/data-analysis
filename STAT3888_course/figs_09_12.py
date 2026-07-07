# -*- coding: utf-8 -*-
"""Figures for STAT3888 lectures 09-12 (dim reduction, supervised intro, logistic, penalised)."""
import numpy as np
from slides import _mpl, savefig, CAT, BLUE, ACCENT, TEAL, GOLD, PURPLE, GREY, INK, MUTED
plt = _mpl()
rng = np.random.default_rng(31)

# ============================================================ L09  Dimension reduction
def L09_pca_vs_tsne():
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    d=load_digits(); X,y=d.data,d.target
    fig,ax=plt.subplots(1,2,figsize=(10.2,4.4))
    P=PCA(2).fit_transform(X)
    ax[0].scatter(P[:,0],P[:,1],c=y,cmap="tab10",s=10,alpha=.7)
    ax[0].set_title("PCA (linear): classes overlap")
    T=TSNE(2,perplexity=30,init="pca",random_state=0).fit_transform(X)
    sc=ax[1].scatter(T[:,0],T[:,1],c=y,cmap="tab10",s=10,alpha=.7)
    ax[1].set_title("t-SNE (non-linear): classes separate")
    for a in ax:a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.suptitle("Digits (64-D) reduced to 2-D",fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L09_pca_vs_tsne.png")

def L09_manifold():
    from sklearn.datasets import make_swiss_roll
    X,c=make_swiss_roll(n_samples=1200,noise=.05,random_state=0)
    fig=plt.figure(figsize=(9.6,4.2))
    ax=fig.add_subplot(1,2,1,projection="3d")
    ax.scatter(X[:,0],X[:,1],X[:,2],c=c,cmap="Spectral",s=8)
    ax.set_title("Data lies on a curved 2-D sheet in 3-D"); ax.set_xticks([]);ax.set_yticks([]);ax.set_zticks([])
    ax2=fig.add_subplot(1,2,2)
    ax2.scatter(c,X[:,1],c=c,cmap="Spectral",s=8)
    ax2.set_title("Unrolled: the true 2-D structure"); ax2.set_xticks([]);ax2.set_yticks([]);ax2.grid(False)
    fig.tight_layout(); return savefig(fig,"L09_manifold.png")

def L09_mds():
    # cities-like: distances preserved in 2D
    pts=np.array([[0,0],[3,1],[1,3],[4,4],[2,-2]],float)
    from scipy.spatial.distance import pdist, squareform
    D=squareform(pdist(pts))
    from sklearn.manifold import MDS
    emb=MDS(2,dissimilarity="precomputed",random_state=0,normalized_stress="auto").fit_transform(D)
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.2))
    names=["A","B","C","D","E"]
    ax[0].scatter(pts[:,0],pts[:,1],color=BLUE,s=120,zorder=3)
    for p,nm in zip(pts,names):ax[0].text(p[0]+.1,p[1]+.1,nm,fontsize=13,fontweight="bold")
    ax[0].set_title("Original positions")
    ax[1].scatter(emb[:,0],emb[:,1],color=ACCENT,s=120,zorder=3)
    for p,nm in zip(emb,names):ax[1].text(p[0]+.1,p[1]+.1,nm,fontsize=13,fontweight="bold")
    ax[1].set_title("MDS reconstruction from distances only")
    for a in ax:a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.tight_layout(); return savefig(fig,"L09_mds.png")

def L09_perplexity():
    from sklearn.datasets import make_blobs
    from sklearn.manifold import TSNE
    X,y=make_blobs(n_samples=300,centers=3,cluster_std=1.0,random_state=1)
    fig,ax=plt.subplots(1,3,figsize=(10.8,3.6))
    for a,pp in zip(ax,[5,30,100]):
        T=TSNE(2,perplexity=pp,init="pca",random_state=0).fit_transform(X)
        a.scatter(T[:,0],T[:,1],c=y,cmap="tab10",s=12,alpha=.8)
        a.set_title(f"perplexity = {pp}"); a.set_xticks([]);a.set_yticks([]);a.grid(False)
    fig.suptitle("t-SNE is sensitive to perplexity — always try several",
                 fontsize=13,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L09_perplexity.png")

# ============================================================ L10  Supervised intro
def L10_train_test():
    fig,ax=plt.subplots(figsize=(9.4,2.4))
    ax.add_patch(plt.Rectangle((0,0),7,1,fc=BLUE,alpha=.85))
    ax.add_patch(plt.Rectangle((7,0),3,1,fc=ACCENT,alpha=.85))
    ax.text(3.5,.5,"TRAINING (fit the model)",ha="center",va="center",color="white",fontsize=14,fontweight="bold")
    ax.text(8.5,.5,"TEST\n(evaluate)",ha="center",va="center",color="white",fontsize=12,fontweight="bold")
    ax.set_xlim(0,10);ax.set_ylim(0,1);ax.axis("off")
    ax.set_title("Split your data — never test on what you trained on",fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L10_train_test.png")

def L10_bias_variance():
    x=np.linspace(0,10,100)
    bias=np.exp(-x/2.5)*3+.3; var=np.exp((x-10)/3.0)*3+.3; tot=bias+var+.4
    fig,ax=plt.subplots(figsize=(7.8,4.6))
    ax.plot(x,bias,color=BLUE,lw=2.6,label="bias²")
    ax.plot(x,var,color=ACCENT,lw=2.6,label="variance")
    ax.plot(x,tot,color=INK,lw=3,label="total error")
    k=x[np.argmin(tot)]; ax.axvline(k,color=TEAL,ls="--",lw=2)
    ax.text(k+.2,tot.max()*.8,"sweet\nspot",color=TEAL,fontweight="bold")
    ax.set_xlabel("model complexity →"); ax.set_ylabel("error"); ax.legend(fontsize=11)
    ax.set_title("The bias–variance trade-off"); ax.set_yticks([])
    fig.tight_layout(); return savefig(fig,"L10_bias_variance.png")

def L10_cv():
    fig,ax=plt.subplots(figsize=(9.2,3.6))
    K=5
    for i in range(K):
        for j in range(K):
            c=ACCENT if j==i else BLUE
            ax.add_patch(plt.Rectangle((j,K-1-i),.95,.95,fc=c,alpha=.85))
        ax.text(-.3,K-1-i+.45,f"Fold {i+1}",ha="right",va="center",fontsize=11)
    ax.text(2.5,K+.3,"each row: one fold held out for validation (red)",ha="center",fontsize=11,color=INK)
    ax.set_xlim(-1.6,K);ax.set_ylim(0,K+.7);ax.axis("off")
    ax.set_title("5-fold cross-validation",fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L10_cv.png")

def L10_complexity_fit():
    xs=np.sort(rng.uniform(0,1,20)); ys=np.sin(2*np.pi*xs)+rng.normal(0,.25,20)
    xg=np.linspace(0,1,200)
    fig,ax=plt.subplots(1,3,figsize=(10.8,3.6))
    for a,(deg,t) in zip(ax,[(1,"Underfit (high bias)"),(3,"Good fit"),(15,"Overfit (high variance)")]):
        cf=np.polyfit(xs,ys,deg); a.plot(xg,np.polyval(cf,xg),color=ACCENT,lw=2.4)
        a.scatter(xs,ys,color=INK,s=24,zorder=5); a.set_ylim(-2,2)
        a.set_title(t,fontsize=12); a.set_xticks([]);a.set_yticks([])
    fig.tight_layout(); return savefig(fig,"L10_complexity_fit.png")

# ============================================================ L11  Logistic regression
def L11_sigmoid():
    x=np.linspace(-8,8,200); s=1/(1+np.exp(-x))
    fig,ax=plt.subplots(figsize=(7.8,4.4))
    ax.plot(x,s,color=ACCENT,lw=3)
    ax.axhline(.5,color=GREY,ls="--"); ax.axvline(0,color=GREY,ls="--")
    ax.text(2,.55,"decision threshold 0.5",color=MUTED,fontsize=11)
    ax.set_xlabel("linear predictor  η = β₀ + β₁x"); ax.set_ylabel("P(Y = 1)")
    ax.set_title("The logistic (sigmoid) function squashes η into (0,1)")
    fig.tight_layout(); return savefig(fig,"L11_sigmoid.png")

def L11_linear_vs_logistic():
    x=np.linspace(0,10,80); p=1/(1+np.exp(-(x-5))); y=(rng.uniform(size=80)<p).astype(float)
    fig,ax=plt.subplots(1,2,figsize=(9.6,4.2))
    ax[0].scatter(x,y,color=BLUE,s=22,alpha=.7)
    cf=np.polyfit(x,y,1); ax[0].plot(x,np.polyval(cf,x),color=ACCENT,lw=2.4)
    ax[0].axhline(0,color=GREY,lw=.8);ax[0].axhline(1,color=GREY,lw=.8)
    ax[0].set_title("Linear regression: predicts <0 and >1 (wrong)")
    ax[1].scatter(x,y,color=BLUE,s=22,alpha=.7)
    xg=np.linspace(0,10,200); ax[1].plot(xg,1/(1+np.exp(-(xg-5))),color=ACCENT,lw=2.6)
    ax[1].set_title("Logistic regression: a valid probability")
    for a in ax:a.set_xlabel("predictor x");a.set_ylabel("Y / P(Y=1)")
    fig.tight_layout(); return savefig(fig,"L11_linear_vs_logistic.png")

def L11_boundary():
    from sklearn.datasets import make_blobs
    from sklearn.linear_model import LogisticRegression
    X,y=make_blobs(n_samples=200,centers=[(1,1),(4,4)],cluster_std=1.1,random_state=3)
    clf=LogisticRegression().fit(X,y)
    fig,ax=plt.subplots(figsize=(6.8,4.8))
    h=.03; xx,yy=np.meshgrid(np.arange(X[:,0].min()-1,X[:,0].max()+1,h),
                             np.arange(X[:,1].min()-1,X[:,1].max()+1,h))
    Z=clf.predict_proba(np.c_[xx.ravel(),yy.ravel()])[:,1].reshape(xx.shape)
    cf=ax.contourf(xx,yy,Z,levels=12,cmap="coolwarm",alpha=.6)
    ax.contour(xx,yy,Z,levels=[.5],colors=[INK],linewidths=2.4)
    for k in range(2):ax.scatter(X[y==k,0],X[y==k,1],color=CAT[k],s=22,edgecolor="w",lw=.4)
    ax.set_title("Decision boundary = where P(Y=1) = 0.5")
    ax.set_xticks([]);ax.set_yticks([]);ax.grid(False)
    fig.colorbar(cf,fraction=.046,label="P(Y=1)")
    fig.tight_layout(); return savefig(fig,"L11_boundary.png")

def L11_odds():
    x=np.linspace(-4,4,100); p=1/(1+np.exp(-x))
    fig,ax=plt.subplots(1,2,figsize=(9.4,4.0))
    ax[0].plot(p,x,color=BLUE,lw=2.6)
    ax[0].set_xlabel("probability p"); ax[0].set_ylabel("log-odds  log(p/(1−p))")
    ax[0].set_title("The logit link is linear in the predictors")
    odds=p/(1-p); ax[1].plot(x,odds,color=ACCENT,lw=2.6)
    ax[1].set_xlabel("log-odds η"); ax[1].set_ylabel("odds  p/(1−p)")
    ax[1].set_title("A unit rise in x multiplies the odds by e^β")
    fig.tight_layout(); return savefig(fig,"L11_odds.png")

def L11_roc():
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_curve, auc
    X,y=make_classification(n_samples=400,n_features=6,n_informative=3,random_state=2)
    from sklearn.model_selection import train_test_split
    Xtr,Xte,ytr,yte=train_test_split(X,y,random_state=0)
    clf=LogisticRegression().fit(Xtr,ytr); pr=clf.predict_proba(Xte)[:,1]
    fpr,tpr,_=roc_curve(yte,pr); a=auc(fpr,tpr)
    fig,ax=plt.subplots(figsize=(5.8,4.8))
    ax.plot(fpr,tpr,color=ACCENT,lw=2.8,label=f"AUC = {a:.2f}")
    ax.plot([0,1],[0,1],color=GREY,ls="--")
    ax.set_xlabel("false positive rate");ax.set_ylabel("true positive rate")
    ax.set_title("ROC curve"); ax.legend(fontsize=12,loc="lower right")
    fig.tight_layout(); return savefig(fig,"L11_roc.png")

# ============================================================ L12  Penalised logistic
def L12_l1_l2_geometry():
    fig,ax=plt.subplots(1,2,figsize=(9.6,4.6))
    th=np.linspace(0,2*np.pi,100)
    for a,(t,shape) in zip(ax,[("Ridge (L2): circle","circle"),("Lasso (L1): diamond","diamond")]):
        # contours of loss
        b1,b2=np.meshgrid(np.linspace(-1,3,200),np.linspace(-1,3,200))
        loss=(b1-2)**2+ .6*(b2-1.5)**2 + .4*(b1-2)*(b2-1.5)
        a.contour(b1,b2,loss,levels=8,colors=[BLUE],linewidths=.8,alpha=.6)
        if shape=="circle":
            a.plot(np.cos(th),np.sin(th),color=ACCENT,lw=2.6)
        else:
            a.plot([1,0,-1,0,1],[0,1,0,-1,0],color=ACCENT,lw=2.6)
        a.scatter([2],[1.5],color=INK,s=60,zorder=5); a.text(2.1,1.5,"OLS",fontsize=11)
        # solution point (approx)
        if shape=="diamond":
            a.scatter([0],[1],color=TEAL,s=110,zorder=6); a.text(.05,1.15,"sparse!",color=TEAL,fontweight="bold")
        else:
            a.scatter([.55],[.83],color=TEAL,s=110,zorder=6)
        a.set_title(t,fontsize=12); a.set_xlabel("β₁");a.set_ylabel("β₂")
        a.set_xlim(-1.3,3);a.set_ylim(-1.3,3);a.set_aspect("equal")
    fig.suptitle("Why lasso zeros coefficients: the diamond has corners on the axes",
                 fontsize=12.5,fontweight="bold",color=INK)
    fig.tight_layout(); return savefig(fig,"L12_l1_l2_geometry.png")

def L12_paths():
    from sklearn.linear_model import lasso_path, ridge_regression
    from sklearn.datasets import make_regression
    X,y=make_regression(n_samples=100,n_features=8,n_informative=4,noise=10,random_state=1)
    X=(X-X.mean(0))/X.std(0)
    alphas,coefs,_=lasso_path(X,y,n_alphas=60)
    fig,ax=plt.subplots(1,2,figsize=(9.8,4.2))
    for i in range(coefs.shape[0]):
        ax[0].plot(np.log10(alphas),coefs[i],lw=2,color=CAT[i%6])
    ax[0].set_xlabel("log10(λ)");ax[0].set_ylabel("coefficient")
    ax[0].set_title("Lasso path: coefficients shrink to exactly 0")
    ax[0].invert_xaxis(); ax[0].axhline(0,color=GREY,lw=.8)
    # ridge path
    from sklearn.linear_model import Ridge
    las=np.logspace(-2,3,60); rc=np.array([Ridge(alpha=a).fit(X,y).coef_ for a in las])
    for i in range(rc.shape[1]):
        ax[1].plot(np.log10(las),rc[:,i],lw=2,color=CAT[i%6])
    ax[1].set_xlabel("log10(λ)");ax[1].set_ylabel("coefficient")
    ax[1].set_title("Ridge path: coefficients shrink but stay non-zero")
    ax[1].axhline(0,color=GREY,lw=.8)
    fig.tight_layout(); return savefig(fig,"L12_paths.png")

def L12_cv_lambda():
    from sklearn.linear_model import LogisticRegressionCV
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    X,y=make_classification(n_samples=300,n_features=20,n_informative=5,random_state=3)
    X=(X-X.mean(0))/X.std(0)
    Cs=np.logspace(-3,2,25); err=[]
    for C in Cs:
        sc=cross_val_score(LogisticRegression(penalty="l1",solver="liblinear",C=C),X,y,cv=5)
        err.append(1-sc.mean())
    fig,ax=plt.subplots(figsize=(7.6,4.2))
    lam=np.log10(1/Cs)
    ax.plot(lam,err,"o-",color=BLUE,lw=2,ms=6)
    best=int(np.argmin(err)); ax.axvline(lam[best],color=ACCENT,ls="--",lw=2)
    ax.text(lam[best]+.1,max(err)*.9,"best λ (min CV error)",color=ACCENT,fontweight="bold")
    ax.set_xlabel("log10(λ)  →  more penalty"); ax.set_ylabel("cross-validated error")
    ax.set_title("Choose λ by cross-validation")
    fig.tight_layout(); return savefig(fig,"L12_cv_lambda.png")

def L12_bias_var_lambda():
    lam=np.linspace(0,10,100)
    var=np.exp(-lam/2.5)*3+.3; bias=(lam/10)**1.5*3+.3; tot=var+bias+.3
    fig,ax=plt.subplots(figsize=(7.6,4.2))
    ax.plot(lam,var,color=ACCENT,lw=2.4,label="variance")
    ax.plot(lam,bias,color=BLUE,lw=2.4,label="bias²")
    ax.plot(lam,tot,color=INK,lw=3,label="test error")
    k=lam[np.argmin(tot)];ax.axvline(k,color=TEAL,ls="--",lw=2)
    ax.set_xlabel("penalty λ →");ax.set_ylabel("error");ax.legend(fontsize=11);ax.set_yticks([])
    ax.set_title("Regularisation trades a little bias for much less variance")
    fig.tight_layout(); return savefig(fig,"L12_bias_var_lambda.png")

ALL=[L09_pca_vs_tsne,L09_manifold,L09_mds,L09_perplexity,
     L10_train_test,L10_bias_variance,L10_cv,L10_complexity_fit,
     L11_sigmoid,L11_linear_vs_logistic,L11_boundary,L11_odds,L11_roc,
     L12_l1_l2_geometry,L12_paths,L12_cv_lambda,L12_bias_var_lambda]
if __name__=="__main__":
    print("\n".join(f() for f in ALL))
