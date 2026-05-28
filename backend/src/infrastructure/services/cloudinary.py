import asyncio
import cloudinary
import cloudinary.uploader
from src.core.config import Settings
from src.core.logging import get_logger
from src.core.exceptions.service import CloudinaryUploadException
from src.services.interfaces import ICloudinaryService

logger = get_logger("app.infrastructure.services.cloudinary")


class CloudinaryService(ICloudinaryService):
    """
    Cloudinary API SDK wrapper implementing ICloudinaryService.
    Executes standard image uploads wrapped in asyncio.to_thread to maintain asynchronous compliance.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        logger.executing("Configuring Cloudinary SDK credentials")
        try:
            if self.settings.cloudinary_url:
                cloudinary.config(cloudinary_url=self.settings.cloudinary_url)
            else:
                cloudinary.config(
                    cloud_name=self.settings.cloudinary_cloud_name,
                    api_key=self.settings.cloudinary_api_key,
                    api_secret=self.settings.cloudinary_api_secret,
                    secure=True,
                )
            logger.finished("Cloudinary SDK credentials configured successfully")
        except Exception as e:
            logger.finished(
                f"Failed to configure Cloudinary SDK: {e}", level=logger.logger.level
            )
            raise CloudinaryUploadException(f"Cloudinary SDK bootstrap failed: {e}")

    async def upload_image(self, image_bytes: bytes, filename: str) -> str:
        logger.executing(f"Initiating upload to Cloudinary for image: {filename}")
        try:
            # Execute synchronous SDK upload safely in a separate thread pool
            response = await asyncio.to_thread(
                cloudinary.uploader.upload,
                image_bytes,
                folder="contact_recognition",
                resource_type="image",
            )
            secure_url = response.get("secure_url")
            if not secure_url:
                raise ValueError("Response structure missing secure_url key")

            logger.finished(
                f"Successfully uploaded image {filename} to Cloudinary. Hosted CDN URL: {secure_url}"
            )
            return secure_url
        except Exception as e:
            logger.finished(
                f"Cloudinary upload sequence crashed: {e}", level=logger.logger.level
            )
            raise CloudinaryUploadException(f"Cloudinary upload failure: {e}")
