import replicate
import os

async def generate_avatar_video(image_url, text, api_key):
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    output = replicate.run(
        "sadtalker/sadtalker:3c1b0e4b5b8c0e0b0a0e9b8c5f9b0a7d7b0c4e5f8b0a1b3c5d7e9f0a1b3c5",
        input={
            "source_image": image_url,
            "driven_audio": None,
            "text": text,
            "preprocess": "full",
            "still_mode": False,
            "use_enhancer": False
        }
    )
    
    return output
