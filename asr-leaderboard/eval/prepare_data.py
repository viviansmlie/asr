"""
Helpers for preparing scoring TSV files.

This file intentionally does NOT download or redistribute datasets.
It only documents expected formats and provides small utilities.

Expected TSV line format:
    utt_id<TAB>text

You should generate:
- ref.tsv from official transcripts
- hyp.tsv from your model outputs
and ensure they share the same utt_id set.
"""

from typing import Iterable, Tuple

def write_tsv(path: str, items: Iterable[Tuple[str, str]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for utt, text in items:
            f.write(f"{utt}\t{text}\n")