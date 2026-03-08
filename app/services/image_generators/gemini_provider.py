import os
from typing import Optional
from google import genai
from google.genai import types
from app.core.interfaces import ImageGenerator

class GeminiImageProvider(ImageGenerator):
    """
    Google Gemini (Imagen) implementation of ImageGenerator.
    """
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._client = None
        if api_key and "your_gemini_api_key_here" not in api_key:
            self._client = genai.Client(api_key=api_key)

    @property
    def provider_name(self) -> str:
        return "Gemini (Imagen)"

    def generate(self, prompt: str) -> Optional[bytes]:
        if not self._client:
            return None

        try:
            # We preferentially use the 3.0 stable model
            response = self._client.models.generate_images(
                model="imagen-3.0-generate-001",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type='image/png'
                )
            )
            
            if response.generated_images:
                gen_image = response.generated_images[0]
                # Extract bytes based on SDK object structure
                if hasattr(gen_image.image, 'image_bytes'):
                    return gen_image.image.image_bytes
                return gen_image.image # Sometimes it's direct bytes or a PIL-like object
        except Exception as e:
            print(f"GeminiProvider Error: {e}")
            return None
        
        return None
