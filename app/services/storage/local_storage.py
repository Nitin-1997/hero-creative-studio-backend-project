import os
import uuid
from app.core.interfaces import StorageProvider

class LocalStorageProvider(StorageProvider):
    """
    Local implementation of StorageProvider.
    Saves files to the server's disk.
    """
    def __init__(self, base_directory: str = "generated_images"):
        self.base_directory = base_directory
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)

    def save_image(self, image_data, prefix: str = "gen") -> str:
        filename = f"{prefix}_{uuid.uuid4()}.png"
        filepath = os.path.join(self.base_directory, filename)
        
        if hasattr(image_data, 'save'):
            # PIL Image
            image_data.save(filepath)
        else:
            # Bytes
            with open(filepath, "wb") as f:
                f.write(image_data)
            
        return filename
