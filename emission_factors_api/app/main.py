import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.vector_search import vector_search_service

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {"message": "Welcome to the Emission Factors Semantic Search API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api_version": "v1",
        "model": settings.EMBEDDING_MODEL
    }

@app.on_event("startup")
async def startup_event():
    """Initialize the vector search service on startup"""
    logger.info("Initializing vector search service...")
    try:
        # Load data and build index
        loaded = vector_search_service.load_data()
        if not loaded:
            logger.warning("Failed to load emission factors data")
            return
            
        built = vector_search_service.build_index()
        if not built:
            logger.warning("Failed to build search index")
            return
            
        logger.info("Vector search service initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing vector search service: {e}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 