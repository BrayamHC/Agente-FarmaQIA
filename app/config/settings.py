from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "moonshotai/kimi-k2"
    app_name: str = "Agente_FarmaQIA"
    app_url: str = "http://localhost:8000"
    environment: str = "development"


settings = Settings()