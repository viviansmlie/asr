import argparse
from dataclasses import dataclass
from typing import Dict, List, Tuple

from normalize import ZhNormalizer, normalize_en


@dataclass
class EditStats:
    S: int = 0
    D: int = 0
    I: int = 0
    N: int = 0

    @property
    def errors(self) -> int:
        return self.S + self.D + self.I

    @property
    def rate(self) -> float:
        return 0.0 if self.N == 0 else (self.errors / self.N) * 100.0


def read_tsv_utt_text(path: str) -> Dict[str, str]:
    """
    Read lines of the form: utt_id<TAB>text
    Empty text is allowed.
    """
    data: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if not line:
                continue
            if "\t" not in line:
                raise ValueError(f"{path}:{ln}: expected TAB-separated 'utt_id\\ttext'")
            utt, text = line.split("\t", 1)
            utt = utt.strip()
            if not utt:
                raise ValueError(f"{path}:{ln}: empty utt_id")
            data[utt] = text
    return data


def join_by_utt(ref: Dict[str, str], hyp: Dict[str, str]) -> List[Tuple[str, str, str]]:
    """
    Return aligned list (utt, ref_text, hyp_text).
    Only utterances present in ref are scored; missing hyp -> empty string.
    """
    aligned = []
    for utt, r in ref.items():
        h = hyp.get(utt, "")
        aligned.append((utt, r, h))
    return aligned


def _levenshtein_counts(ref: List[str], hyp: List[str]) -> Tuple[int, int, int]:
    n = len(ref)
    m = len(hyp)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    bt = [[None] * (m + 1) for _ in range(n + 1)]

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
                bt[i][j] = "sub" if best == sub else ("del" if best == dele else "ins")

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
            break
    return S, D, I


def score(lang: str, ref_path: str, hyp_path: str, zh_t2s: bool = True) -> EditStats:
    ref = read_tsv_utt_text(ref_path)
    hyp = read_tsv_utt_text(hyp_path)
    aligned = join_by_utt(ref, hyp)

    zh_norm = ZhNormalizer(t2s=zh_t2s) if lang == "zh" else None

    stats = EditStats()
    for _, r, h in aligned:
        if lang == "en":
            rn = normalize_en(r)
            hn = normalize_en(h)
            ref_toks = rn.split() if rn else []
            hyp_toks = hn.split() if hn else []
        elif lang == "zh":
            rn = zh_norm(r)  # type: ignore[misc]
            hn = zh_norm(h)  # type: ignore[misc]
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
    ap.add_argument("--lang", required=True, choices=["en", "zh"])
    ap.add_argument("--ref", required=True)
    ap.add_argument("--hyp", required=True)
    ap.add_argument("--zh-t2s", action="store_true", default=True,
                    help="Enable Traditional->Simplified for Chinese (default: enabled).")
    ap.add_argument("--no-zh-t2s", dest="zh_t2s", action="store_false",
                    help="Disable Traditional->Simplified for Chinese.")
    args = ap.parse_args()

    st = score(args.lang, args.ref, args.hyp, zh_t2s=args.zh_t2s)
    metric = "WER" if args.lang == "en" else "CER"
    print(f"lang={args.lang} metric={metric}")
    print(f"S={st.S} D={st.D} I={st.I} N={st.N}")
    print(f"{metric}={st.rate:.2f}%")

if __name__ == "__main__":
    main()