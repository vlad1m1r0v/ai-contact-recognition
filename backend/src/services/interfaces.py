import abc
from typing import List, Optional, Tuple
from src.core.schemas.contact import (
    ContactExtractionSchema,
    CardListElement,
    PaginatedResponse,
)


class IContactExtractorService(abc.ABC):
    """
    Abstract interface for parsing images and extracting contact schemas.
    Follows Clean Architecture boundary interfaces.
    """

    @abc.abstractmethod
    async def extract_contact_info(
        self, image_bytes: bytes, mime_type: str
    ) -> ContactExtractionSchema:
        """
        Extract contact data from raw image bytes and mime type.
        """
        pass


class ICloudinaryService(abc.ABC):
    """
    Abstract boundary for hosting uploaded business cards in Cloudinary.
    """

    @abc.abstractmethod
    async def upload_image(self, image_bytes: bytes, filename: str) -> str:
        """
        Upload image binary bytes and return secure URL.
        """
        pass


class ICardRepository(abc.ABC):
    """
    Abstract persistence repository boundary for card entities.
    """

    @abc.abstractmethod
    async def save_card(self, extraction: ContactExtractionSchema) -> str:
        """
        Persist complete card details in MongoDB. Returns the generated ID.
        """
        pass

    @abc.abstractmethod
    async def list_cards(
        self, page: int, limit: int, search: Optional[str] = None
    ) -> Tuple[List[CardListElement], int]:
        """
        Retrieve simplified list summaries matching criteria.
        If search is provided, filter by display_name substring (case-insensitive).
        Returns (items, total_count).
        """
        pass

    @abc.abstractmethod
    async def get_card_by_id(self, card_id: str) -> Optional[ContactExtractionSchema]:
        """
        Fetch full contact extraction entity by database ID.
        """
        pass


class ICardUsecaseService(abc.ABC):
    """
    Core orchestrating service combining image hosting, OCR parsing, and DB persistence.
    """

    @abc.abstractmethod
    async def extract_contact_info(
        self, image_bytes: bytes, mime_type: str
    ) -> ContactExtractionSchema:
        """
        Extract contact info from image bytes using Vision LLM (no persistence).
        """
        pass

    @abc.abstractmethod
    async def create_card(
        self, extraction: ContactExtractionSchema, image_bytes: bytes, filename: str
    ) -> ContactExtractionSchema:
        """
        Upload image to Cloudinary and persist extracted data to MongoDB.
        Returns the saved schema with generated id.
        """
        pass

    @abc.abstractmethod
    async def get_all_cards(
        self, page: int, limit: int, search: Optional[str] = None
    ) -> PaginatedResponse:
        """
        Coordinate loading list of all scanned cards.
        """
        pass

    @abc.abstractmethod
    async def get_card_details(self, card_id: str) -> ContactExtractionSchema:
        """
        Load detailed scanned card metrics.
        """
        pass
