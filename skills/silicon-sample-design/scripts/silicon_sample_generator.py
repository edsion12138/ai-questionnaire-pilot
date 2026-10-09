#!/usr/bin/env python3
"""Generic ordinal silicon-sample generator for questionnaire pre-piloting.

Input: JSON config. Output: CSV + metadata JSON.
This is a starter implementation, not a substitute for researcher-specified population logic.

Example config keys:
{
  "n": 800,
  "seed": 20261009,
  "split_seed": 20261010,
  "ordinal_thresholds": [-0.9, -0.2, 0.5, 1.2],
  "background_variables": {
    "grade": {"values": ["3", "4"], "probs": [0.5, 0.5]},
    "major": {"values": ["A", "B", "C"], "probs": [0.4, 0.35, 0.25]}
  },
  "dimensions": {
    "D1": {"items": ["I01","I02","I03"], "loading": 0.70},
    "D2": {"items": ["I04","I05","I06"], "loading": 0.68}
  },
  "dimension_correlations": [[1.0,0.45],[0.45,1.0]],
  "background_effects": {
    "grade": {"4": {"D1": 0.20, "D2": 0.15}},
    "major": {"B": {"D2": 0.20}}
  },
  "exposure_missing": {
    "I06": {"base_prob": 0.03, "by": {"grade": {"3": 0.06, "4": 0.01}}}
  }
}
"""

import argparse, csv, json, math
from pathlib import Path
import numpy as np


def nearest_psd_corr(R):
    R = np.asarray(R, float)
    vals, vecs = np.linalg.eigh((R + R.T) / 2)
    vals = np.clip(vals, 1e-6, None)
    P = vecs @ np.diag(vals) @ vecs.T
    d = np.sqrt(np.diag(P))
    return P / np.outer(d, d)


def sample_background(rng, n, specs):
    out = {}
    for name, spec in specs.items():
        vals = spec["values"]
        probs = np.asarray(spec.get("probs", [1/len(vals)]*len(vals)), float)
        probs = probs / probs.sum()
        out[name] = rng.choice(vals, size=n, p=probs)
    return out


def apply_background_effects(latent, dim_names, background, effects):
    for var, levels in effects.items():
        if var not in background:
            continue
        for level, dim_eff in levels.items():
            mask = background[var].astype(str) == str(level)
            for dim, beta in dim_eff.items():
                if dim in dim_names:
                    latent[mask, dim_names.index(dim)] += float(beta)


def missing_probability(item, row_idx, background, config):
    spec = config.get("exposure_missing", {}).get(item)
    if not spec:
        return 0.0
    p = float(spec.get("base_prob", 0.0))
    for var, level_map in spec.get("by", {}).items():
        level = str(background[var][row_idx])
        if level in level_map:
            p = float(level_map[level])
    return min(max(p, 0.0), 0.95)


def stratified_split(rows, strata, seed):
    rng = np.random.default_rng(seed)
    keys = [tuple(str(r[s]) for s in strata) for r in rows]
    groups = {}
    for i, k in enumerate(keys):
        groups.setdefault(k, []).append(i)
    labels = [None] * len(rows)
    for idxs in groups.values():
        idxs = np.asarray(idxs)
        rng.shuffle(idxs)
        half = len(idxs) // 2
        for i in idxs[:half]: labels[int(i)] = "exploration"
        for i in idxs[half:]: labels[int(i)] = "validation"
    return labels


def generate(config):
    n = int(config.get("n", 800))
    seed = int(config.get("seed", 20261009))
    split_seed = int(config.get("split_seed", seed + 1))
    rng = np.random.default_rng(seed)

    dimensions = config["dimensions"]
    dim_names = list(dimensions)
    k = len(dim_names)
    R = nearest_psd_corr(config.get("dimension_correlations", np.eye(k)))
    latent = rng.multivariate_normal(np.zeros(k), R, size=n)

    background = sample_background(rng, n, config.get("background_variables", {}))
    apply_background_effects(latent, dim_names, background, config.get("background_effects", {}))

    thresholds = np.asarray(config.get("ordinal_thresholds", [-1.0, -0.25, 0.45, 1.15]), float)
    item_values = {}
    item_meta = {}
    for d_idx, d in enumerate(dim_names):
        spec = dimensions[d]
        base_loading = float(spec.get("loading", 0.7))
        for item in spec["items"]:
            loading = float(spec.get("item_loadings", {}).get(item, base_loading + rng.normal(0, 0.035)))
            loading = float(np.clip(loading, 0.35, 0.90))
            noise = rng.normal(size=n)
            y = loading * latent[:, d_idx] + math.sqrt(max(1e-6, 1-loading**2)) * noise
            shift = float(spec.get("item_intercepts", {}).get(item, rng.normal(0, 0.12)))
            y = y + shift
            ordinal = np.digitize(y, thresholds) + 1
            vals = ordinal.astype(object)
            for i in range(n):
                if rng.random() < missing_probability(item, i, background, config):
                    vals[i] = config.get("missing_code", 0)
            item_values[item] = vals
            item_meta[item] = {"dimension": d, "loading_used": loading, "shift_used": shift}

    rows = []
    bg_names = list(background)
    item_names = list(item_values)
    for i in range(n):
        r = {"ID": f"S{i+1:04d}"}
        for b in bg_names: r[b] = str(background[b][i])
        for item in item_names: r[item] = item_values[item][i]
        rows.append(r)

    strata = config.get("split_strata", bg_names[:2])
    if strata:
        split = stratified_split(rows, strata, split_seed)
    else:
        idx = np.arange(n); rng2 = np.random.default_rng(split_seed); rng2.shuffle(idx)
        split = [None]*n
        for rank, i in enumerate(idx): split[int(i)] = "exploration" if rank < n//2 else "validation"
    for r, label in zip(rows, split): r["sample_group"] = label

    metadata = {
        "n": n,
        "seed": seed,
        "split_seed": split_seed,
        "split_strata": strata,
        "dimension_order": dim_names,
        "dimension_correlations_used": R.tolist(),
        "ordinal_thresholds": thresholds.tolist(),
        "item_generation": item_meta,
        "missing_code": config.get("missing_code", 0),
        "provenance": "AI/silicon sample for pre-pilot stress testing; not human empirical data"
    }
    return rows, metadata


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out", default="silicon_sample.csv")
    ap.add_argument("--meta", default="silicon_sample_metadata.json")
    args = ap.parse_args()
    config = json.load(open(args.config, encoding="utf-8"))
    rows, meta = generate(config)
    fields = list(rows[0])
    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    json.dump(meta, open(args.meta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {args.out} and {args.meta}")


if __name__ == "__main__":
    main()
