from app.providers.openrouter import openrouter_provider
from app.services.prompt_service import prompt_service
from app.services.inventory_service import inventory_service


class ChatService:
    """
    Orquesta el flujo completo: recibe mensaje del usuario,
    construye el contexto y obtiene la respuesta del modelo.
    """

    def handle_message(self, user_message: str, history: list[dict] | None = None) -> str:
        tags = prompt_service.extract_tags(user_message)
        productos = inventory_service.get_products_by_tags(tags) if tags else []
        inventory_context = (
            prompt_service.format_inventory_context(productos)
            if productos
            else None
        )

        messages = prompt_service.build_messages(
            user_message=user_message,
            history=history,
            inventory_context=inventory_context,
        )

        return openrouter_provider.generate_response(messages)


chat_service = ChatService()