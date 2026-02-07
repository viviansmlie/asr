# English ASR Leaderboard

Evaluation rules: see `../EVAL_RULES.md`

## Datasets
- LibriSpeech: test-clean / test-other
- TED-LIUM v3: test
- Hub5'00: SWB / CH (if you report Hub5'00)

## Leaderboard (WER %, lower is better)

| Model | Params | Decode | LM | LibriSpeech test-clean | LibriSpeech test-other | TED-LIUM v3 test | Hub5'00 SWB | Hub5'00 CH | Date | Artifact/Commit | Notes |
|------|--------|--------|----|-------------------------|------------------------|------------------|-------------|------------|------|------------------|-------|
| Baseline (fill me) | N/A | greedy | none | N/A | N/A | N/A | N/A | N/A | YYYY-MM-DD | link-or-hash | normalization per rules |

## Notes
- All scores must follow the normalization/tokenization rules in `EVAL_RULES.md`.
- If Hub5'00 is not evaluated, set SWB/CH as N/A.
