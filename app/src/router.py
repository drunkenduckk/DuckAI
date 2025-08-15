import re

LIVE_HINTS = [
    r"\b(weather|temperature|forecast)\b",
    r"\b(news|headline|trending)\b",
    r"\b(stock|price|flight|train|schedule|score)\b",
    r"\bnow\b",
]

def route(user: str):
    """
    Very simple router:
    - If looks like live data => 'live'
    - If very short or greeting => 'local'
    - Else => 'gpt'
    """
    text = (user or "").strip()
    if not text:
        return "local", "Empty message."

    for pat in LIVE_HINTS:
        if re.search(pat, text, flags=re.I):
            return "live", "Looks like live/real-time info."

    if len(text.split()) <= 2 or re.search(r"\b(hi|hello|hey)\b", text, re.I):
        return "local", "Short/greeting — handled locally."

    return "gpt", "General question — send to model."