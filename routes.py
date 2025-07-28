from fastapi import APIRouter, Request, Response, Cookie
from datetime import datetime
import uuid
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

@router.get("/get_token")
def get_token(response: Response, anonymous_token: str = Cookie(None)):
    if not anonymous_token:
        token = str(uuid.uuid4())
        response.set_cookie(key="anonymous_token", value=token, httponly=True, samesite="lax")
    else:
        token = anonymous_token
    return {"token": token}

@router.post("/chat")
async def chat_endpoint(request: Request, anonymous_token: str = Cookie(None)):
    if not anonymous_token:
        return {"response": "No session token. Please refresh page."}
    data = await request.json()
    user_message = data["message"]

    # OpenAI ile yanıt
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
