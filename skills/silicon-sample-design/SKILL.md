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

<!-- MULTISEED-V1.1 -->
## 12＋2＋2情景稳定性工作流（v1.1，可选增强）

在初步结构通过内容审查之后，可以预先设定12个中等测量清晰度种子、2个高噪声种子、2个高共同性种子，固定每道题的生成参数，观察模型对随机实现与参数变化的敏感性。先用8个中等种子提出删题候选，再在4个**未参与筛选**的中等种子与4个压力/乐观情景种子上复核。所有版本须在每轮同一份数据和同一固定探索/验证分组上比较，完整案例依据原始题库一次确定，不能因为删题造成N改变。报告中位数、范围、达标次数与失败条件，禁止自动择优随机种子、后验抬高载荷，禁止把恢复预设因子解释为真实构念验证。根据问卷内容维度进行人工修订，不用统计阈值代替内容覆盖。详见 `references/multiseed-sensitivity-method.md`；运行 `scripts/multiseed_sensitivity.py`。**此脚本为参数生成器而非LLM API；CFA/CR/AVE等另行验证。**
