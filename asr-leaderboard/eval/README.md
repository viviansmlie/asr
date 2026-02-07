# ASR Evaluation Toolkit (EN WER + ZH CER)

This toolkit is consistent with `../../asr-leaderboard/EVAL_RULES.md` and supports:
- Input format: `utt_id<TAB>text`
- Alignment: join by `utt_id`
- English: WER (whitespace tokens after normalization)
- Chinese: CER (character tokens after normalization), **Traditional->Simplified enabled by default**
- Batch evaluation via YAML config, and output Markdown rows for leaderboards

## Install
```bash
pip install -r asr-leaderboard/eval/requirements.txt
```

## Quick test (toy examples)
```bash
python asr-leaderboard/eval/score.py --lang en \
  --ref asr-leaderboard/eval/example/ref_en.tsv \
  --hyp asr-leaderboard/eval/example/hyp_en.tsv

python asr-leaderboard/eval/score.py --lang zh \
  --ref asr-leaderboard/eval/example/ref_zh.tsv \
  --hyp asr-leaderboard/eval/example/hyp_zh.tsv
```

## Run multiple datasets (YAML)
1) Copy example config:
```bash
cp asr-leaderboard/eval/config.example.yaml my_eval.yaml
```

2) Edit paths in `my_eval.yaml` (refs/hyps prepared by you)

3) Run:
```bash
python asr-leaderboard/eval/run_eval.py --config my_eval.yaml
```

It will print:
- Per-task S/D/I/N + WER/CER
- A Markdown table row you can paste into:
  - `asr-leaderboard/leaderboards/en.md`
  - `asr-leaderboard/leaderboards/zh.md`

## Data
This repo does NOT redistribute LibriSpeech/TED-LIUM/AISHELL/HKUST/Hub5'00.
Use official sources and licenses; prepare `ref.tsv` and `hyp.tsv` files in the required format.
See `prepare_data.py` for format helpers.