from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routes import poster_routes
import os

app = FastAPI(title="Hero Creative Studio API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create generated_images directory if it doesn't exist
if not os.path.exists("generated_images"):
    os.makedirs("generated_images")

# Serve generated images as static files
app.mount("/images", StaticFiles(directory="generated_images"), name="images")

# Include routers
app.include_router(poster_routes.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hero Creative Studio API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
