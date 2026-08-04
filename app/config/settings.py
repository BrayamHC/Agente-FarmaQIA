from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

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

    # NestJS
    NESTJS_API_URL: str = "http://localhost:3100"
    NESTJS_INTERNAL_API_KEY: str = ""
    FARMACIA_SUCURSAL_ID: int = 1

settings = Settings()