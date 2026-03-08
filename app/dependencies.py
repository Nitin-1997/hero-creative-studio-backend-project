import os
from dotenv import load_dotenv
from app.services.poster_service import PosterService
from app.services.storage_service import StorageService
from app.services.image_generators.gemini_provider import GeminiImageProvider
from app.services.image_generators.pollinations_provider import PollinationsImageProvider

load_dotenv()

def get_poster_service() -> PosterService:
    # 1. Initialize Storage
    storage = StorageService()

    # 2. Initialize Generators in order of priority
    api_key = os.getenv("GEMINI_API_KEY")
    generators = [
        GeminiImageProvider(api_key),
        PollinationsImageProvider() # Fallback
    ]

    # 3. Create the orchestrator
    return PosterService(generators, storage)
