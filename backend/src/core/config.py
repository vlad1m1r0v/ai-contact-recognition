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


# Instantiate settings
settings = Settings()
