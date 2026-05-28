from starlette import status
from src.core.exceptions.base import DefaultHTTPException


class GroqRateLimitException(DefaultHTTPException):
    """
    Exception thrown when the Groq LLM API rate limits are hit.
    """

    error = "GROQ_RATE_LIMIT"
    message = "Groq API rate limit has been exceeded. Please retry later."
    field = "groq_api"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class LLMAPIException(DefaultHTTPException):
    """
    Exception thrown when there is an API or network error communicating with Groq.
    """

    error = "LLM_API_ERROR"
    message = "An error occurred while communicating with the Vision LLM service."
    field = "llm_service"
    status_code = status.HTTP_502_BAD_GATEWAY


class InvalidImageException(DefaultHTTPException):
    """
    Exception thrown when an uploaded image is invalid or unreadable.
    """

    error = "INVALID_IMAGE"
    message = "The uploaded file is not a valid image or is corrupted."
    field = "image"
    status_code = status.HTTP_400_BAD_REQUEST


class CloudinaryUploadException(DefaultHTTPException):
    """
    Exception thrown when Cloudinary hosting fails.
    """

    error = "CLOUDINARY_UPLOAD_ERROR"
    message = "Failed to upload and host the card image in Cloudinary."
    field = "cloudinary"
    status_code = status.HTTP_502_BAD_GATEWAY


class CardNotFoundException(DefaultHTTPException):
    """
    Exception thrown when the requested scanned card cannot be found.
    """

    error = "CARD_NOT_FOUND"
    message = "The requested contact card could not be found."
    field = "card_id"
    status_code = status.HTTP_404_NOT_FOUND


class DatabaseConnectionException(DefaultHTTPException):
    """
    Exception thrown when MongoDB operations fail due to connection or integrity issues.
    """

    error = "DATABASE_ERROR"
    message = "A database service error occurred. Please try again."
    field = "database"
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
