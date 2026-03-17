import logging
from fastapi import APIRouter, HTTPException, Depends, Response
from app.models.request_model import PosterRequest
from app.utils.prompt_builder import build_prompt
from app.services.poster_service import PosterService
from app.dependencies import get_poster_service, get_storage_provider

# Set up logging using the uvicorn logger for consistent formatting
logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.post("/generate-poster")
async def generate_poster(
    request: PosterRequest, 
    service: PosterService = Depends(get_poster_service)
):
    try:
        logger.info(f"Received poster generation request for model: {request.bike_model}")
        
        # 1. Build the prompt for the image generator
        prompt = build_prompt(request)
        
        # 2. Use the injected service to generate the poster
        image_filename = service.create_poster(prompt)
        
        if not image_filename:
            logger.error("Poster generation failed after trying all providers.")
            raise Exception("AI service failed to generate an image.")
            
        logger.info(f"Poster successfully generated: {image_filename}")
        
        image_url = image_filename
        if not image_url.startswith("http") and not image_url.startswith("/api/"):
            image_url = f"/images/{image_filename}"
            
        # 3. Return the results
        return {
            "status": "success",
            "message": "Poster generated successfully",
            "image_url": image_url,
            "prompt": prompt
        }
    except Exception as e:
        logger.exception("An error occurred during poster generation")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drive-image/{file_id}")
async def get_drive_image(
    file_id: str,
    storage = Depends(get_storage_provider)
):
    """
    Proxies an image from Google Drive to the browser.
    """
    try:
        if hasattr(storage, 'get_image'):
            image_bytes = storage.get_image(file_id)
            return Response(content=image_bytes, media_type="image/png")
        else:
            raise HTTPException(status_code=400, detail="Storage provider does not support direct fetch.")
    except Exception as e:
        logger.error(f"Failed to fetch image {file_id} from Drive: {e}")
        raise HTTPException(status_code=404, detail="Image not found in Drive.")

@router.get("/health")
async def health_check():
    logger.info("--- Health Check endpoint called ---")
    return {"status": "ok"}
