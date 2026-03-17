import os
from dotenv import load_dotenv
from app.services.poster_service import PosterService
from app.services.storage.local_storage import LocalStorageProvider
from app.services.image_generators.gemini_provider import GeminiImageProvider
from app.services.image_generators.pollinations_provider import PollinationsImageProvider
from app.services.image_generators.placeholder_provider import LocalPlaceholderProvider

load_dotenv()

def get_storage_provider():
    return LocalStorageProvider()

def get_poster_service() -> PosterService:
    storage = get_storage_provider()

    # Initialize Generators in order of priority
    api_key = os.getenv("GEMINI_API_KEY")
    generators = [
        GeminiImageProvider(api_key),
        PollinationsImageProvider(), # AI Fallback 1
        PollinationsImageProvider(model="turbo"), # AI Fallback 2 (Faster model)
        LocalPlaceholderProvider()   # Final Emergency Fallback
    ]

    # Create the orchestrator
    return PosterService(generators, storage)
