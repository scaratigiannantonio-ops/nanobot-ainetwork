from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import openai
import replicate

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    provider: str = "deepseek"

class AvatarRequest(BaseModel):
    imageUrl: str
    text: str

@app.post("/api/generate")
async def generate(req: GenerateRequest):
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Sei un assistente specializzato in network marketing. Genera post coinvolgenti per social media. Massimo 150 parole. Includi sempre una call-to-action."},
            {"role": "user", "content": req.prompt}
        ]
    )
    
    text = response.choices[0].message.content
    return {"text": text, "provider": "deepseek"}

@app.post("/api/avatar")
async def avatar(req: AvatarRequest):
    api_key = os.environ.get("REPLICATE_API_KEY", "")
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    output = replicate.run(
        "sadtalker/sadtalker:3c1b0e4b5b8c0e0b0a0e9b8c5f9b0a7d7b0c4e5f8b0a1b3c5d7e9f0a1b3c5",
        input={
            "source_image": req.imageUrl,
            "text": req.text,
            "preprocess": "full",
            "still_mode": False,
            "use_enhancer": False
        }
    )
    
    return {"videoUrl": output}
