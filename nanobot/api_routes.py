from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import openai

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    provider: str = "deepseek"

@app.post("/api/generate")
async def generate(req: GenerateRequest):
    # Usa DeepSeek per generare il post
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Sei un assistente specializzato in network marketing. Genera post coinvolgenti per social media."},
            {"role": "user", "content": req.prompt}
        ]
    )
    
    text = response.choices[0].message.content
    return {"text": text, "provider": "deepseek"}
