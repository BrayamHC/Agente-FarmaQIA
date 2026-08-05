import httpx
import logging
from typing import Optional
from app.config.settings import settings

logger = logging.getLogger(__name__)


class PedidoService:
    """
    Servicio dedicado a crear pedidos en NestJS.
    Consume el endpoint POST /pedidos con lista de productos y cantidades.
    El backend se encarga de asignar lotes con FEFO (First Expired, First Out).
    """

    def __init__(self):
        self.base_url = settings.nestjs_api_url.rstrip("/") if settings.nestjs_api_url else ""
        self.api_key = settings.nestjs_internal_api_key
        self.sucursal_id = settings.farmacia_sucursal_id
        self.headers = {
            "x-internal-api-key": self.api_key,
            "x-sucursal-id": str(self.sucursal_id),
        }
        logger.info(
            f"PedidoService initialized: base_url={'✓' if self.base_url else '✗'}, "
            f"sucursal_id={self.sucursal_id}"
        )

    async def crear_pedido(self, items: list[dict]) -> dict:
        """
        Registra un pedido desde la conversación de WhatsApp.
        
        Args:
            items: Lista de diccionarios con estructura:
                   [{"producto_uuid": "uuid", "cantidad": 1}, ...]
                   
        Returns:
            dict con estructura: {"success": bool, "pedido_id": str|None, "message": str}
        """
        if not self.base_url:
            logger.error("NESTJS_API_URL no configurada")
            return {"success": False, "pedido_id": None, "message": "Configuración incompleta"}

        if not items:
            logger.warning("Intento de crear pedido sin items")
            return {"success": False, "pedido_id": None, "message": "No hay productos en el pedido"}

        payload = {
            "origen": "whatsapp",
            "items": items,
            "sucursal_id": self.sucursal_id,
        }
        
        logger.info(f"Creando pedido en NestJS: {len(items)} items, sucursal={self.sucursal_id}")

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/pedidos",
                    json=payload,
                    headers=self.headers,
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Pedido creado exitosamente: pedido_id={data.get('pedido_id')}")
                return {
                    "success": True,
                    "pedido_id": data.get("pedido_id"),
                    "message": "Pedido registrado correctamente",
                    "data": data,
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"Error HTTP al crear pedido: {e.response.status_code} - {e.response.text[:200]}")
                return {
                    "success": False,
                    "pedido_id": None,
                    "message": f"Error del servidor: {e.response.status_code}",
                }
            except httpx.TimeoutException as e:
                logger.error(f"Timeout al crear pedido: {e}")
                return {
                    "success": False,
                    "pedido_id": None,
                    "message": "Tiempo de espera agotado",
                }
            except Exception as e:
                logger.error(f"Error inesperado al crear pedido: {e}")
                return {
                    "success": False,
                    "pedido_id": None,
                    "message": str(e),
                }


pedido_service = PedidoService()
