import requests
import uuid
from typing import Optional
from urllib.parse import quote
from app.core.interfaces import ImageGenerator

class PollinationsImageProvider(ImageGenerator):
    """
    Pollinations.ai fallback implementation of ImageGenerator.
    """
    def __init__(self, model: str = "flux"):
        self.model = model

    @property
    def provider_name(self) -> str:
        return "Pollinations (AI Fallback)"

    def generate(self, prompt: str) -> Optional[bytes]:
        try:
            encoded_prompt = quote(prompt)
            seed = uuid.uuid4().int % 1000000
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&model={self.model}&nologo=true"
            
            response = requests.get(url, timeout=60)
            
            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                return response.content
        except Exception as e:
            print(f"PollinationsProvider Error: {e}")
            
        return None
