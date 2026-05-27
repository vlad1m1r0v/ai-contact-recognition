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
