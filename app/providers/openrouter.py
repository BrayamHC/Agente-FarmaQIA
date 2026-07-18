from openai import OpenAI
from app.config.settings import settings


class OpenRouterProvider:
    """
    Unica integracion con el modelo de IA.
    Nunca acoplar el codigo a un modelo especifico:
    el modelo se controla via variable de entorno OPENROUTER_MODEL.
    """

    def __init__(self) -> None:
        self._client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )
        self._model = settings.openrouter_model

    def generate_response(self, messages: list[dict]) -> str:
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            extra_headers={
                "HTTP-Referer": settings.app_url,
                "X-Title": settings.app_name,
            },
        )
        return completion.choices[0].message.content or ""


openrouter_provider = OpenRouterProvider()