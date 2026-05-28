import re
import base64
from datetime import datetime
from fastapi import APIRouter, Body, File, Query, UploadFile, status
from dishka.integrations.fastapi import FromDishka, inject

from typing import Optional
from src.core.schemas.contact import (
    ContactExtractionSchema,
    CreateContactRequest,
    PaginatedResponse,
)
from src.core.exceptions.generator import generate_examples
from src.core.exceptions.service import (
    InvalidImageException,
    GroqRateLimitException,
    LLMAPIException,
    CloudinaryUploadException,
    CardNotFoundException,
    DatabaseConnectionException,
)
from src.services.interfaces import ICardUsecaseService
from src.core.logging import get_logger

logger = get_logger("app.presentation.api.extractor")

router = APIRouter(prefix="/contacts", tags=["Contact Recognition"])


@router.post(
    path="/extract",
    response_model=ContactExtractionSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        InvalidImageException,
        GroqRateLimitException,
        LLMAPIException,
    ),
    response_model_exclude_none=True,
    summary="Extract Contact Info from Image",
    description=(
        "Upload an image (business card, poster, flyer, banner, or billboard), "
        "parse it into structured contact data via Vision LLM. "
        "Data is NOT persisted — use POST /contacts to save after review."
    ),
)
@inject
async def extract_contacts(
    card_usecase_service: FromDishka[ICardUsecaseService],
    file: UploadFile = File(
        ..., description="The image file containing contact information"
    ),
) -> ContactExtractionSchema:
    """
    Extract contact information from form-uploaded image bytes
    using Vision LLM. No data is saved to the database.
    """
    logger.executing(
        f"API request received: Extract contacts from uploaded file {file.filename}"
    )

    image_bytes = await file.read()
    mime_type = file.content_type or "image/png"

    result = await card_usecase_service.extract_contact_info(
        image_bytes=image_bytes, mime_type=mime_type
    )

    logger.finished(f"API request completed successfully for file {file.filename}")
    return result


@router.post(
    path="",
    response_model=ContactExtractionSchema,
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        InvalidImageException,
        CloudinaryUploadException,
        DatabaseConnectionException,
    ),
    response_model_exclude_none=True,
    summary="Save a Contact Card",
    description=(
        "Create a new contact card from pre-extracted JSON data and a base64-encoded image. "
        "The image is uploaded to Cloudinary and the structured data is persisted in MongoDB."
    ),
)
@inject
async def create_contact_card(
    card_usecase_service: FromDishka[ICardUsecaseService],
    body: CreateContactRequest = Body(
        ..., description="Contact data with base64-encoded image"
    ),
) -> ContactExtractionSchema:
    """
    Save a contact card to the database. Accepts previously extracted
    (and optionally user-edited) contact information along with the
    original image as a base64 data URI.
    """
    logger.executing("API request received: Create new contact card")

    match = re.match(r"data:(?P<mime>[^;]+);base64,(?P<data>.+)", body.image_base64)
    if not match:
        raise InvalidImageException(
            "Invalid image data URI format. Expected: data:{mime};base64,{data}"
        )

    mime_type = match.group("mime")
    image_bytes = base64.b64decode(match.group("data"))
    ext = mime_type.split("/")[-1]
    filename = f"card_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"

    extraction = ContactExtractionSchema(
        first_name=body.first_name,
        last_name=body.last_name,
        middle_name=body.middle_name,
        company_name=body.company_name,
        position=body.position,
        services=body.services,
        addresses=body.addresses,
        phone_number=body.phone_number,
        email=body.email,
        website=body.website,
        social_media=body.social_media,
        summary=body.summary,
    )

    result = await card_usecase_service.create_card(
        extraction=extraction, image_bytes=image_bytes, filename=filename
    )

    logger.finished("API request completed: Contact card created successfully")
    return result


@router.get(
    path="",
    response_model=PaginatedResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(DatabaseConnectionException),
    summary="List Scanned Cards",
    description=(
        "Retrieve a paginated list of all previously scanned contact cards. "
        "Each item contains the Cloudinary image URL, display name, and scanning timestamp."
    ),
)
@inject
async def list_cards(
    card_usecase_service: FromDishka[ICardUsecaseService],
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(
        default=None, description="Filter by display name substring (case-insensitive)"
    ),
) -> PaginatedResponse:
    """
    Paginated listing of all scanned contact cards.
    """
    logger.executing(
        f"API request received: List scanned cards (page={page}, limit={limit}, search={search})"
    )

    result = await card_usecase_service.get_all_cards(
        page=page, limit=limit, search=search
    )

    logger.finished(
        f"API request completed: Listed {len(result.items)} cards (total={result.total})"
    )
    return result


@router.get(
    path="/{card_id}",
    response_model=ContactExtractionSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(CardNotFoundException, DatabaseConnectionException),
    response_model_exclude_none=True,
    summary="Get Card Details",
    description="Retrieve the full extracted contact information for a specific scanned card by its ID.",
)
@inject
async def get_card_details(
    card_id: str,
    card_usecase_service: FromDishka[ICardUsecaseService],
) -> ContactExtractionSchema:
    """
    Load full contact extraction details for a specific card by MongoDB ID.
    """
    logger.executing(f"API request received: Get card details for ID {card_id}")

    result = await card_usecase_service.get_card_details(card_id=card_id)

    logger.finished(f"API request completed: Loaded card details for ID {card_id}")
    return result
