# ASR Evaluation (EN WER + ZH CER)

This folder provides a minimal, reproducible scoring toolkit consistent with `../EVAL_RULES.md`.

## What it does
- English: normalization + **WER** (whitespace tokenization)
- Chinese: normalization + **CER** (character tokenization)
- Reports: S/D/I counts, N (reference tokens), and error rate %

## Input format
Two text files:
- `ref.txt`: one utterance per line
- `hyp.txt`: one utterance per line
Lines are matched by line number (1-to-1). Empty lines are allowed.

## Usage

### English WER
```bash
python asr-leaderboard/eval/score.py --lang en --ref path/to/ref.txt --hyp path/to/hyp.txt
```

### Chinese CER
```bash
python asr-leaderboard/eval/score.py --lang zh --ref path/to/ref.txt --hyp path/to/hyp.txt
```

### Example
```bash
python asr-leaderboard/eval/score.py --lang en --ref asr-leaderboard/eval/example/refs_en.txt --hyp asr-leaderboard/eval/example/hyps_en.txt
python asr-leaderboard/eval/score.py --lang zh --ref asr-leaderboard/eval/example/refs_zh.txt --hyp asr-leaderboard/eval/example/hyps_zh.txt
```

## Notes on rules
- EN normalization follows: lowercase, replace non `[a-z0-9 ]` with spaces, collapse spaces, trim.
- ZH normalization follows: full-width->half-width, remove spaces, remove punctuation, keep digits/latin, char tokenization.

For dataset download guidance, see `download_data.md` (documentation only, no redistribution).