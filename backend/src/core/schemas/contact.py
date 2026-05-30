from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactMethod(BaseModel):
    """Schema representing a single digital contact method."""

    type: str = Field(
        ...,
        description="Contact type, e.g., phone, email, website, telegram, linkedin, etc. (always lowercase)",
    )
    value: str = Field(
        ..., description="The actual phone number, email address, or URL string"
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
    positions: List[str] = Field(
        default_factory=list,
        description="List of professional positions, job titles, or roles held by the person",
    )
    services: List[str] = Field(
        default_factory=list,
        description="List of strings describing core services, activities, specialties, or tags representing what they offer",
    )
    addresses: List[str] = Field(
        default_factory=list,
        description="Physical addresses, locations, or branches mentioned on the card/image",
    )
    digital_contacts: List[ContactMethod] = Field(
        default_factory=list,
        description="Unified list of all digital contact methods (phone, email, website, social media, etc.)",
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
    positions: List[str] = Field(
        default_factory=list,
        description="List of professional positions, job titles, or roles held by the person",
    )
    services: List[str] = Field(
        default_factory=list,
        description="List of strings describing core services, activities, specialties, or tags representing what they offer",
    )
    addresses: List[str] = Field(
        default_factory=list,
        description="Physical addresses, locations, or branches mentioned on the card/image",
    )
    digital_contacts: List[ContactMethod] = Field(
        default_factory=list,
        description="Unified list of all digital contact methods",
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
