from openai import OpenAI
from app.config.settings import settings


class OpenRouterProvider:
    def __init__(self) -> None:
        self._client = OpenAI(
            base_url=settings.OPENROUTER_BASE_URL,
            api_key=settings.OPENROUTER_API_KEY,
        )
        self._model = settings.OPENROUTER_MODEL

    def generate_response(self, messages: list[dict]) -> str:
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            extra_headers={
                "HTTP-Referer": settings.APP_URL,
                "X-Title": settings.APP_NAME,
            },
        )
        return completion.choices[0].message.content or ""


openrouter_provider = OpenRouterProvider()