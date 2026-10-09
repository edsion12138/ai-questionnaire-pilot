---
name: validation-report
description: Produce a reproducible questionnaire-development record after silicon or human pretesting. Use when the user wants a consolidated Excel workbook, revision-process report, analysis log, codebook, version history, or handoff template that clearly separates silicon evidence from human empirical evidence.
---

Use this skill near the end of each iteration and before handoff to human pretesting.

## Required outputs

### 1. Consolidated analysis workbook
Prefer one workbook rather than scattered files. Include, when applicable:
- overview/index;
- sample structure;
- variable codebook;
- raw data;
- complete-case flags;
- data-screening, missingness, and complete-case audit;
- descriptive statistics;
- common-method-bias diagnostics;
- item analysis;
- parallel analysis;
- EFA loadings;
- CFA/model comparison;
- reliability;
- CR/AVE;
- Fornell-Larcker;
- HTMT;
- criterion validity;
- version comparison;
- item deletion/rewrite log;
- random seeds and reproducibility parameters;
- human follow-up template.

Keep data preparation distinct from statistical quality checks. In the report, order quality checks as: descriptive statistics → CMB → item analysis → KMO/Bartlett/parallel analysis → EFA → CFA → reliability → convergent validity → discriminant validity → criterion-related/external validity. Place regression, path analysis, SEM, mediation, and moderation in a separate subsequent theory-testing section. Clearly label historical analyses versus the current final analysis convention.

### 2. Revision-process report
Document:
- theoretical starting structure;
- questionnaire development and content validation (content validity, expert review, cognitive interviews);
- silicon sample design, when applicable;
- data screening, missing-data diagnosis, complete-case audit, and fixed EFA/CFA samples;
- descriptive statistics and each formal quality-check stage in the standard order;
- each analysis round;
- item modifications and rationale;
- model comparison;
- final silicon evidence;
- limitations of silicon evidence;
- cognitive-interview plan;
- human pilot plan;
- fields/placeholders to fill after human data are collected.

### 3. Provenance rule
Every report must clearly distinguish:
- AI/silicon-sample simulation results;
- human empirical results;
- literature-derived claims;
- researcher decisions.

Never describe simulated respondents as real participants.

### 4. Reproducibility
Record:
- data version;
- random seeds;
- stratification;
- fixed split rule;
- missing-data rule;
- estimator/extraction/rotation choices;
- item-number mapping across versions.

Use the templates in `assets/analysis-workbook-template.xlsx` and `assets/revision-report-template.docx` when they match the user's workflow. Read `references/reporting-checklist.md` before finalization.
