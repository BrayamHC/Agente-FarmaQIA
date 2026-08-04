import logging
from typing import Optional
from app.config.settings import settings

logger = logging.getLogger(__name__)


class FarmaciaService:
    """Conecta el microservicio con el backend NestJS de FarmaQ."""

    def __init__(self):
        self.base_url = settings.nestjs_api_url.rstrip("/") if settings.nestjs_api_url else ""
        self.api_key = settings.nestjs_internal_api_key
        self.sucursal_id = settings.farmacia_sucursal_id
        self.headers = {
            "x-internal-api-key": self.api_key,
            "x-sucursal-id": self.sucursal_id,
        }

    async def obtener_recomendaciones(
        self,
        tags: list[str],
        limite: int = 8,
        stock_minimo: int = 1,
    ) -> dict:
        """
        Consulta productos por tags aplicando FEFO en NestJS.
        Retorna lista limpia sin información de caducidad.
        """
        if not self.base_url or not tags:
            return {"success": False, "total": 0, "productos": []}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/productos/recomendaciones",
                    params={
                        "tags": ",".join(tags),
                        "limite": limite,
                        "stock_minimo": stock_minimo,
                    },
                    headers=self.headers,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error HTTP desde NestJS: {e.response.status_code}")
                return {"success": False, "total": 0, "productos": []}
            except Exception as e:
                logger.error(f"Error al conectar con NestJS: {e}")
                return {"success": False, "total": 0, "productos": []}

    async def crear_pedido(self, items: list[dict]) -> dict:
        """
        Registra un pedido desde la conversación de WhatsApp.
        items: [{ sku, producto_id, cantidad }]
        """
        if not self.base_url:
            return {"success": False, "message": "NESTJS_API_URL no configurada"}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/pedidos",
                    json={
                        "origen": "whatsapp",
                        "items": items,
                        "sucursal_id": self.sucursal_id,
                    },
                    headers=self.headers,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error al crear pedido: {e.response.status_code}")
                return {"success": False, "message": "No se pudo registrar el pedido"}
            except Exception as e:
                logger.error(f"Error inesperado al crear pedido: {e}")
                return {"success": False, "message": str(e)}


farmacia_service = FarmaciaService()