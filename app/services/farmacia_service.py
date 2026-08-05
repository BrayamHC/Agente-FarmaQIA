import httpx
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


class FarmaciaService:
    """Conecta el microservicio con el backend NestJS de FarmaQ."""

    def _get_headers(self) -> dict:
        """Lee settings en tiempo de ejecución, no en construcción."""
        return {
            "x-internal-api-key": settings.NESTJS_INTERNAL_API_KEY,
            "x-sucursal-id": str(settings.FARMACIA_SUCURSAL_ID),
        }

    async def obtener_recomendaciones(
        self,
        tags: list[str],
        limite: int = 8,
        stock_minimo: int = 1,
    ) -> dict:
        base_url = settings.NESTJS_API_URL.rstrip("/")

        if not base_url:
            logger.warning("NESTJS_API_URL no configurada — omitiendo consulta de inventario")
            return {"success": False, "total": 0, "productos": []}

        if not tags:
            return {"success": False, "total": 0, "productos": []}

        url = f"{base_url}/productos/recomendaciones"
        params = {
            "tags": ",".join(tags),
            "limite": limite,
            "stock_minimo": stock_minimo,
        }
        logger.info(f"Consultando NestJS → {url} | tags={tags} | params={params}")

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, params=params, headers=self._get_headers())
                logger.info(f"NestJS respondió {response.status_code} | body={response.text[:300]}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"Error HTTP desde NestJS: {e.response.status_code} | "
                    f"body={e.response.text[:300]}"
                )
                return {"success": False, "total": 0, "productos": []}
            except Exception as e:
                logger.error(f"Error al conectar con NestJS: {e}")
                return {"success": False, "total": 0, "productos": []}

    async def crear_pedido(self, items: list[dict]) -> dict:
        base_url = settings.NESTJS_API_URL.rstrip("/")

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{base_url}/pedidos",
                    json={
                        "origen": "whatsapp",
                        "items": items,
                        "sucursal_id": settings.FARMACIA_SUCURSAL_ID,
                    },
                    headers=self._get_headers(),
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