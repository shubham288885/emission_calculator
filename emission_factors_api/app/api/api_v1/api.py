from fastapi import APIRouter

from app.api.api_v1.endpoints import search

api_router = APIRouter()
api_router.include_router(search.router, prefix="/emission-factors", tags=["emission factors"]) 