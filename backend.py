from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set up FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class Query(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

# Create API clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)

groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

@app.post("/chat")
async def chat(request: Request):
    try:
        payload = await request.json()
        query = Query(**payload)
    except Exception as e:
        return {"error": f"❌ Invalid request format: {str(e)}"}

    # Format messages for chat
    messages = []
    for idx, msg in enumerate(query.messages):
        role = "user" if idx % 2 == 0 else "assistant"
        messages.append({"role": role, "content": msg})

    # Prepend system prompt
    messages.insert(0, {"role": "system", "content": query.system_prompt})

    try:
        if query.model_provider.lower() == "openai":
            response = openai_client.chat.completions.create(
                model=query.model_name,
                messages=messages,
                temperature=0.7
            )
            final_message = response.choices[0].message.content

        elif query.model_provider.lower() == "groq":
            response = groq_client.chat.completions.create(
                model=query.model_name,
                messages=messages,
                temperature=0.7
            )
            final_message = response.choices[0].message.content

        else:
            return {"error": f"❌ Unsupported model provider: {query.model_provider}"}

        return {
            "model": query.model_name,
            "provider": query.model_provider,
            "message": final_message,
            "prompt": query.system_prompt,
            "history": query.messages + [final_message]
        }

    except Exception as e:
        return {"error": f"❌ API call failed: {str(e)}"}
