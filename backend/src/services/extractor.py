import base64
from io import BytesIO
from PIL import Image

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.core.config import Settings
from src.core.logging import get_logger
from src.core.schemas.contact import ContactExtractionSchema
from src.core.exceptions.service import (
    InvalidImageException,
    GroqRateLimitException,
    LLMAPIException,
)
from src.services.interfaces import IContactExtractorService

logger = get_logger("app.services.extractor")


class ContactExtractorService(IContactExtractorService):
    """
    Implementation of IContactExtractorService using LangChain ChatGroq Vision LLM.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        logger.executing("Initializing ChatGroq Vision model")
        try:
            self.llm = ChatGroq(
                model=self.settings.llm_model,
                temperature=0.0,
                api_key=self.settings.groq_api_key,
            )
            # Enforce Pydantic schema structure
            self.structured_llm = self.llm.with_structured_output(
                ContactExtractionSchema
            )
            logger.finished("ChatGroq Vision model initialized successfully")
        except Exception as e:
            logger.finished(
                f"Failed to initialize ChatGroq Vision model: {e}",
                level=logger.logger.level,
            )
            raise LLMAPIException(f"LLM initialization failure: {e}")

    async def extract_contact_info(
        self, image_bytes: bytes, mime_type: str
    ) -> ContactExtractionSchema:
        # 1. Validate image format using Pillow
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

        # 2. Encode to base64 Data URI
        logger.executing("Encoding image bytes to Base64 URI")
        try:
            encoded_str = base64.b64encode(image_bytes).decode("utf-8")
            image_data_uri = f"data:{mime_type};base64,{encoded_str}"
            logger.finished("Image bytes encoded to Base64 successfully")
        except Exception as e:
            logger.finished(f"Encoding failed: {e}", level=logger.logger.level)
            raise InvalidImageException(f"Encoding image bytes to Base64 failed: {e}")

        # 3. Construct system and human prompts
        system_prompt = (
            "You are an expert Vision AI model specializing in extracting contact information from images "
            "such as business cards, event posters, flyers, banners, or billboards.\n\n"
            "Your task is to analyze the provided image, locate any contact-related details, identify core services/activities, "
            "and generate a short summary. Respond with a JSON object that matches the requested schema.\n\n"
            "Make sure to adhere to the following rules:\n"
            "1. Extract ONLY contact information (names, company, positions, addresses, services, digital contacts, summary).\n"
            "2. Identify the core services, tags, or specialties of the person or company.\n"
            "3. Write a brief 1-2 sentence summary explaining who this person/company is and what they offer based strictly on the image context.\n"
            '4. IMPORTANT: Professional roles, job titles, and positions (e.g., "Психиатр", "Software Engineer", "CEO") '
            "MUST be placed into the `positions` array, NOT into `services`. "
            "`services` should only contain actual services, offerings, or specialties.\n"
            "5. IGNORE any event-specific data like event dates, schedules, ticket prices, or locations/schedules that do not represent a permanent contact address.\n"
            "6. IMPORTANT: If a field cannot be found or is not explicitly present in the image, it MUST remain null (None) or an empty list. "
            "Do not make up, infer, or hallucinate information not present in the image.\n"
            "7. CRITICAL: All digital contact methods (phone numbers, email addresses, website URLs, social media handles/URLs) "
            "MUST be placed into the `digital_contacts` array. Do NOT use separate fields for phone, email, website, or social_media. "
            "Each item in `digital_contacts` must be an object with `type` and `value` keys:\n"
            "   - type: a lowercase string describing the contact type (e.g., 'phone', 'email', 'website', 'telegram', 'linkedin', "
            "'whatsapp', 'facebook', 'instagram', 'viber', 'x', 'vk').\n"
            "   - value: the actual phone number, email address, URL, or handle.\n"
            "   If the card has two phone numbers, add TWO items with type 'phone'. Do the same for any repeated contact type.\n"
            '   Example: digital_contacts = [{"type": "phone", "value": "+1 555 000 0000"}, {"type": "email", "value": "john@example.com"}]\n'
        )

        system_message = SystemMessage(content=system_prompt)
        human_message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "Analyze the following image and extract all contact and service information according to the specified Pydantic schema.",
                },
                {"type": "image_url", "image_url": {"url": image_data_uri}},
            ]
        )

        # 4. Invoke LLM and map exceptions
        logger.executing("Invoking Vision LLM for contact recognition")
        try:
            result: ContactExtractionSchema = await self.structured_llm.ainvoke(
                [system_message, human_message]
            )
            logger.finished("Structured contact information extracted successfully")
            return result
        except Exception as e:
            error_str = str(e)
            logger.finished(
                f"Vision LLM invocation failed: {error_str}", level=logger.logger.level
            )

            # Map Groq/LLM failures to custom clean DefaultHTTPException classes
            if "rate_limit" in error_str.lower() or "429" in error_str:
                raise GroqRateLimitException(
                    "Vision LLM rate limit exceeded. Please try again later."
                )

            raise LLMAPIException(f"Vision LLM service error: {error_str}")
