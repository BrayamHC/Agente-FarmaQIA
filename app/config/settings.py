from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        populate_by_name=True,
    )

    # OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "moonshotai/kimi-k2"

    # App
    APP_NAME: str = "Agente_FarmaQIA"
    APP_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"

    # WhatsApp
    WHATSAPP_VERIFY_TOKEN: str
    WHATSAPP_ACCESS_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str
    WHATSAPP_API_VERSION: str = "v23.0"

    # NestJS API
    NESTJS_API_URL: str = ""
    NESTJS_INTERNAL_API_KEY: str = ""
    FARMACIA_SUCURSAL_ID: str = "1"


settings = Settings()