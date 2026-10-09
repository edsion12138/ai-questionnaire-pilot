#!/usr/bin/env python3
"""Reproducible complete-case psychometric starter pipeline.

Input:
- CSV item data
- JSON config with item -> dimension mapping and valid scale range

Performs:
- item descriptives using available valid responses
- complete-case audit
- Cronbach alpha and omega by dimension
- KMO/Bartlett
- parallel analysis
- PAF + Oblimin EFA
- Fornell-style score correlations and HTMT on complete cases

CFA is deliberately not hardwired here because estimator choice should match the
actual data type and software available. The accompanying skill requires CFA and
recommends ordinal estimators for human Likert data.
"""

import argparse, csv, json, math
import numpy as np
from scipy.stats import pearsonr, skew, kurtosis
from sklearn.decomposition import FactorAnalysis
from statsmodels.multivariate.factor import Factor


def alpha(X):
    X=np.asarray(X,float); k=X.shape[1]
    if k < 2: return float("nan")
    return float(k/(k-1)*(1-np.var(X,axis=0,ddof=1).sum()/np.var(X.sum(axis=1),ddof=1)))


def omega_onefactor(X):
    X=np.asarray(X,float)
    Z=(X-X.mean(axis=0))/X.std(axis=0,ddof=1)
    fa=FactorAnalysis(n_components=1,random_state=0).fit(Z)
    lam=fa.components_[0].copy()
    if lam.sum()<0: lam=-lam
    return float((lam.sum()**2)/((lam.sum()**2)+fa.noise_variance_.sum()))


def kmo_bartlett(X):
    R=np.corrcoef(X,rowvar=False); p=R.shape[0]; n=X.shape[0]
    inv=np.linalg.inv(R); P=np.zeros_like(R)
    for i in range(p):
        for j in range(p):
            if i!=j: P[i,j]=-inv[i,j]/math.sqrt(inv[i,i]*inv[j,j])
    inds=np.triu_indices(p,1)
    kmo=float(np.sum(R[inds]**2)/(np.sum(R[inds]**2)+np.sum(P[inds]**2)))
    det=np.linalg.det(R)
    bart=float(-(n-1-(2*p+5)/6)*math.log(det)); df=p*(p-1)//2
    return kmo,bart,df


def parallel_analysis(X,iters=500,seed=20261009):
    n,p=X.shape
    eig=np.linalg.eigvalsh(np.corrcoef(X,rowvar=False))[::-1]
    rng=np.random.default_rng(seed); rand=np.empty((iters,p))
    for b in range(iters):
        Z=rng.normal(size=(n,p)); rand[b]=np.linalg.eigvalsh(np.corrcoef(Z,rowvar=False))[::-1]
    q95=np.quantile(rand,.95,axis=0)
    return eig,q95,int(np.sum(eig>q95))


def htmt(X, groups, m):
    R=np.corrcoef(X,rowvar=False); H=np.eye(m); g=np.asarray(groups)
    for a in range(m):
        ia=np.where(g==a)[0]
        wa=np.abs(R[np.ix_(ia,ia)])[np.triu_indices(len(ia),1)].mean()
        for b in range(a+1,m):
            ib=np.where(g==b)[0]
            wb=np.abs(R[np.ix_(ib,ib)])[np.triu_indices(len(ib),1)].mean()
            cross=np.abs(R[np.ix_(ia,ib)]).mean()
            H[a,b]=H[b,a]=cross/math.sqrt(wa*wb)
    return H


def load_csv(path):
    with open(path,encoding="utf-8-sig") as f: return list(csv.DictReader(f))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("config")
    ap.add_argument("--out",default="psychometric_results.json")
    args=ap.parse_args()
    cfg=json.load(open(args.config,encoding="utf-8")); rows=load_csv(args.data)
    dim_map=cfg["dimensions"]
    dims=list(dim_map); items=[i for d in dims for i in dim_map[d]]
    lo,hi=cfg.get("valid_range",[1,5])
    missing_codes=set(str(x) for x in cfg.get("missing_codes",[0,"",None]))

    A=np.empty((len(rows),len(items))); A[:]=np.nan
    for r_idx,r in enumerate(rows):
        for c_idx,item in enumerate(items):
            v=r.get(item,"")
            if str(v) in missing_codes: continue
            try:
                x=float(v)
                if lo<=x<=hi: A[r_idx,c_idx]=x
            except: pass
    complete=np.all(np.isfinite(A),axis=1); X=A[complete]

    item_stats=[]
    for j,item in enumerate(items):
        v=A[np.isfinite(A[:,j]),j]
        item_stats.append({
            "item":item,"valid_n":int(len(v)),"missing_rate":float(1-len(v)/len(rows)),
            "mean":float(np.mean(v)),"sd":float(np.std(v,ddof=1)),
            "skew":float(skew(v,bias=False)),"kurtosis":float(kurtosis(v,bias=False))
        })

    groups=[dims.index(next(d for d in dims if item in dim_map[d])) for item in items]
    kmo,bart,bdf=kmo_bartlett(X)
    eig,q95,npa=parallel_analysis(X,int(cfg.get("parallel_iterations",500)),int(cfg.get("parallel_seed",20261009)))
    nf=int(cfg.get("efa_factors",len(dims)))
    efa=Factor(X,n_factor=nf,method="pa",smc=True,missing="drop").fit(); efa.rotate("oblimin")
    L=np.asarray(efa.loadings)

    rel=[]
    for di,d in enumerate(dims):
        inds=[i for i,g in enumerate(groups) if g==di]
        Xi=X[:,inds]
        rel.append({"dimension":d,"items":len(inds),"alpha":alpha(Xi),"omega":omega_onefactor(Xi)})

    # Score-based Fornell-style matrix is only a diagnostic; latent correlations belong in CFA.
    scores=np.column_stack([X[:,[i for i,g in enumerate(groups) if g==di]].mean(axis=1) for di in range(len(dims))])
    score_corr=np.corrcoef(scores,rowvar=False)
    H=htmt(X,groups,len(dims))

    out={
        "provenance":"silicon/human input as provided; this script does not infer provenance",
        "candidate_n":len(rows),"complete_case_n":int(complete.sum()),"retention_rate":float(complete.mean()),
        "item_stats":item_stats,"kmo":kmo,"bartlett_chi2":bart,"bartlett_df":bdf,
        "parallel_actual_eigenvalues":eig.tolist(),"parallel_random95":q95.tolist(),"parallel_factor_count":npa,
        "efa_loadings":L.tolist(),"reliability":rel,"dimension_score_correlations":score_corr.tolist(),"htmt":H.tolist(),
        "method_note":"EFA=PAF+Oblimin; CFA/CR/AVE/Fornell latent matrix should be completed with an estimator appropriate to the data."
    }
    json.dump(out,open(args.out,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"candidate N={len(rows)}; complete N={complete.sum()}; wrote {args.out}")

if __name__=="__main__": main()
