import os
import uuid

class StorageService:
    """
    Handles file system operations. 
    Single Responsibility: Persisting generated assets.
    """
    def __init__(self, base_directory: str = "generated_images"):
        self.base_directory = base_directory
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)

    def save_image(self, image_bytes: bytes, prefix: str = "gen") -> str:
        """
        Saves image bytes and returns the filename.
        """
        filename = f"{prefix}_{uuid.uuid4()}.png"
        filepath = os.path.join(self.base_directory, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        return filename

    def get_full_path(self, filename: str) -> str:
        return os.path.join(self.base_directory, filename)
