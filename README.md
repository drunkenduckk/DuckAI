# Ready AI Router (FastAPI + OpenRouter)

A minimal, ready-to-run web chat app that talks to an AI model via the OpenRouter API.
You said you use **gpt-oss-20b** — this project lets you set the model with an env var.

## 1) Quick start

```bash
# 0) Unzip the folder
cd ready-ai-router

# 1) Create and activate a virtual env (recommended)
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Create your .env
cp .env.example .env  # or copy manually on Windows
# Edit .env to set your OPENROUTER_API_KEY and MODEL_ID

# 4) Run
uvicorn app.web.app:app --reload --port 8000
```
Open http://localhost:8000 in your browser.


```bash
# 0) Unzip the folder
cd ready-ai-router

# 1) Create and activate a virtual env (recommended)
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Create your .env from the example
copy .env.example .env   # Windows
# or
cp .env.example .env     # macOS/Linux

# 4) Edit .env and set your OPENROUTER_API_KEY and MODEL_ID (e.g., gpt-oss-20b)

# 5) Run the app
uvicorn app.web.app:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your browser.

## 2) API

- `POST /chat` with JSON `{ "message": "Hello" }`
- Response: `{ "reply": "...", "route": "gpt|local|live", "reason": "..." }`

## 3) Notes

- Uses **httpx directly (no OpenAI SDK). Works with any OpenRouter model ID.
- Put exactly the model name you want in `MODEL_ID` (e.g., `gpt-oss-20b`).
- If you get 401/403 errors, your key is missing or invalid.
- If you get 404/422 from OpenRouter, the `MODEL_ID` may be wrong or not accessible to your key.