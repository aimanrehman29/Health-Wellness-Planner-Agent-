import sys
import os
import requests
import json
from agents import RunContextWrapper
from context import UserSessionContext
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY") or "sk-or-..."
base_url = "https://openrouter.ai/api/v1"
model = "google/gemini-2.5-flash-lite-preview-06-17"  # or any other model you want

def get_openrouter_response(user_input: str) -> str:
    """Make a POST request to OpenRouter API and return the assistant response."""
    url = f"{base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 1000,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error contacting OpenRouter API: {e}"

async def stream_response(
    agent, 
    prompt: str,
    ctx: RunContextWrapper[UserSessionContext],
) -> None:
    """
    Simulate a streamed response from the OpenRouter model using a single call.
    You can improve it further by breaking long outputs into chunks.
    """
    print("\nAssistant: ", end="")
    response = get_openrouter_response(prompt)
    print(response)
    sys.stdout.flush()
