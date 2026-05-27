from fastapi import APIRouter, File, UploadFile, status
from dishka.integrations.fastapi import FromDishka, inject

from src.core.schemas.contact import ContactExtractionSchema
from src.core.exceptions.generator import generate_examples
from src.core.exceptions.service import (
    InvalidImageException,
    GroqRateLimitException,
    LLMAPIException,
)
from src.services.interfaces import IContactExtractorService
from src.core.logging import get_logger

logger = get_logger("app.presentation.api.extractor")

router = APIRouter(prefix="/contacts", tags=["Contact Recognition"])


@router.post(
    path="/extract",
    response_model=ContactExtractionSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        InvalidImageException, GroqRateLimitException, LLMAPIException
    ),
    response_model_exclude_none=True,
    summary="Extract Contact Info from Image",
    description="Upload an image (business card, poster, flyer, banner, or billboard) and parse it into structured contact data.",
)
@inject
async def extract_contacts(
    extractor_service: FromDishka[IContactExtractorService],
    file: UploadFile = File(
        ..., description="The image file containing contact information"
    ),
) -> ContactExtractionSchema:
    """
    Extract contact information from form-uploaded image bytes using ChatGroq.
    """
    logger.executing(
        f"API request received: Extract contacts from uploaded file {file.filename}"
    )

    # Read file content and determine mime type
    image_bytes = await file.read()
    mime_type = file.content_type or "image/png"

    # Run business use-case service
    result = await extractor_service.extract_contact_info(
        image_bytes=image_bytes, mime_type=mime_type
    )

    logger.finished(f"API request completed successfully for file {file.filename}")
    return result
