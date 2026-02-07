import argparse
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import yaml

from score import score


@dataclass
class TaskResult:
    key: str
    lang: str
    metric: str
    rate: float
    S: int
    D: int
    I: int
    N: int


def _load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _metric(lang: str) -> str:
    return "WER" if lang == "en" else "CER"


def run(config: Dict[str, Any]) -> List[TaskResult]:
    defaults = config.get("defaults", {})
    zh_t2s = bool(defaults.get("zh_t2s", True))

    tasks = config.get("tasks", [])
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("config must contain a non-empty list: tasks")

    results: List[TaskResult] = []
    for t in tasks:
        key = t["key"]              # e.g., "librispeech_test_clean"
        lang = t["lang"]            # "en" or "zh"
        ref = t["ref"]
        hyp = t["hyp"]

        st = score(lang, ref, hyp, zh_t2s=zh_t2s)
        results.append(TaskResult(
            key=key,
            lang=lang,
            metric=_metric(lang),
            rate=st.rate,
            S=st.S, D=st.D, I=st.I, N=st.N
        ))
    return results


def _fmt_rate(x: Optional[float]) -> str:
    return "N/A" if x is None else f"{x:.2f}"


def render_markdown_rows(config: Dict[str, Any], results: List[TaskResult]) -> str:
    meta = config.get("meta", {})
    model = meta.get("model", "MODEL_NAME")
    params = meta.get("params", "N/A")
    decode = meta.get("decode", "greedy")
    lm = meta.get("lm", "none")
    date = meta.get("date", "YYYY-MM-DD")
    artifact = meta.get("artifact", "commit-or-hash")
    notes = meta.get("notes", "")

    # Build dict for lookup
    rmap = {r.key: r for r in results}

    # English row (matches leaderboards/en.md columns)
    en_keys = config.get("render", {}).get("en_order", [])
    if not en_keys:
        en_keys = [
            "librispeech_test_clean",
            "librispeech_test_other",
            "tedlium3_test",
            "hub5_00_swb",
            "hub5_00_ch",
        ]
    en_vals = []
    for k in en_keys:
        rr = rmap.get(k)
        en_vals.append(_fmt_rate(rr.rate if rr else None))

    en_row = (
        f"| {model} | {params} | {decode} | {lm} | "
        + " | ".join(en_vals)
        + f" | {date} | {artifact} | {notes} |"
    )

    # Chinese row (matches leaderboards/zh.md columns)
    zh_keys = config.get("render", {}).get("zh_order", [])
    if not zh_keys:
        zh_keys = ["aishell1_test", "hkust_test"]
    zh_vals = []
    for k in zh_keys:
        rr = rmap.get(k)
        zh_vals.append(_fmt_rate(rr.rate if rr else None))

    zh_row = (
        f"| {model} | {params} | {decode} | {lm} | "
        + " | ".join(zh_vals)
        + f" | {date} | {artifact} | {notes} |"
    )

    return "\n".join([
        "## Markdown rows (copy/paste)",
        "",
        "### English leaderboard row",
        en_row,
        "",
        "### Chinese leaderboard row",
        zh_row,
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = _load_yaml(args.config)
    results = run(cfg)

    print("## Results")
    for r in results:
        print(f"- {r.key} ({r.lang} {r.metric}): {r.rate:.2f}%  [S={r.S} D={r.D} I={r.I} N={r.N}]")

    print("")
    print(render_markdown_rows(cfg, results))


if __name__ == "__main__":
    main()