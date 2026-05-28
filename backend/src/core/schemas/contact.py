from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SocialPlatform(str, Enum):
    """Enum representing supported social media platforms."""

    TELEGRAM = "telegram"
    LINKEDIN = "linkedin"
    WHATSAPP = "whatsapp"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    VIBER = "viber"
    X = "x"
    VK = "vk"


class SocialMedia(BaseModel):
    """Schema representing a social media handle or link."""

    platform: SocialPlatform = Field(
        ...,
        description="The social media platform name, e.g., telegram, linkedin, whatsapp, facebook, instagram, viber, x",
    )
    username_or_link: str = Field(
        ..., description="The username, handle, or full URL to the social media profile"
    )


class ContactExtractionSchema(BaseModel):
    """Schema representing the contact and service details extracted from an image."""

    id: Optional[str] = Field(
        default=None, description="Unique database ID for this scanned card"
    )
    image_url: Optional[str] = Field(
        default=None, description="Cloudinary hosting URL for the scanned card image"
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="Scanning timestamp indicating when the card was processed",
    )

    first_name: Optional[str] = Field(
        default=None, description="First name of the contact person, if available"
    )
    last_name: Optional[str] = Field(
        default=None, description="Last name of the contact person, if available"
    )
    middle_name: Optional[str] = Field(
        default=None, description="Middle name of the contact person, if available"
    )
    company_name: Optional[str] = Field(
        default=None, description="Name of the company or organization, if available"
    )
    position: Optional[str] = Field(
        default=None,
        description="Job title or professional position of the person, if available",
    )
    services: List[str] = Field(
        default_factory=list,
        description="List of strings describing core services, activities, specialties, or tags representing what they offer",
    )
    addresses: List[str] = Field(
        default_factory=list,
        description="Physical addresses, locations, or branches mentioned on the card/image",
    )
    phone_number: Optional[str] = Field(
        default=None,
        description="Contact phone number including any country code or formatting",
    )
    email: Optional[str] = Field(
        default=None, description="Email address of the contact person or company"
    )
    website: Optional[str] = Field(default=None, description="Official website URL")
    social_media: List[SocialMedia] = Field(
        default_factory=list, description="List of social media channels extracted"
    )
    summary: Optional[str] = Field(
        default=None,
        description="A 1-2 sentence brief description explaining who this person/company is and what they offer based on the image context",
    )


class CardListElement(BaseModel):
    """Simplified element representation for the scanned cards paginated list."""

    id: str = Field(..., description="Unique database ID of the contact card")
    image_url: str = Field(
        ..., description="Cloudinary secure hosting URL for the card image"
    )
    display_name: str = Field(..., description="Company name OR Person's full name")
    created_at: datetime = Field(..., description="Scanning timestamp")


class CreateContactRequest(BaseModel):
    """Request schema for creating a new contact card with pre-extracted data."""

    image_base64: str = Field(
        ...,
        description="Base64 data URI of the card image (e.g., data:image/png;base64,iVBOR...)",
    )
    first_name: Optional[str] = Field(
        default=None, description="First name of the contact person, if available"
    )
    last_name: Optional[str] = Field(
        default=None, description="Last name of the contact person, if available"
    )
    middle_name: Optional[str] = Field(
        default=None, description="Middle name of the contact person, if available"
    )
    company_name: Optional[str] = Field(
        default=None, description="Name of the company or organization, if available"
    )
    position: Optional[str] = Field(
        default=None,
        description="Job title or professional position of the person, if available",
    )
    services: List[str] = Field(
        default_factory=list,
        description="List of strings describing core services, activities, specialties, or tags representing what they offer",
    )
    addresses: List[str] = Field(
        default_factory=list,
        description="Physical addresses, locations, or branches mentioned on the card/image",
    )
    phone_number: Optional[str] = Field(
        default=None,
        description="Contact phone number including any country code or formatting",
    )
    email: Optional[str] = Field(
        default=None, description="Email address of the contact person or company"
    )
    website: Optional[str] = Field(default=None, description="Official website URL")
    social_media: List[SocialMedia] = Field(
        default_factory=list, description="List of social media channels"
    )
    summary: Optional[str] = Field(
        default=None,
        description="A 1-2 sentence brief description explaining who this person/company is and what they offer",
    )


class PaginatedResponse(BaseModel):
    """Generic envelope model for paginated API responses."""

    items: List[CardListElement] = Field(
        ..., description="List of items for the current page"
    )
    total: int = Field(
        ..., description="Total number of elements in database matching criteria"
    )
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Limit of elements per page")
