#!/usr/bin/env python3
"""Pre-registered 12+2+2 synthetic measurement sensitivity audit.

Standalone, NumPy/SciPy/statsmodels-compatible with the repository's JSON
``dimensions`` / ``background_variables`` conventions. This is a parametric
synthetic generator, NOT an LLM respondent API. Neither EFA recovery nor
reliability in generated data is evidence of human measurement validity.
CFA/CR/CFA-AVE/Fornell-Larcker must be computed separately by the
psychometric-pretest stage using the appropriate ordinal estimator.
"""
from __future__ import annotations
import argparse
import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.stats import chi2
from statsmodels.multivariate.factor import Factor


def code_to_offset(key: str) -> float:
    """Stable item-specific deviation, constant over ALL seeds and scenarios."""
    number = int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], 'big')
    return 2 * (number / (2**64 - 1)) - 1


def corr_psd(corr, n):
    r = np.asarray(corr if corr is not None else np.eye(n), dtype=float)
    if r.shape != (n, n):
        raise ValueError(f'Expected {n}x{n} factor correlation matrix')
    r = (r + r.T) / 2
    eig, u = np.linalg.eigh(r)
    r = (u * np.maximum(eig, 1e-6)) @ u.T
    s = np.sqrt(np.diag(r))
    return r / s[:, None] / s[None, :]


def generate(base, seed, scenario):
    rng = np.random.default_rng(seed)
    n = int(base['n'])
    dims = list(base['dimensions'])
    r = corr_psd(base.get('dimension_correlations'), len(dims))
    latent = rng.multivariate_normal(np.zeros(len(dims)), r, size=n)
    bg = {}
    for key, spec in base.get('background_variables', {}).items():
        vals = [str(v) for v in spec['values']]
        p = np.asarray(spec.get('probs', [1 / len(vals)] * len(vals)), float)
        bg[key] = rng.choice(vals, n, p=p / p.sum())
    for var, levels in base.get('background_effects', {}).items():
        if var not in bg:
            raise ValueError(f'background_effects references unknown variable {var}')
        for level, effects in levels.items():
            mask = bg[var] == str(level)
            for dim, beta in effects.items():
                latent[mask, dims.index(dim)] += float(beta)
    threshold = np.array(base.get('ordinal_thresholds', [-1.0, -0.25, .45, 1.15]), dtype=float)
    if len(threshold) != 4 or not np.all(np.diff(threshold) > 0):
        raise ValueError('Require 4 strictly increasing thresholds for 1--5 Likert')
    method = rng.normal(size=n)
    all_items = [x for d in dims for x in base['dimensions'][d]['items']]
    if len(all_items) != len(set(all_items)):
        raise ValueError('Duplicate item code across dimensions')
    answers = {}
    manifest = {}
    for d in dims:
        spec = base['dimensions'][d]
        for item in spec['items']:
            fixed = float(spec.get('item_loadings', {}).get(item, float(spec.get('loading', .7)) +
                      float(base.get('item_loading_jitter', .025)) * code_to_offset(item)))
            main = fixed * float(scenario.get('loading_scale', 1))
            if not .05 < main < .96:
                raise ValueError(f'Invalid scaled loading {main:.3f} for {item}; change scenario')
            cross = base.get('cross_loadings', {}).get(item, {})
            cs = {k: float(v) * float(scenario.get('cross_scale', 1)) for k, v in cross.items()}
            method_loading = float(base.get('method_loading', .06)) * float(scenario.get('method_scale', 1))
            variance = main**2 + sum(x*x for x in cs.values()) + method_loading**2
            if variance >= .97:
                raise ValueError(f'Factor loadings account for >=.97 variance for item {item}')
            z = main * latent[:, dims.index(d)] + method_loading * method
            for other, weight in cs.items():
                z += weight * latent[:, dims.index(other)]
            z += np.sqrt(1 - variance) * rng.normal(size=n)
            z += float(spec.get('item_intercepts', {}).get(item, 0))
            values = np.searchsorted(threshold, z, side='right') + 1
            exposure = base.get('exposure_missing', {}).get(item)
            if exposure:
                prob = np.full(n, float(exposure.get('base_prob', 0)))
                for variable, bylevel in exposure.get('by', {}).items():
                    if variable not in bg:
                        raise ValueError(f'Missing background {variable} in exposure rule')
                    for lev, p in bylevel.items():
                        prob[bg[variable] == str(lev)] = float(p)
                if not np.all((prob >= 0) & (prob <= 1)):
                    raise ValueError('Exposure missingness probability outside [0,1]')
                values[rng.random(n) < prob] = 0
            answers[item] = values
            manifest[item] = {'dimension': d, 'loading': round(main, 5),
                              'cross_loadings': cs, 'method_loading': method_loading}
    rows = []
    for i in range(n):
        row = {'ID': f'S{i+1:04d}', **{v: str(bg[v][i]) for v in bg}}
        row.update({item: int(answers[item][i]) for item in all_items})
        rows.append(row)
    # Fixed 50:50 split within observed strata, independent of item outcomes
    rngsplit = np.random.default_rng(seed + 20_000)
    strata = base.get('split_strata', list(bg)[:2])
    strata_groups = {}
    for i, row in enumerate(rows):
        key = tuple(row[k] for k in strata)
        strata_groups.setdefault(key, []).append(i)
    split = [''] * n
    for indices in strata_groups.values():
        idx = np.array(indices, dtype=int)
        rngsplit.shuffle(idx)
        for row_index in idx[:len(idx)//2]: split[row_index] = 'exploration'
        for row_index in idx[len(idx)//2:]: split[row_index] = 'validation'
    for row, group in zip(rows, split): row['sample_group'] = group
    return rows, {'item_parameters': manifest, 'factor_correlation': r.tolist(),
                  'split_strata': strata, 'split_seed': seed + 20_000}


def alpha(x):
    k = x.shape[1]
    if k < 2: return float('nan')
    return float(k / (k-1) * (1 - x.var(axis=0, ddof=1).sum() / x.sum(axis=1).var(ddof=1)))


def kmo(x):
    r = np.corrcoef(x, rowvar=False)
    inv = np.linalg.pinv(r)
    partial = -inv / np.sqrt(np.outer(np.diag(inv), np.diag(inv)))
    ii = np.triu_indices(r.shape[0], 1)
    a = np.sum(r[ii]**2)
    return float(a/(a+np.sum(partial[ii]**2)))


def parallel(x, iters, seed):
    n, p = x.shape
    actual = np.linalg.eigvalsh(np.corrcoef(x, rowvar=False))[::-1]
    rng = np.random.default_rng(seed)
    random_eigs = np.empty((iters, p))
    for b in range(iters):
        fake = rng.standard_normal((n, p))
        random_eigs[b] = np.linalg.eigvalsh(np.corrcoef(fake, rowvar=False))[::-1]
    return int((actual > np.quantile(random_eigs, .95, axis=0)).sum())


def htmt(x, groups, dimensions):
    r = np.abs(np.corrcoef(x, rowvar=False))
    ratios = []
    for a in range(dimensions):
        aa = np.where(groups == a)[0]
        if len(aa) < 2: continue
        wa = r[np.ix_(aa,aa)][np.triu_indices(len(aa),1)].mean()
        for b in range(a+1, dimensions):
            bb = np.where(groups == b)[0]
            if len(bb) < 2: continue
            wb = r[np.ix_(bb,bb)][np.triu_indices(len(bb),1)].mean()
            ratios.append(r[np.ix_(aa,bb)].mean()/np.sqrt(max(wa*wb,1e-9)))
    return float(max(ratios)) if ratios else float('nan')


def analyse(rows, base, block_dims, drop, parallel_iters, seed):
    dim_items = {d: [it for it in base['dimensions'][d]['items'] if it not in drop] for d in block_dims}
    if min(map(len, dim_items.values())) < 3:
        return {'status': 'blocked_min_three_items', 'dimension_counts': {d:len(v) for d,v in dim_items.items()}}
    items = [it for d in dim_items for it in dim_items[d]]
    bank = [it for d in block_dims for it in base['dimensions'][d]['items']]
    # Common-case policy applies to original block bank, NOT recalculated after candidate deletion
    valid = [r for r in rows if all(str(r[it]) in {'1','2','3','4','5'} for it in bank)]
    ex = [r for r in valid if r['sample_group']=='exploration']
    va = [r for r in valid if r['sample_group']=='validation']
    result = {'eligible_n': len(valid), 'efa_n': len(ex),'validation_n': len(va),
              'items': len(items),'dimensions':len(dim_items)}
    if min(len(ex),len(va)) < max(30,4*len(items)):
        result['status'] = 'insufficient_complete_cases'
        return result
    xe = np.array([[int(r[it]) for it in items] for r in ex],float)
    xv = np.array([[int(r[it]) for it in items] for r in va],float)
    result['kmo'] = kmo(xe)
    result['parallel_factors'] = parallel(xe, parallel_iters, seed+30_000)
    g = np.array([j for j,d in enumerate(dim_items) for it in dim_items[d]])
    efa = Factor(xe, n_factor=len(dim_items), method='pa', smc=True, missing='drop').fit()
    efa.rotate('oblimin')
    L = np.asarray(efa.loadings)
    target = np.zeros((len(dim_items),len(dim_items)))
    for fac in range(len(dim_items)):
        target[fac] = np.abs(L[g==fac]).mean(axis=0)
    row, col = linear_sum_assignment(-target)
    order = col[np.argsort(row)]
    L = L[:,order]
    primary = np.abs(L[np.arange(len(items)),g])
    secondary = np.max(np.where(np.eye(len(dim_items), dtype=bool)[g], 0, np.abs(L)),axis=1)
    result.update({'status':'ok', 'min_primary': float(primary.min()),'max_cross':float(secondary.max()),
                   'item_efa':{it:{'primary':float(primary[i]), 'cross':float(secondary[i])} for i,it in enumerate(items)},
                   'alpha':{d:alpha(xv[:,g==i]) for i,d in enumerate(dim_items)},
                   'max_htmt':htmt(xv,g,len(dim_items))})
    # These are screening diagnostics, not a CFA-based reliability/validity claim.
    result['checks']={'KMO_ge_0.7': result['kmo']>=.7,
      'PA_recovers_intended':result['parallel_factors']==len(dim_items),
      'min_primary_ge_0.45': result['min_primary']>=.45,
      'max_cross_le_0.30':result['max_cross']<=.30,
      'all_alpha_ge_0.7':all(a>=.7 for a in result['alpha'].values()),
      'HTMT_lt_0.85':result['max_htmt']<.85}
    return result


def robust_summary(records, blocks, candidates, selection_seeds):
    def summarise(rr):
        ok=[r['result'] for r in rr if r['result']['status']=='ok']
        if not ok: return {'runs':len(rr),'ok_runs':0}
        keys=['kmo','parallel_factors','min_primary','max_cross','max_htmt']
        d={'runs':len(rr),'ok_runs':len(ok)}
        for k in keys:
            vals=np.array([r[k] for r in ok],float)
            d[k]={'min':float(vals.min()),'median':float(np.median(vals)),'max':float(vals.max())}
        d['PA_recovery_count']=sum('PA_recovers_intended' in o['checks'] and o['checks']['PA_recovers_intended'] for o in ok)
        d['all_checks_pass_count']=sum(all(o['checks'].values()) for o in ok)
        alpha_by={k:[o['alpha'][k] for o in ok] for k in ok[0]['alpha']}
        d['alpha_median']={k:float(np.median(v)) for k,v in alpha_by.items()}
        return d
    report={}
    for block in blocks:
        report[block]={}
        for candidate in candidates:
            scoped=[x for x in records if x['block']==block and x['version']==candidate]
            report[block][candidate]={part:summarise([x for x in scoped if x['scenario']==part]) for part in ['medium','noise','high']}
            dev=[x for x in scoped if x['scenario']=='medium' and x['seed'] in selection_seeds]
            held=[x for x in scoped if x['scenario']=='medium' and x['seed'] not in selection_seeds]
            report[block][candidate]['development_8']=summarise(dev)
            report[block][candidate]['seed_holdout_4']=summarise(held)
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('design',help='Multi-scenario JSON configuration')
    parser.add_argument('--out',default='multi_seed_results')
    parser.add_argument('--save-raw', action='store_true',help='Save 16 complete synthetic data sets')
    args=parser.parse_args(argv)
    designpath=Path(args.design).resolve()
    design=json.loads(designpath.read_text(encoding='utf-8'))
    basepath=(designpath.parent/design['base_config']).resolve()
    base=json.loads(basepath.read_text(encoding='utf-8'))
    design.setdefault('analysis_blocks',{'all':list(base['dimensions'])})
    candidates={'full':[],**design.get('candidates',{})}
    med=design['seeds']['medium'];noise=design['seeds']['noise'];high=design['seeds']['high']
    if list(map(len,(med,noise,high))) != [12,2,2]:
        raise ValueError('Protocol requires EXACTLY 12 medium + 2 noise + 2 high seeds')
    seeds=med+noise+high
    if len(set(seeds)) != 16:
        raise ValueError('All 16 seeds must be distinct and predeclared')
    dev_count=int(design.get('development_medium_seeds',8))
    if dev_count!=8:raise ValueError('Eight development seeds and four held-out seeds required')
    for name,drop in candidates.items():
        if len(drop)!=len(set(drop)):raise ValueError('Repeated candidate deletion item')
        missing=set(drop)-set(it for d in base['dimensions'].values() for it in d['items'])
        if missing:raise ValueError(f'Unknown item(s) for {name}: {missing}')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if args.save_raw:(out/'samples').mkdir(exist_ok=True)
    (out/'frozen_design.json').write_text(json.dumps({'design':design,'base':base},ensure_ascii=False,indent=2),encoding='utf-8')
    records=[];manifests=[]
    for scenario, ss in [('medium',med),('noise',noise),('high',high)]:
        mod=design.get('scenarios',{}).get(scenario,{})
        for idx,seed in enumerate(ss):
            rows,extra=generate(base,int(seed),mod)
            manifests.append({'scenario':scenario,'seed':seed,'role': ('development' if scenario=='medium' and idx<8 else 'seed_holdout' if scenario=='medium' else 'sensitivity'), 'metadata':extra})
            if args.save_raw:
                with (out/'samples'/f'{scenario}_{seed}.csv').open('w',encoding='utf-8-sig',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            for block,dims in design['analysis_blocks'].items():
                for version,drop in candidates.items():
                    result=analyse(rows,base,dims,set(drop),int(design.get('parallel_iterations',100)),int(seed))
                    records.append({'scenario':scenario,'seed':seed,'block':block,'version':version,'role':manifests[-1]['role'],'result':result})
            print(f'{scenario} {idx+1}/{len(ss)} seed={seed} complete',flush=True)
    report={'provenance':'PARAMETRIC SYNTHETIC PRE-PILOT, not human data or LLM API survey',
       'design_path':str(basepath),'scenario_seeds':design['seeds'],
       'selection_rule':'No automatic seed or version cherry-picking; reserve 4 medium seeds plus 4 sensitivity runs; 8 development seeds only for candidate screening',
       'not_estimated':['CFA','CFA-based CR','CFA-based AVE','Fornell-Larcker','CMB-CFA','criterion validity'],
       'summary':robust_summary(records,design['analysis_blocks'],candidates,set(med[:8]))}
    (out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps(manifests,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'runs.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'runs_flat.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['scenario','seed','role','block','version','status','eligible_n','efa_n','validation_n','n_items','n_dimensions','kmo','PA','min_primary','max_cross','max_htmt','all_checks_pass']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for r in records:
            v=r['result'];writer.writerow({'scenario':r['scenario'],'seed':r['seed'],'role':r['role'],'block':r['block'],'version':r['version'],
                'status':v['status'],'eligible_n':v.get('eligible_n'), 'efa_n':v.get('efa_n'),
                'validation_n':v.get('validation_n'),'n_items':v.get('items'),'n_dimensions':v.get('dimensions'),
                'kmo':v.get('kmo'),'PA':v.get('parallel_factors'),'min_primary':v.get('min_primary'),
                'max_cross':v.get('max_cross'),'max_htmt':v.get('max_htmt'),
                'all_checks_pass':all(v['checks'].values()) if 'checks' in v else False})
    print('Wrote',out/'summary.json')
    return report


if __name__=='__main__':main()
