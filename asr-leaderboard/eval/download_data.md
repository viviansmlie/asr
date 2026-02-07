# How to obtain evaluation datasets (documentation only)

This repo does **not** redistribute datasets. Please obtain them from official sources and follow their licenses.

## English
### LibriSpeech
- Official site: http://www.openslr.org/12
- Common evaluation splits: test-clean, test-other

### TED-LIUM v3
- Official site: http://www.openslr.org/51
- Common evaluation split: test

### Hub5'00 / Switchboard
- Typically LDC licensed; obtain via LDC.
- Common evaluation: Hub5'00 (SWB/CH)

## Chinese
### AISHELL-1
- Official site: http://www.openslr.org/33
- Evaluation split: test

### HKUST
- Commonly distributed via LDC (licensed).
- Use official test split.

## What you need for scoring
For each dataset split, prepare:
- `ref.txt`: reference transcript, one utterance per line
- `hyp.txt`: model output transcript, one utterance per line

If you have utterance IDs, you may store `utt_id<TAB>text` lines, but then you must pre-join or align them into the same line order before using `score.py` (this toolkit assumes line-by-line alignment).