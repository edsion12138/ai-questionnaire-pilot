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
- item analysis;
- parallel analysis;
- EFA loadings;
- CFA/model comparison;
- reliability;
- CR/AVE;
- Fornell-Larcker;
- HTMT;
- common-method-bias diagnostics;
- criterion validity;
- version comparison;
- item deletion/rewrite log;
- random seeds and reproducibility parameters;
- human follow-up template.

Clearly label historical analyses versus the current final analysis convention.

### 2. Revision-process report
Document:
- theoretical starting structure;
- wording/content audit;
- silicon sample design;
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
