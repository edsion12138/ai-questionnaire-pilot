# AI Questionnaire Pilot v1.1.0

**中文名：AI问卷硅样本预调研**

本项目提供一套可组合的问卷开发、参数化硅样本压力测试与心理测量分析 Skills，帮助研究者在真人预测试前发现构念边界、题项表达和测量结构中的问题。模拟结果用于方法演练与敏感性诊断，不提供真人效度证据。

## 包含的 5 个 Skills

1. `questionnaire-audit`：审查构念定义、题项语言、维度边界和内容覆盖。
2. `silicon-sample-design`：设计分层硅样本、固定分析分组，并运行多随机种子与测量情景压力测试。
3. `psychometric-pretest`：按数据准备和质量检验流程开展项目分析、EFA、CFA、信效度及效标分析。
4. `questionnaire-iteration`：结合统计结果、理论角色和内容覆盖决定保留、观察、改写、删题或转移构念。
5. `validation-report`：整理样本、分析结果、版本修订、复现参数和真人后续验证计划。

## 标准工作流程

### A. 问卷开发与内容验证

理论和构念建构 → 内容效度 → 专家审查 → 认知访谈。该阶段用于确定测量内容与题项表达，不属于统计意义上的问卷质量检验。

### B. 数据准备

数据筛查 → 缺失诊断 → 完整案例审计 → 固定 EFA/CFA 样本与分组。记录样本从回收、筛查到各分析样本的变化；候选版本比较沿用原题库确定的完整案例，避免删题后样本量变化造成不公平比较。

### C. 正式问卷质量检验

**描述性统计 → CMB 检验 → 项目分析 → KMO/Bartlett 与平行分析 → EFA → CFA → 信度（α、ω、CR）→ 聚合效度（标准化载荷、AVE）→ 区分效度（Fornell–Larcker、HTMT）→ 效标关联/外部效度。**

信度与效度在报告中放在 CFA 之后，归属于最终测量结构。回归、路径分析、SEM、中介和调节属于后续理论检验，应另设分析部分。

## V1.1 多种子与情景压力测试

在构念和题项通过开发阶段审查后，可运行 **12＋2＋2** 设计：12 个中等测量清晰度种子用于评估波动，另设 2 个高噪声情景和 2 个较高共同性情景用于敏感性检查。建议从 12 个中等种子中预先划定 8 个开发种子与 4 个保留种子；保留种子不参与候选筛选。4 个保留种子和 4 个压力情景检查的是模拟机制下的稳定性，不构成真人独立验证。

种子、题项参数、情景、候选版本、样本完整案例和分析分组应在查看结果前冻结。所有候选版本须在相同响应数据和固定分组下比较，报告每轮结果、中位数、范围、达标次数及未通过情景；不挑选表现最佳的一轮，也不靠事后提高预设载荷追求达标。

### 运行示例

需要 Python 及依赖包。安装依赖并运行示例：

```bash
python -m pip install -r requirements-multiseed.txt
python skills/silicon-sample-design/scripts/multiseed_sensitivity.py skills/silicon-sample-design/assets/example-multi-scenario-config.json --out demo16 --save-raw
```

脚本输出情景设计快照、生成参数、各轮和各版本结果汇总；使用 `--save-raw` 时另存 16 份模拟数据。运行随包测试：

```bash
python -m unittest discover -s tests -v
```

详细方法见 [`multiseed-sensitivity-method.md`](skills/silicon-sample-design/references/multiseed-sensitivity-method.md)，删题记录见 [`multiseed-decision-worksheet.md`](skills/questionnaire-iteration/references/multiseed-decision-worksheet.md)，完整示例见 [`16-scenario-quick-start.md`](examples/16-scenario-quick-start.md)。

### 模拟器能力边界

新增脚本是**参数化硅样本模拟器**，不是 LLM 逐人扮演受访者的服务。它计算简化的 Cronbach's α、KMO、平行分析、PAF+Oblimin EFA 载荷/交叉载荷和 HTMT；不计算 ω、CITC、Bartlett 检验、CFA、CR、CFA-AVE、Fornell–Larcker、CMB 或效标关联效度。后续检验由 `psychometric-pretest` 按实际数据类型、同源数据和适用估计器完成。

## 核心方法原则

- 构念属性错置时先重审定义或调整构念归属，不用删题替代理论判断。
- “未接触/无法判断”按结构性缺失处理，不编码为最低分。
- EFA 与 CFA 使用预先固定的不同样本；候选版本沿用同一完整案例和分组。
- 默认以 PAF 和斜交旋转开展潜变量 EFA；不把 PCA 等同于共同因子 EFA。
- 删题同时考察统计诊断、理论角色、内容覆盖、题项冗余及跨群体适用性。

## 命令行快速安装

先安装 Node.js（提供 `npx`）。在终端中运行以下命令，可将全部 5 个 Skills 安装到检测到的支持平台：

这些命令从仓库默认分支安装。`upgrade/v1.1.0` 合并到默认分支后，命令会安装 V1.1.0；合并前默认分支仍是 V1.0。

```bash
npx skills add edsion12138/ai-questionnaire-pilot --all
```

也可以指定平台安装：

```bash
# Codex 平台
npx skills add edsion12138/ai-questionnaire-pilot --skill '*' --agent codex

# Claude Code 平台
npx skills add edsion12138/ai-questionnaire-pilot --skill '*' --agent claude-code

# Cursor 平台
npx skills add edsion12138/ai-questionnaire-pilot --skill '*' --agent cursor

# Gemini CLI 平台
npx skills add edsion12138/ai-questionnaire-pilot --skill '*' --agent gemini-cli

# GitHub Copilot 平台
npx skills add edsion12138/ai-questionnaire-pilot --skill '*' --agent github-copilot

# OpenCode 平台
npx skills add edsion12138/ai-questionnaire-pilot --skill '*' --agent opencode
```

默认安装到当前项目；添加 `-g` 可安装到用户级目录，例如：

```bash
npx skills add edsion12138/ai-questionnaire-pilot --skill '*' --agent codex -g
```

## 项目边界

本项目不连接外部 MCP 服务、不访问问卷平台，也不自动发放调查。
