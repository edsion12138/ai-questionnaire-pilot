#!/usr/bin/env python3
"""Safely integrate the v1.1 delta into the *existing* ai-questionnaire-pilot repo.

Run FROM repository root after copying the delta tree into the repo, e.g.:
   python apply_upgrade.py

Idempotent: the same marker is never appended twice. Existing code and templates
remain unchanged; creates .bak-v1.0 copies for original text files before writing.
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MARKER='<!-- MULTISEED-V1.1 -->'
README_SECTION=f'''\n{MARKER}
## V1.1：12＋2＋2多种子稳定性与测量压力测试

本版新增**固定12个中等测量清晰度种子＋2个高噪声种子＋2个高共同性种子**的情景分析协议：为所有版本保留固定题目参数、背景分层、完整案例和探索/验证分组，在同一响应实现上比较候选删题方案；同时汇总中位数、极值、达标次数，并按8个开发种子与4个保留种子分别输出结果。绝不自动挑选表现最好的随机种子。

```bash
python skills/silicon-sample-design/scripts/multiseed_sensitivity.py \\
  skills/silicon-sample-design/assets/example-multi-scenario-config.json \\
  --out demo16 --save-raw
```

- **方法详解**：`skills/silicon-sample-design/references/multiseed-sensitivity-method.md`
- **删题审查表**：`skills/questionnaire-iteration/references/multiseed-decision-worksheet.md`
- **运行示例**：`examples/16-scenario-quick-start.md`

新脚本是**参数化硅样本模拟器**，不是LLM逐个扮演受访者的服务；用于比较测量情景敏感性。它生成EFA、KMO、平行分析、α和HTMT等筛查结果，**不自动计算CFA、CR、CFA-AVE、Fornell–Larcker、CMB或效标关联效度**；这些步骤仍必须在 `psychometric-pretest` 中按正确的估计器和同源数据完成。运行结果不能宣称为真人实证检验。
'''
SKILL_SNIPPETS={
 'skills/silicon-sample-design/SKILL.md':f'''\n{MARKER}
## 12＋2＋2情景稳定性工作流（v1.1，可选增强）

在初步结构通过内容审查之后，可以预先设定12个中等测量清晰度种子、2个高噪声种子、2个高共同性种子，固定每道题的生成参数，观察模型对随机实现与参数变化的敏感性。先用8个中等种子提出删题候选，再在4个**未参与筛选**的中等种子与4个压力/乐观情景种子上复核。所有版本须在每轮同一份数据和同一固定探索/验证分组上比较，完整案例依据原始题库一次确定，不能因为删题造成N改变。报告中位数、范围、达标次数与失败条件，禁止自动择优随机种子、后验抬高载荷，禁止把恢复预设因子解释为真实构念验证。根据问卷内容维度进行人工修订，不用统计阈值代替内容覆盖。详见 `references/multiseed-sensitivity-method.md`；运行 `scripts/multiseed_sensitivity.py`。**此脚本为参数生成器而非LLM API；CFA/CR/AVE等另行验证。**
''',
 'skills/questionnaire-iteration/SKILL.md':f'''\n{MARKER}
## 多种子版本比较增强（v1.1）

对候选删题版先提供12轮中等情景指标的中位数、最小最大值及达标轮数，再附2轮噪声压力与2轮较高共同性结果。提高中等情景表现却在噪声下崩溃，属于敏感候选；只在较高共同性下“通过”，不构成真实有效的证据。优先以8个开发种子决定候选并锁定版本，4个保留种子用于后续复核，不应再重新优化并声称独立验证。请按 `references/multiseed-decision-worksheet.md` 记录每个删除题项的独特侧面损失，并以研究者的理论/内容审查为最终决策。禁止按单一AVA/CFI指标或最漂亮模拟轮次自动筛选。
''',
 'skills/psychometric-pretest/SKILL.md':f'''\n{MARKER}
## 分析来源与情景敏感性（v1.1）

如收到16轮参数化硅样本结果，先识别是否仅完成了EFA/KMO/α/HTMT筛查。**不要把EFA主载荷平方当成CFA-AVE**，也不要把预设生成载荷作为已估计的标准化载荷；CFA、CR、Fornell–Larcker、单因子CFA、效标与CMB同源检验需要独立分析阶段完成。每轮都固定探索/验证组，保留真实样本完整案例定义，按核心能力/影响因素分别做EFA和CFA；效标单独建分并做外部相关。详见 `../silicon-sample-design/references/multiseed-sensitivity-method.md`。
''',
 'skills/validation-report/SKILL.md':f'''\n{MARKER}
## 16情景稳定性表格（v1.1）

当使用12＋2＋2模式时，增设：①冻结情景参数与预声明16个随机种子；②各轮样本完整性及固定拆分；③同一轮候选版本对比；④12轮中位数、极值及达标频率；⑤2轮噪声与2轮高共同性情景；⑥8开发/4留出种子；⑦删题内容覆盖损失；⑧不可计算或暂缓的人类效度指标及后续复核计划。失败条件必须与通过条件同样展示，不允许只展示最优轮次。
''',
}

def update_text(path, original, patched):
 if original==patched:
  print('unchanged',path)
  return
 backup=path.with_name(path.name+'.bak-v1.0')
 if not backup.exists(): shutil.copy2(path,backup)
 path.write_text(patched,encoding='utf-8')
 print('updated',path.relative_to(ROOT))

def main():
 readme=ROOT/'README.md'
 if not readme.exists() or not (ROOT/'skills/questionnaire-iteration/SKILL.md').exists():
  raise SystemExit('Place this delta in the existing ai-questionnaire-pilot repository root first.')
 before=readme.read_text(encoding='utf-8')
 after=before.replace('# AI Questionnaire Pilot v1.0','# AI Questionnaire Pilot v1.1',1)
 after=after.replace('## V1.0 的边界','## 当前版本的边界',1)
 if MARKER not in after:after+=README_SECTION
 update_text(readme,before,after)
 for rel,snippet in SKILL_SNIPPETS.items():
  path=ROOT/rel
  if not path.is_file():raise SystemExit(f'Required skill missing: {rel}')
  before=path.read_text(encoding='utf-8')
  if MARKER not in before:update_text(path,before,before.rstrip()+'\n'+snippet)
 plugin=ROOT/'plugin.json'
 data=json.loads(plugin.read_text(encoding='utf-8'))
 if data.get('version')!='1.1.0':
  before=plugin.read_text(encoding='utf-8');data['version']='1.1.0'
  update_text(plugin,before,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 change=ROOT/'CHANGELOG.md';before=change.read_text(encoding='utf-8')
 entry='''## 1.1.0\n- 添加预注册12＋2＋2随机种子×情景敏感性模拟和8＋4种子留出审计。\n- 添加多轮固定完整案例、固定分层拆分及候选删题同数据比较脚本。\n- 增补构念迁移、内容覆盖、跨专业能力侧面及参数敏感性方法说明。\n- 明确参数式生成与LLM persona、真人实证的边界；CFA等指标保留后续分析接口。\n\n'''
 if '## 1.1.0' not in before:
  after=before.replace('# Changelog\n','# Changelog\n\n'+entry,1)
  update_text(change,before,after)
 print('Upgrade complete. Existing scripts and example templates preserved.')

if __name__=='__main__':main()
