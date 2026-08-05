import logging
import httpx
from app.services.prompt_service import prompt_service
from app.services.farmacia_service import farmacia_service
from app.config.settings import settings

logger = logging.getLogger(__name__)


class ChatService:
    async def handle_message(
        self, user_message: str, history: list[dict] | None = None
    ) -> str:
        # 1. Extraer tags
        tags = prompt_service.extract_tags(user_message)
        logger.info(f"Mensaje recibido: '{user_message}' | Tags extraídos: {tags}")

        # 2. Consultar inventario si hay tags
        inventory_context: str | None = None
        if tags:
            resultado = await farmacia_service.obtener_recomendaciones(tags=tags, limite=5)
            productos = resultado.get("productos", [])
            logger.info(f"Productos recibidos de NestJS: {len(productos)}")

            if productos:
                inventory_context = prompt_service.format_inventory_context(productos)
            else:
                logger.warning("NestJS devolvió lista vacía de productos")
        else:
            logger.info("Sin tags detectados — respuesta general sin inventario")

        # 3. Construir mensajes
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

                choices = data.get("choices", [])
                if not choices or "message" not in choices[0]:
                    logger.error(f"Respuesta inválida de OpenRouter: {data}")
                    return "Disculpa, no pude procesar tu consulta. ¿Podrías intentar de nuevo?"

                return choices[0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP de OpenRouter: {e.response.status_code} - {e.response.text}")
            return "Disculpa, estoy teniendo problemas para responder. ¿Podrías intentar de nuevo?"
        except Exception as e:
            logger.error(f"Error inesperado llamando a OpenRouter: {e}")
            return "Disculpa, estoy teniendo problemas para responder. ¿Podrías intentar de nuevo?"


chat_service = ChatService()