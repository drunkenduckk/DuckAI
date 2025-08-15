"""
A tiny "local knowledge base" placeholder.
Replace the ENTRIES dict with your own pairs or plug a real vector DB.
"""
ENTRIES = {
    "hi": "Hey! How can I help you today?",
    "hello": "Hello! What can I do for you?",
    "help": "Ask me anything. For live data like weather or prices, integrate a provider.",
}

def lookup(q: str):
    ql = (q or "").strip().lower()
    return ENTRIES.get(ql)