from typing import List, Optional
from pydantic import BaseModel, Field


class SocialMedia(BaseModel):
    """Schema representing a social media handle or link."""

    platform: str = Field(
        ...,
        description="The social media platform name, e.g., telegram, linkedin, whatsapp, facebook, instagram, viber, x",
    )
    username_or_link: str = Field(
        ..., description="The username, handle, or full URL to the social media profile"
    )


class ContactExtractionSchema(BaseModel):
    """Schema representing the contact and service details extracted from an image."""

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
