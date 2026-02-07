# 中文 ASR 榜单（Chinese ASR Leaderboard）

评测规则见：`../EVAL_RULES.md`

## 数据集
- AISHELL-1: test
- HKUST: official test set

## Leaderboard（CER %, 越低越好）

| 模型 | 参数量 | 解码 | LM | AISHELL-1 test | HKUST test | 日期 | Artifact/Commit | 备注 |
|------|--------|------|----|----------------|------------|------|------------------|------|
| Baseline（待填写） | N/A | greedy | none | N/A | N/A | YYYY-MM-DD | link-or-hash | 按规则做 normalization |

## 备注
- 中文默认使用 CER（按字符），并执行统一的标点/空白清理与全半角归一化。
- 若你坚持中文 WER（分词后按词），必须在 `EVAL_RULES.md` 中新增明确分词器与版本，并对全榜单一致执行。
