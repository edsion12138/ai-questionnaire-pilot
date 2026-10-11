# AI Questionnaire Pilot V1.1 升级补丁（非完整仓库）

此包针对仓库 <https://github.com/edsion12138/ai-questionnaire-pilot> 当前V1.0构建。**不包含原有5个Skill的全部基础文件或二进制模板**，只包含新增脚本、方法文档、配置、测试以及升级合并器。

## 应用步骤

1. 从GitHub克隆/下载原有仓库，保留原目录结构。
2. 将本ZIP内容（包括 `apply_upgrade.py`、`skills/`、`examples/`、`tests/`）解压或复制到**仓库根目录**，允许合并同名目录；本补丁只带一个新Python脚本和新参考文件，不覆盖原有示例配置及代码。
3. 在仓库根目录运行 `python apply_upgrade.py`。它会备份被修改的原文本文件到同目录 `.bak-v1.0`，再补充README、4个Skill说明、CHANGELOG和plugin.json的1.1.0版本号；重复运行不会重复插入正文。
4. 安装分析依赖：`python -m pip install numpy scipy statsmodels`。运行 `python -m unittest discover -s tests -v`。
5. 运行 `python skills/silicon-sample-design/scripts/multiseed_sensitivity.py skills/silicon-sample-design/assets/example-multi-scenario-config.json --out demo16 --save-raw`。
6. 检查 `demo16/summary.json` 和 `runs_flat.csv`，并结合人工内容审核后提出候选。CFA及后续完整信效度需在既有psychometric-pretest工作流中完成。

## 版本发布建议

由于目前GitHub连接仅能读取目标仓库，创建分支返回403，本次未修改仓库main或建立PR。使用以上补丁先在本地新分支提交并创建PR。补丁代码已执行16轮示例冒烟测试，非真实问卷数据。

## 补丁结构

- `skills/silicon-sample-design/scripts/multiseed_sensitivity.py`
- `skills/silicon-sample-design/assets/example-multi-scenario-config.json`
- `skills/silicon-sample-design/references/multiseed-sensitivity-method.md`
- `skills/questionnaire-iteration/references/multiseed-decision-worksheet.md`
- `examples/16-scenario-quick-start.md`
- `tests/test_multiseed.py`
- `apply_upgrade.py`
- `README_升级补丁使用说明.md`

本项目可导出的Python模拟器为参数式合成响应压力测试模块，并非LLM真实受访者模拟。不得将生成指标称为“真实预测试验证结果”。
