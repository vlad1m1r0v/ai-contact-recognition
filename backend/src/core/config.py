from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings powered by pydantic-settings.
    Automatically loads environment variables from a .env file if available.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    groq_api_key: str = Field(
        ..., alias="GROQ_API_KEY", description="API Key for Groq authentication"
    )
    llm_model: str = Field(
        default="meta-llama/llama-4-scout-17b-16e-instruct",
        alias="LLM_MODEL",
        description="Vision LLM model identifier",
    )
    app_host: str = Field(
        default="0.0.0.0", alias="APP_HOST", description="FastAPI service bind host"
    )
    app_port: int = Field(
        default=8000, alias="APP_PORT", description="FastAPI service bind port"
    )
    debug: bool = Field(default=False, alias="DEBUG", description="Enable debug mode")

    # MongoDB Configurations
    mongodb_url: str = Field(
        default="mongodb://admin:adminpassword@localhost:27017",
        alias="MONGODB_URL",
        description="MongoDB connection string URL",
    )
    mongodb_database: str = Field(
        default="contact_recognition",
        alias="MONGODB_DATABASE",
        description="MongoDB database name",
    )

    # Cloudinary Configurations
    cloudinary_cloud_name: str = Field(
        default="", alias="CLOUDINARY_CLOUD_NAME", description="Cloudinary Cloud Name"
    )
    cloudinary_api_key: str = Field(
        default="", alias="CLOUDINARY_API_KEY", description="Cloudinary API Key"
    )
    cloudinary_api_secret: str = Field(
        default="", alias="CLOUDINARY_API_SECRET", description="Cloudinary API Secret"
    )
    cloudinary_url: str = Field(
        default="",
        alias="CLOUDINARY_URL",
        description="Cloudinary URL integration configuration string",
    )


# Instantiate settings
settings = Settings()
