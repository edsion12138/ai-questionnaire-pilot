---
name: silicon-sample-design
description: Design reproducible AI silicon samples for questionnaire pre-piloting. Use when the user wants synthetic respondents that reflect realistic heterogeneity, stratification, exposure patterns, missing/not-exposed responses, and fixed EFA/CFA splits without manufacturing a perfect factor structure.
---

Use this skill after the questionnaire structure is sufficiently clear.

## Goal
Create a stress-test dataset, not a proof that the questionnaire works.

## Rules

1. Never pre-label respondents as “high ability” and “low ability” and directly force their answers.
2. Build heterogeneity from plausible observed variables and latent/random variation, for example:
   - major/discipline;
   - grade/year;
   - admission pathway;
   - prior learning;
   - internship/project/competition exposure;
   - tool-use frequency;
   - AI-use frequency;
   - resource conditions;
   - teacher/peer support.
3. Let these factors influence latent tendencies probabilistically. Include meaningful residual noise so respondents within the same subgroup do not answer identically.
4. Same-dimension items may correlate moderately; adjacent constructs may correlate; do not force near-perfect simple structure.
5. If the questionnaire has “未接触/无法判断/not applicable”, generate it from exposure logic. Do not sprinkle missing values randomly merely to look realistic.
6. Record every reproducibility parameter:
   - sample size;
   - strata and target proportions;
   - random seed;
   - latent correlation assumptions;
   - item discrimination/noise parameters;
   - ordinal thresholds;
   - missing/exposure rules;
   - EFA/CFA split seed.
7. When a second silicon round is required:
   - generate an independent response realization;
   - use a new response-generation seed;
   - keep the same intended population design unless the researcher changes it;
   - once EFA/CFA groups are fixed, do not redraw them when comparing questionnaire versions.

## Recommended workflow

1. Propose the stratification table.
2. Ask for confirmation only if the user's intended population proportions or key variables are unknown.
3. Generate demographics/background variables first.
4. Generate latent tendencies from those backgrounds plus random individual effects.
5. Generate ordinal item responses from latent tendencies plus item-specific noise.
6. Apply exposure-based missing/not-exposed rules.
7. Create and save a fixed stratified EFA/CFA split.
8. Produce a sample-structure table and reproducibility log before psychometric analysis.

Read `references/simulation-principles.md` and use `scripts/silicon_sample_generator.py` as a starting implementation when code execution is appropriate.
