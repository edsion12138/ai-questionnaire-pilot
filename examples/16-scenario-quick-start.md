# 16情景（12＋2＋2）入门

在仓库根目录安装 `numpy scipy statsmodels` 后运行：

```bash
python skills/silicon-sample-design/scripts/multiseed_sensitivity.py \
  skills/silicon-sample-design/assets/example-multi-scenario-config.json \
  --out demo16 --save-raw
```

- 12轮中等情景：只更换种子，题项参数**固定**；预留其中4个种子供方案选择后的复核。
- 2轮噪声压力：降低主载荷，提高方法因子及交叉载荷影响。
- 2轮高共同性：提高主载荷，降低方法因子及交叉载荷影响。
- 候选删题：`candidates`配置中写版本名和拟删除的原题号；**每轮同一份数据上比较版本**，并使用原题库完整案例，避免删题改变分析样本。

结果解读顺序：`summary.json` → `runs_flat.csv` → `runs.json` → `manifest.json` → 原始模拟CSV。注意 `summary.json` 只汇总EFA/α/HTMT等可计算的筛查指标；正式CFA、CR、AVE、Fornell–Larcker、CMB与效标效度属于下一阶段，不应声称本脚本完成。

## 本示例的意义

示例从原仓库的3因子、12题配置出发，重现16个独立随机实现，展示完整/删题两种以上方案如何进行**中位数、达标频率、噪声压力、高共同性上界**比较。它不能证明这3个因子在真实样本中存在，也不是复制职业本科39题量表的真实测量数据。

完整案例优先；如果某轮完整案例不足，输出 `insufficient_complete_cases`，不擅自插补。
