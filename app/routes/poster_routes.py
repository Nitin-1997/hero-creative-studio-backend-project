import logging
from fastapi import APIRouter, HTTPException, Depends
from app.models.request_model import PosterRequest
from app.utils.prompt_builder import build_prompt
from app.services.poster_service import PosterService
from app.dependencies import get_poster_service

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
        
        # 1. Build the prompt
        prompt = build_prompt(request)
        
        # 2. Use the injected service to generate the poster
        image_filename = service.create_poster(prompt)
        
        if not image_filename:
            logger.error("Poster generation failed after trying all providers.")
            raise Exception("AI service failed to generate an image.")
            
        logger.info(f"Poster successfully generated: {image_filename}")
        
        # 3. Return the results
        return {
            "status": "success",
            "message": "Poster generated successfully",
            "image_url": f"/images/{image_filename}",
            "prompt": prompt
        }
    except Exception as e:
        logger.exception("An error occurred during poster generation")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    logger.info("--- Health Check endpoint called ---")
    return {"status": "ok"}
