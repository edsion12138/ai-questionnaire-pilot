# AI Questionnaire Pilot v1.0

**中文名：AI问卷硅样本预调研**

这是一个 skills-only plugin，用于在真人预测试之前，对新开发问卷进行低成本、可复现的“硅样本压力测试”。它不会把AI模拟数据当成真人实证结果，也不会以“把统计指标做漂亮”为目标，而是帮助研究者提前发现题项表达、维度边界、缺失机制、EFA/CFA结构、信效度与效标设计中的潜在问题。

## 包含的 5 个 Skills

1. `questionnaire-audit`：理论结构、题项语言、维度边界与跨群体适用性审查。
2. `silicon-sample-design`：分层硅样本设计、异质性建模、随机种子与缺失机制记录。
3. `psychometric-pretest`：项目分析、完整案例审计、平行分析、PAF+Oblimin EFA、CFA、α/ω、CR/AVE、Fornell–Larcker、HTMT、CMB辅助诊断与效标相关。
4. `questionnaire-iteration`：以“统计证据 + 理论依据 + 内容效度”进行保留、观察、改写、候选删除及版本比较。
5. `validation-report`：统一输出全过程Excel、修订报告、复现参数和真人后续分析模板。

## 推荐工作流

初始问卷/理论材料 → Questionnaire Audit → Silicon Sample Design → Psychometric Pretest → Questionnaire Iteration → 独立第二轮硅样本复核 → 真人认知访谈 → 真人预测试 → Validation Report。

## 核心方法原则

- 硅样本只用于预预测试、压力测试和分析流程演练，不能替代真人预测试或正式验证。
- 不人为先贴“高能力/低能力”标签再生成漂亮答案；差异应由真实背景变量、潜在个体差异和随机扰动共同形成。
- “未接触/无法判断”不是0分或1分，应按缺失处理。
- 项目描述统计允许各题有效N不同；EFA/CFA及主要信效度必须明确共同分析样本。
- 默认优先 PAF + Oblimin/Promax，而不是把 PCA + Varimax 当成量表EFA的默认方案。
- 不机械追求 α、AVE、CFI 或载荷阈值；删题必须同时考虑理论与内容效度。
- 对与理论不一致的结果如实报告，并明确哪些问题必须留待真人样本验证。

## 安装/使用

该目录遵循 portable plugin 结构。根目录有 `plugin.json`，skills 位于 `skills/` 下。可以将整个 `ai-questionnaire-pilot` 目录压缩为ZIP后，在支持上传Skills/Plugins的ChatGPT工作区中测试。具体可用性受账号、工作区和产品界面影响。

## V1.0 的边界

V1.0 不连接外部MCP服务，不自动访问问卷平台，也不自动发送调查。它提供方法工作流、分析代码和报告模板。正式研究仍需研究者负责抽样、伦理、知情同意、真人数据质量和最终统计决策。
