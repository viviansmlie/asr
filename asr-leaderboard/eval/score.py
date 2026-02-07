import argparse
from dataclasses import dataclass
from typing import List, Tuple

from normalize import normalize_en, normalize_zh


@dataclass
class EditStats:
    S: int = 0
    D: int = 0
    I: int = 0
    N: int = 0  # reference token count

    @property
    def errors(self) -> int:
        return self.S + self.D + self.I

    @property
    def rate(self) -> float:
        return 0.0 if self.N == 0 else (self.errors / self.N) * 100.0


def _levenshtein_counts(ref: List[str], hyp: List[str]) -> Tuple[int, int, int]:
    """
    Return (S, D, I) counts to transform ref -> hyp.
    Classic DP; backtrace to count ops.
    """
    n = len(ref)
    m = len(hyp)

    # dp cost
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    bt = [[None] * (m + 1) for _ in range(n + 1)]  # 'ok','sub','del','ins'

    for i in range(1, n + 1):
        dp[i][0] = i
        bt[i][0] = "del"
    for j in range(1, m + 1):
        dp[0][j] = j
        bt[0][j] = "ins"

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                bt[i][j] = "ok"
            else:
                sub = dp[i - 1][j - 1] + 1
                dele = dp[i - 1][j] + 1
                ins = dp[i][j - 1] + 1
                best = min(sub, dele, ins)
                dp[i][j] = best
                if best == sub:
                    bt[i][j] = "sub"
                elif best == dele:
                    bt[i][j] = "del"
                else:
                    bt[i][j] = "ins"

    # backtrace
    i, j = n, m
    S = D = I = 0
    while i > 0 or j > 0:
        op = bt[i][j]
        if op == "ok":
            i -= 1
            j -= 1
        elif op == "sub":
            S += 1
            i -= 1
            j -= 1
        elif op == "del":
            D += 1
            i -= 1
        elif op == "ins":
            I += 1
            j -= 1
        else:
            # Should not happen
            break

    return S, D, I


def _read_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def score(lang: str, ref_lines: List[str], hyp_lines: List[str]) -> EditStats:
    if len(ref_lines) != len(hyp_lines):
        raise ValueError(f"Line count mismatch: ref={len(ref_lines)} hyp={len(hyp_lines)}")

    stats = EditStats()
    for r, h in zip(ref_lines, hyp_lines):
        if lang == "en":
            rn = normalize_en(r)
            hn = normalize_en(h)
            ref_toks = rn.split() if rn else []
            hyp_toks = hn.split() if hn else []
        elif lang == "zh":
            rn = normalize_zh(r)
            hn = normalize_zh(h)
            ref_toks = list(rn) if rn else []
            hyp_toks = list(hn) if hn else []
        else:
            raise ValueError("lang must be 'en' or 'zh'")

        S, D, I = _levenshtein_counts(ref_toks, hyp_toks)
        stats.S += S
        stats.D += D
        stats.I += I
        stats.N += len(ref_toks)

    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True, choices=["en", "zh"], help="en: WER, zh: CER")
    ap.add_argument("--ref", required=True, help="Reference text file, one utterance per line")
    ap.add_argument("--hyp", required=True, help="Hypothesis text file, one utterance per line")
    args = ap.parse_args()

    ref_lines = _read_lines(args.ref)
    hyp_lines = _read_lines(args.hyp)

    st = score(args.lang, ref_lines, hyp_lines)

    metric = "WER" if args.lang == "en" else "CER"
    print(f"lang={args.lang} metric={metric}")
    print(f"S={st.S} D={st.D} I={st.I} N={st.N}")
    print(f"{metric}={st.rate:.2f}%")

if __name__ == "__main__":
    main()