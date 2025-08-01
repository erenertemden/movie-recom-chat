from fastapi import APIRouter, Request
from datetime import datetime
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data["message"]

    system_prompt = "You are a helpful movie recommendation assistant. Always answer concisely."
    
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150,
        temperature=0.7
    )

    response_text = completion.choices[0].message.content.strip()
    
    return {"response": response_text}
