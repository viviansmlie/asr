import re
import unicodedata

_EN_KEEP_RE = re.compile(r"[^a-z0-9 ]+")  # everything except a-z, 0-9, space
_EN_SPACE_RE = re.compile(r"\s+")

def normalize_en(text: str) -> str:
    """
    English normalization per EVAL_RULES.md:
    1) lowercase
    2) replace non [a-z0-9 ] with spaces
    3) collapse spaces
    4) trim
    """
    if text is None:
        return ""
    t = text.lower()
    t = _EN_KEEP_RE.sub(" ", t)
    t = _EN_SPACE_RE.sub(" ", t).strip()
    return t


# A conservative punctuation remover for Chinese:
# - Normalize full-width to half-width via NFKC
# - Remove whitespace
# - Remove Unicode punctuation categories
# - Keep digits and latin letters as-is
def _is_punctuation(ch: str) -> bool:
    cat = unicodedata.category(ch)
    # P* are punctuation categories in Unicode
    if cat.startswith("P"):
        return True
    # Also treat some common symbols as punctuation-like
    if cat.startswith("S"):
        # Keep currency/math symbols? For leaderboard simplicity, remove symbols.
        return True
    return False

def normalize_zh(text: str) -> str:
    """
    Chinese normalization per EVAL_RULES.md:
    1) full-width -> half-width (NFKC)
    2) remove spaces
    3) remove Chinese/English punctuation
    4) keep digits and latin letters
    """
    if text is None:
        return ""
    t = unicodedata.normalize("NFKC", text)
    out = []
    for ch in t:
        if ch.isspace():
            continue
        if _is_punctuation(ch):
            continue
        out.append(ch)
    return "".join(out)