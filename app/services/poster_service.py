from typing import List, Optional
from app.core.interfaces import ImageGenerator, StorageProvider

class PosterService:
    """
    Orchestrates the poster generation process.
    Depends on abstractions (ImageGenerator & StorageProvider) rather than concrete classes (DIP).
    This handles SRP by focusing only on orchestration.
    """
    def __init__(self, generators: List[ImageGenerator], storage: StorageProvider):
        self.generators = generators
        self.storage = storage

    def create_poster(self, prompt: str) -> Optional[str]:
        """
        Tries each generator in order until one succeeds.
        Saves via the injected storage provider (Disk, G-Drive, etc).
        """
        for generator in self.generators:
            print(f"Attempting generation with: {generator.provider_name}")
            image_data = generator.generate(prompt)
            
            if image_data:
                # Use the injected storage provider to persist the image
                filename_or_id = self.storage.save_image(
                    image_data, 
                    prefix=generator.provider_name[:3].lower()
                )
                return filename_or_id
                
        return None
