# ASR Leaderboard

This repository contains a bilingual (English + Chinese) ASR evaluation leaderboard.

## Leaderboards
- English leaderboard: `asr-leaderboard/leaderboards/en.md`
- Chinese leaderboard: `asr-leaderboard/leaderboards/zh.md`

## Evaluation rules
- Rules and normalization: `asr-leaderboard/EVAL_RULES.md`

## How to submit results
1. Follow the mandatory rules in `asr-leaderboard/EVAL_RULES.md` (normalization + tokenization + metric definitions).
2. Add a new run folder under `asr-leaderboard/runs/YYYY-MM-DD_<model-name>/` including:
   - `README.md` describing model, decoding, segmentation, and artifact/commit.
   - (Optional) `refs/` and `hyps/` transcripts and `scores.md` for reproducibility.
3. Update the appropriate leaderboard table:
   - `asr-leaderboard/leaderboards/en.md`
   - `asr-leaderboard/leaderboards/zh.md`

## Directory layout
- `asr-leaderboard/EVAL_RULES.md`: single source of truth for evaluation policy
- `asr-leaderboard/leaderboards/`: leaderboard tables
- `asr-leaderboard/runs/`: per-run provenance
