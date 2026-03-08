from typing import List, Optional
from app.core.interfaces import ImageGenerator
from app.services.storage_service import StorageService

class PosterService:
    """
    Orchestrates the poster generation process.
    Depends on abstractions (ImageGenerator) rather than concrete classes (DIP).
    """
    def __init__(self, generators: List[ImageGenerator], storage: StorageService):
        self.generators = generators
        self.storage = storage

    def create_poster(self, prompt: str) -> Optional[str]:
        """
        Tries each generator in order until one succeeds.
        """
        for generator in self.generators:
            print(f"Attempting generation with: {generator.provider_name}")
            image_bytes = generator.generate(prompt)
            
            if image_bytes:
                # If bytes is actually a PIL object (as some SDKs return), we handle that in storage or here
                # Let's assume bytes for now as defined in interface
                filename = self.storage.save_image(image_bytes, prefix=generator.provider_name[:3].lower())
                return filename
                
        return None
