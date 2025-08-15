import os
import httpx
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL_ID", "gpt-oss-20b")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

class OpenRouterClient:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENROUTER_API_KEY in environment. Put it in a .env file.")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Router App",
        }
        # Single client with sane timeouts; no retries here to keep it simple
        self.client = httpx.Client(timeout=httpx.Timeout(30.0, read=60.0))

    def chat(self, messages, model: str | None = None) -> str:
        payload = {
            "model": model or DEFAULT_MODEL,
            "messages": messages,
        }
        try:
            resp = self.client.post(BASE_URL, headers=self.headers, json=payload)
            # Raise for non-2xx to surface clear errors
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            # Return a concise error that UI can show
            return f"OpenRouter HTTP error {e.response.status_code}: {e.response.text[:400]}"
        except Exception as e:
            return f"OpenRouter request failed: {e}"
