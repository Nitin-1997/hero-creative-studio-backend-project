from typing import Optional
from app.core.interfaces import ImageGenerator

class LocalPlaceholderProvider(ImageGenerator):
    """
    Emergency fallback that returns a pre-existing placeholder image 
    if all AI services fail. Ensures the API never returns a 500/error.
    """
    def __init__(self, placeholder_path: str = "app/static/placeholder_bike.png"):
        self.placeholder_path = placeholder_path

    @property
    def provider_name(self) -> str:
        return "Local Placeholder (Emergency)"

    def generate(self, prompt: str) -> Optional[bytes]:
        try:
            import os
            if os.path.exists(self.placeholder_path):
                with open(self.placeholder_path, "rb") as f:
                    return f.read()
            
            # If no file, try to generate a tiny red square or similar via PIL
            from PIL import Image
            import io
            img = Image.new('RGB', (1024, 1024), color = (237, 28, 36)) # Hero Red
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        except:
            return None
