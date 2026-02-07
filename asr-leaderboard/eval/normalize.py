import re
import unicodedata
from typing import Optional

try:
    from opencc import OpenCC
except Exception:  # pragma: no cover
    OpenCC = None

_EN_KEEP_RE = re.compile(r"[^a-z0-9 ]+")
_EN_SPACE_RE = re.compile(r"\s+")

def normalize_en(text: Optional[str]) -> str:
    """
    EN normalization:
    - lowercase
    - replace non [a-z0-9 ] with spaces
    - collapse spaces
    - trim
    """
    if not text:
        return ""
    t = text.lower()
    t = _EN_KEEP_RE.sub(" ", t)
    t = _EN_SPACE_RE.sub(" ", t).strip()
    return t


def _is_punctuation_or_symbol(ch: str) -> bool:
    cat = unicodedata.category(ch)
    # P* punctuation, S* symbols
    return cat.startswith("P") or cat.startswith("S")


class ZhNormalizer:
    """
    ZH normalization:
    - NFKC (full-width -> half-width)
    - remove spaces
    - remove punctuation/symbols
    - Traditional -> Simplified (enabled by default)
    """
    def __init__(self, t2s: bool = True):
        self.t2s = t2s
        self._cc = None
        if self.t2s:
            if OpenCC is None:
                raise RuntimeError(
                    "opencc is required for Traditional->Simplified conversion. "
                    "Install: pip install opencc-python-reimplemented"
                )
            # t2s: Traditional Chinese to Simplified Chinese
            self._cc = OpenCC("t2s")

    def __call__(self, text: Optional[str]) -> str:
        if not text:
            return ""
        t = unicodedata.normalize("NFKC", text)
        out = []
        for ch in t:
            if ch.isspace():
                continue
            if _is_punctuation_or_symbol(ch):
                continue
            out.append(ch)
        t = "".join(out)
        if self._cc is not None:
            t = self._cc.convert(t)
        return t