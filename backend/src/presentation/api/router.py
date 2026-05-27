from fastapi import APIRouter
from src.presentation.api.extractor import router as extractor_router

api_router = APIRouter()
api_router.include_router(extractor_router)
