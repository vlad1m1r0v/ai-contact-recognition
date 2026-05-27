import abc
from src.core.schemas.contact import ContactExtractionSchema


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
