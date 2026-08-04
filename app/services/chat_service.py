# app/services/chat_service.py
import logging
from app.services.prompt_service import prompt_service
from app.services.farmacia_service import FarmaciaService
from app.config.settings import settings
import httpx

logger = logging.getLogger(__name__)
farmacia_service = FarmaciaService()


class ChatService:
    async def handle_message(self, user_message: str, history: list[dict] | None = None) -> str:
        # 1. Extraer tags del mensaje del usuario
        tags = prompt_service.extract_tags(user_message)

        # 2. Si hay tags, consultar inventario en NestJS
        inventory_context = None
        if tags:
            logger.info(f"Tags detectados: {tags}")
            resultado = await farmacia_service.obtener_recomendaciones(tags=tags, limite=5)
            productos = resultado.get("productos", [])
            inventory_context = prompt_service.format_inventory_context(productos)
            logger.info(f"Productos encontrados: {len(productos)}")

        # 3. Construir mensajes con contexto de inventario
        messages = prompt_service.build_messages(
            user_message=user_message,
            history=history,
            inventory_context=inventory_context,
        )

        # 4. Llamar a OpenRouter
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{settings.OPENROUTER_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.OPENROUTER_MODEL,
                        "messages": messages,
                        "max_tokens": 1024,
                        "temperature": 0.7,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error llamando a OpenRouter: {e}")
            return "Disculpa, estoy teniendo problemas para responder. ¿Podrías intentar de nuevo?"


chat_service = ChatService()