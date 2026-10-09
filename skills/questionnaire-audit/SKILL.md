---
name: questionnaire-audit
description: Audit a draft questionnaire before human pilot testing. Use when the user wants to review construct definitions, dimension boundaries, item wording, content coverage, cross-group applicability, response scales, or whether a draft questionnaire is ready for silicon-sample or human pretesting.
---

Use this skill before generating any silicon sample when the questionnaire structure has not yet been audited.

## Development-stage boundary

Treat theoretical construct development, content-validity review, expert review, and cognitive interviews as questionnaire development and content validation before formal administration. They are not statistical questionnaire-quality tests. Use this skill to organize the construct and item review; use `psychometric-pretest` for data screening and the subsequent statistical quality checks.

## Workflow

1. Read the user's questionnaire, theoretical framework, target population, reference scales, and any coding/interview material they provide.
2. Reconstruct the intended measurement model:
   - target construct(s);
   - first-order dimensions;
   - any higher-order structure;
   - item-to-dimension mapping;
   - response scale;
   - non-scale modules such as demographics, behavior frequencies, predictors, criteria, and open-ended questions.
3. For every scale item, check:
   - one item = one core behavior/judgment;
   - double-barreled wording;
   - unnecessary conjunctions such as “并/以及/同时/且”;
   - vague frequency, time, or task referents;
   - over-abstract language;
   - jargon or discipline-specific terms that may not generalize;
   - attitude/knowledge/behavior/ability mixing;
   - social desirability or obviously “correct” answers;
   - overlap with neighboring dimensions;
   - whether respondents can reasonably recall an experience and choose a response.
4. Build an item diagnostic table with at least:
   - item ID;
   - dimension;
   - content function;
   - wording issue;
   - dimension-boundary issue;
   - cross-group applicability;
   - suggested action: retain / observe / rewrite / possible deletion.
5. Do not delete items solely from wording review. Distinguish language revision from psychometric deletion.
6. Before any simulation, present the user with:
   - the reconstructed structure;
   - main theoretical/wording risks;
   - proposed silicon-sample stratification variables;
   - analysis plan;
   - only the few decisions that truly require researcher confirmation.

## Output requirements

Prefer concise tables plus a short methodological interpretation. Preserve the user's construct terminology unless a change is necessary and clearly explained.

Read `references/item-writing-rules.md` and `references/content-validity-checklist.md` when performing a full audit.
