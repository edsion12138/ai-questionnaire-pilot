---
name: psychometric-pretest
description: "Run a rigorous questionnaire pretest workflow on silicon or human pilot data: item analysis, missing-data audit, complete-case counts, parallel analysis, PAF+Oblimin EFA, CFA model comparison, alpha/omega, CR/AVE, Fornell-Larcker, HTMT, common-method-bias diagnostics, and criterion-related validity."
---

Use this skill when item-response data are available.

## Workflow and scope

Keep three stages distinct:

### A. Questionnaire development

Theory and construct development → content validity → expert review → cognitive interviews. These are development and content-validation activities, not statistical questionnaire-quality tests; conduct them before formal administration.

### B. Data preparation

Data screening → missing-data diagnosis → complete-case audit → fix the eligible EFA and CFA samples. Report each sample transition, for example: returned N=1,000 → eligible N=950 after screening → 35-item complete cases N=720 → fixed exploration N=360 and validation N=360. Sample screening and complete-case counts describe data eligibility, not questionnaire quality indicators. Do this before descriptive statistics.

### C. Formal questionnaire quality checks

After data preparation, follow this reporting order:

1. Descriptive statistics.
2. Common method bias (CMB) diagnostics.
3. Item analysis.
4. KMO, Bartlett's test, and parallel analysis.
5. Exploratory factor analysis (EFA).
6. Confirmatory factor analysis (CFA).
7. Reliability (e.g. alpha, omega, CR).
8. Convergent validity (standardized loadings, AVE).
9. Discriminant validity (Fornell-Larcker, HTMT).
10. Criterion-related/external validity.

Run reliability and validity reporting after CFA in the report, even if software calculates some statistics in the same step. Attribute them to the final measurement structure. Regression, path analysis, SEM, mediation, and moderation are subsequent theory tests, not questionnaire-quality checks; handle them separately when requested.

## A. Data preparation and missing-value rules

1. Treat only valid response-scale values as scale scores.
2. Treat 0, blank, “未接触/无法判断”, “not applicable”, or any non-scale code as missing unless the user explicitly defines otherwise.
3. Never silently convert “not exposed” to the lowest score.
4. Item descriptive statistics may use all valid responses to that item, so item-level N may differ.
5. For the default conservative pre-pilot workflow:
   - CITC, alpha-if-deleted, and extreme-group discrimination use complete cases for that scale;
   - parallel analysis and EFA use complete cases in the fixed exploration group;
   - CFA, alpha/omega, CR/AVE, Fornell-Larcker, and HTMT use the same complete cases in the fixed validation group.
6. Always report candidate N, analysis N, and retention rate.
7. If complete-case retention is poor, do not automatically impute. First diagnose whether missingness is concentrated by item, construct, or subgroup. For human ordinal data, consider an appropriate model-based missing-data approach only after that diagnosis.

## B. Descriptive statistics

Before item-level quality diagnostics, describe the eligible sample and item response distributions. Report valid N and missing/not-exposed rate by item, plus mean, SD, skewness, kurtosis, and floor/ceiling proportions. Item-level valid N may differ. Keep sample screening and complete-case counts in the data-preparation section.

## C. Common method bias

For same-respondent, same-time self-report measures:
1. Harman unrotated single-factor diagnostic: report first-factor variance and number of factors; do not treat 40%/50% as a universal law.
2. Single-factor CFA across the same-source item set; compare against the theoretical measurement model.
3. If different silicon datasets were generated independently, do not concatenate them and claim a valid joint CMB test. Mark the joint test as pending human same-source data.

## D. Item analysis

Report at minimum:
- valid N;
- missing/not-exposed rate;
- mean;
- SD;
- skewness;
- kurtosis;
- floor/ceiling proportions;
- total-scale CITC;
- within-dimension CITC;
- alpha if deleted within the dimension;
- high/low 27% group discrimination when useful.

Do not delete an item from a single statistic.

## E. Factorability and factor-count assessment

1. Report KMO and Bartlett's test as evidence about factorability.
2. Use parallel analysis as the primary empirical guide to factor count; also inspect theory and the scree pattern.

## F. Exploratory factor analysis

1. Default extraction for latent scale development: Principal Axis Factoring (PAF).
2. Default rotation when constructs may correlate: Oblimin or Promax.
3. Do not treat PCA as equivalent to common-factor EFA.
4. Report primary loading, secondary loading/cross-loading, communality, and factor correlations.
5. A theoretically important item with a borderline loading should be flagged for human retesting rather than automatically deleted.

## G. CFA/model comparison

At minimum compare:
- one-factor model;
- intended correlated first-order model;
- any theoretically justified hierarchical model.

Report:
- chi-square;
- df;
- chi-square/df;
- RMSEA;
- CFI;
- TLI;
- SRMR;
- AIC/BIC when available;
- nested-model difference test when appropriate.

For human 5-point ordinal Likert data, consider WLSMV/DWLS rather than defaulting mechanically to normal-theory ML.

## H. Reliability

Using the same fixed validation sample, report by construct:
- Cronbach's alpha;
- McDonald's omega;
- mean inter-item correlation;
- composite reliability (CR).

## I. Convergent validity

After the CFA measurement structure is established, report standardized loading range and AVE by construct. Do not use AVE >= .50 as an automatic deletion rule. Interpret it with reliability, loadings, model fit, and content coverage.

## J. Discriminant validity

Calculate and present full matrices for:
- Fornell-Larcker: sqrt(AVE) on the diagonal, latent correlations off-diagonal;
- HTMT: all construct pairs.

Common heuristic: HTMT < .85 is stricter; < .90 is looser. Do not present only the maximum if the user asks for full validation.

## K. Criterion-related/external validity

If a validated criterion scale is available:
- score it separately;
- do not merge it into the new scale's EFA/CFA;
- report Pearson r, p, and 95% CI at minimum;
- optionally report latent correlation/SEM coefficient;
- for cross-sectional same-time data use terms such as concurrent criterion-related validity, external validity, or nomological validity rather than predictive validity.

Read `references/missing-data-rules.md`, `references/efa-cfa-rules.md`, and `references/validity-rules.md`. Use `scripts/psychometric_pipeline.py` as a reproducible starter when appropriate.
