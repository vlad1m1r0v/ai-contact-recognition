from io import BytesIO
from typing import Optional
from datetime import datetime
from PIL import Image
from src.core.logging import get_logger
from src.core.schemas.contact import ContactExtractionSchema, PaginatedResponse
from src.core.exceptions.service import CardNotFoundException, InvalidImageException
from src.services.interfaces import (
    IContactExtractorService,
    ICloudinaryService,
    ICardRepository,
    ICardUsecaseService,
)

logger = get_logger("app.services.card_usecase")


class CardUsecaseService(ICardUsecaseService):
    """
    Standard use-case interactor orchestrating visual recognition,
    CDN image hosting, and database persistence.
    """

    def __init__(
        self,
        extractor: IContactExtractorService,
        cloudinary: ICloudinaryService,
        repository: ICardRepository,
    ) -> None:
        self.extractor = extractor
        self.cloudinary = cloudinary
        self.repository = repository
        logger.finished("CardUsecaseService boundaries and interactor wired.")

    async def extract_contact_info(
        self, image_bytes: bytes, mime_type: str
    ) -> ContactExtractionSchema:
        logger.executing("Starting contact info extraction use-case (no persistence)")

        extraction = await self.extractor.extract_contact_info(image_bytes, mime_type)

        logger.finished("Contact info extraction completed successfully")
        return extraction

    async def create_card(
        self, extraction: ContactExtractionSchema, image_bytes: bytes, filename: str
    ) -> ContactExtractionSchema:
        logger.executing("Starting card creation use-case (Cloudinary + DB)")

        # 1. Validate image integrity
        logger.executing("Verifying image integrity using Pillow")
        try:
            with Image.open(BytesIO(image_bytes)) as img:
                img.verify()
            logger.finished("Image integrity verified successfully")
        except Exception as e:
            logger.finished(
                f"Image verification failed: {e}", level=logger.logger.level
            )
            raise InvalidImageException(f"The provided file is not a valid image: {e}")

        # 2. Host image in Cloudinary
        image_url = await self.cloudinary.upload_image(image_bytes, filename)

        # 3. Add CDN link and current timestamp to metadata
        extraction.image_url = image_url
        extraction.created_at = datetime.now()

        # 4. Persist to MongoDB
        card_id = await self.repository.save_card(extraction)
        extraction.id = card_id

        logger.finished(
            f"Card creation use-case completed successfully. Card persisted with ID: {card_id}"
        )
        return extraction

    async def get_all_cards(
        self, page: int, limit: int, search: Optional[str] = None
    ) -> PaginatedResponse:
        logger.executing(
            f"Orchestrating listing request for scanned cards (page={page}, limit={limit}, search={search})"
        )

        items, total = await self.repository.list_cards(page, limit, search=search)
        response = PaginatedResponse(items=items, total=total, page=page, limit=limit)

        logger.finished(
            f"Orchestrated scanned cards listing loaded successfully (items={len(items)}, total={total})"
        )
        return response

    async def get_card_details(self, card_id: str) -> ContactExtractionSchema:
        logger.executing(f"Orchestrating detailed contact lookup for ID: {card_id}")

        card = await self.repository.get_card_by_id(card_id)
        if not card:
            logger.finished(
                f"Orchestrated contact details lookup failed (Card not found): {card_id}",
                level=logger.logger.level,
            )
            raise CardNotFoundException(
                f"Contact card details cannot be found for ID: {card_id}"
            )

        logger.finished(
            f"Orchestrated contact details loaded successfully for ID: {card_id}"
        )
        return card

    async def delete_card(self, card_id: str) -> None:
        logger.executing(f"Orchestrating card deletion for ID: {card_id}")
        card = await self.repository.get_card_by_id(card_id)
        if not card:
            raise CardNotFoundException(
                f"Contact card cannot be found for deletion: {card_id}"
            )
        await self.repository.delete_card(card_id)
        logger.finished(f"Card deletion orchestrated successfully for ID: {card_id}")

    async def update_card(
        self, card_id: str, extraction: ContactExtractionSchema
    ) -> ContactExtractionSchema:
        logger.executing(f"Orchestrating card update for ID: {card_id}")
        updated = await self.repository.update_card(card_id, extraction)
        if not updated:
            raise CardNotFoundException(
                f"Contact card cannot be found for update: {card_id}"
            )
        logger.finished(f"Card update orchestrated successfully for ID: {card_id}")
        return updated
