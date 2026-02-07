# Run: ExampleModel v1 (2026-02-07)

## Model
- Name: ExampleModel v1
- Artifact/Commit: abcdef1
- Params: 120M

## Decoding
- Decode: beam
- Beam size: 10
- LM: none
- Hotwords/Biasing: no

## Segmentation
- VAD: no
- Chunking: N/A

## Datasets evaluated
- English: LibriSpeech test-clean/test-other, TED-LIUM v3 test
- Chinese: AISHELL-1 test, HKUST test

## Outputs
- `refs/`: reference transcripts
- `hyps/`: hypothesis transcripts
- `scores.md`: scoring outputs (WER/CER)
