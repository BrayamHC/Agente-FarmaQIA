from app.providers.openrouter import openrouter_provider
from app.services.prompt_service import prompt_service


class ChatService:
    """
    Orquesta el flujo completo: recibe mensaje del usuario,
    construye el contexto y obtiene la respuesta del modelo.
    """

    def handle_message(self, user_message: str, history: list[dict] | None = None) -> str:
        messages = prompt_service.build_messages(user_message, history)
        return openrouter_provider.generate_response(messages)


chat_service = ChatService()