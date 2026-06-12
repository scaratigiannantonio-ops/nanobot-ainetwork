from aiohttp import web
import os
import openai
import replicate

async def handle_generate(request: web.Request) -> web.Response:
    """POST /api/generate"""
    try:
        body = await request.json()
        prompt = body.get("prompt", "")
    except Exception:
        return web.json_response({"error": "Invalid JSON"}, status=400)

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Sei un assistente specializzato in network marketing. Genera post coinvolgenti per social media. Massimo 150 parole. Includi sempre una call-to-action."},
            {"role": "user", "content": prompt}
        ]
    )
    
    text = response.choices[0].message.content
    resp = web.json_response({"text": text, "provider": "deepseek"})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


async def handle_avatar(request: web.Request) -> web.Response:
    """POST /api/avatar"""
    try:
        body = await request.json()
        image_url = body.get("imageUrl", "")
        text = body.get("text", "")
    except Exception:
        return web.json_response({"error": "Invalid JSON"}, status=400)

    api_key = os.environ.get("REPLICATE_API_KEY", "")
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    output = replicate.run(
        "sadtalker/sadtalker:3c1b0e4b5b8c0e0b0a0e9b8c5f9b0a7d7b0c4e5f8b0a1b3c5d7e9f0a1b3c5",
        input={
            "source_image": image_url,
            "text": text,
            "preprocess": "full",
            "still_mode": False,
            "use_enhancer": False
        }
    )
    
    resp = web.json_response({"videoUrl": output})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


async def handle_options(request: web.Request) -> web.Response:
    """Handle CORS preflight"""
    resp = web.Response()
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


def create_routes_app() -> web.Application:
    """Create the aiohttp sub-application for custom API routes."""
    app = web.Application()
    app.router.add_post("/generate", handle_generate)
    app.router.add_post("/avatar", handle_avatar)
    app.router.add_options("/generate", handle_options)
    app.router.add_options("/avatar", handle_options)
    return app
