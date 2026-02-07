# ASR Evaluation Rules (English + Chinese)

This document defines *mandatory* evaluation rules for the ASR leaderboards in this repository.
All submitted results must follow these rules; otherwise results are not comparable and may be rejected.

## 1. Metrics
- English: **WER (%)**
- Chinese: **CER (%)** (character error rate)

WER/CER is computed as: (Substitutions + Deletions + Insertions) / Number_of_reference_tokens * 100

## 2. Datasets & Splits (Fixed)
### English (Primary)
- LibriSpeech: `test-clean`, `test-other`
- TED-LIUM v3: `test`
- Hub5'00 (Switchboard): `Hub5'00` (report SWB / CH separately if available)

### Chinese (Primary)
- AISHELL-1: `test`
- HKUST: official test set

> If you add new datasets, you must add them to this file and backfill baseline models if needed.

## 3. Text Normalization (Mandatory)

### 3.1 English normalization (applies to BOTH ref and hyp)
1) Lowercase all text  
2) Remove punctuation (keep only letters/numbers/spaces)  
3) Collapse multiple spaces to a single space  
4) Trim leading/trailing spaces  
5) Do NOT expand numbers (e.g., "10" stays "10") unless explicitly stated for the whole leaderboard version  

Tokenization for WER: **whitespace tokenization** after normalization.

### 3.2 Chinese normalization (applies to BOTH ref and hyp)
1) Normalize full-width/half-width forms to **half-width**  
2) Remove all spaces  
3) Remove Chinese/English punctuation  
4) Keep digits and latin letters as-is (do not spell out)  
5) (Optional, only if needed) Convert Traditional -> Simplified consistently  

Tokenization for CER: **character-level** after normalization.

## 4. Decoding & Post-processing Disclosure (Required fields)
Each submission must disclose:
- Decode: greedy / beam
- Beam size (if beam)
- LM usage: none / n-gram / neural LM, and LM weight
- Hotwords / biasing: yes/no (describe if yes)
- VAD / segmentation strategy: yes/no (describe if yes)

## 5. Reproducibility (Required)
Each result must include:
- Model identifier + version (commit hash or model artifact hash)
- Evaluation script version (commit hash)
- Date
- Hardware summary (optional but recommended)

## 6. Result Format
Scores must be reported with 2 decimal places (e.g., 2.34).
If a metric is not applicable, use "N/A" (do not leave blank).
