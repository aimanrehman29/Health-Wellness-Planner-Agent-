import sys
import os
import requests
import json
from agents import Runner, RunContextWrapper
from context import UserSessionContext
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = "https://openrouter.ai/api/v1"
model = "deepseek/deepseek-r1-0528:free"

def get_openrouter_response(user_input):
    """Function to make a request to OpenRouter API and get the response."""
    url = f"{base_url}/chat/completions" 

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Prepare the payload
    data = {
        "model": model,
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 1000,  
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

async def stream_response(
    agent, 
    prompt: str,
    ctx: RunContextWrapper[UserSessionContext],
) -> None:
    """ Stream real-time responses from the agent. """
    response = get_openrouter_response(prompt)  

    sys.stdout.write("\nAssistant: ")
    sys.stdout.write(response)  
    sys.stdout.flush()



