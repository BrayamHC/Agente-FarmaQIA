import httpx
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self) -> None:
        self.base_url = settings.nestjs_api_url.rstrip("/") if settings.nestjs_api_url else ""
        self.api_key = settings.nestjs_internal_api_key
        self.sucursal_id = settings.farmacia_sucursal_id

    def get_products_by_tags(self, tags: list[str], limite: int = 5) -> list[dict]:
        if not self.base_url or not tags:
            return []

        headers = {
            "x-internal-api-key": self.api_key,
            "x-sucursal-id": self.sucursal_id,
        }

        params = {
            "tags": ",".join(tags),
            "limite": limite,
            "stock_minimo": 1,
        }

        try:
            response = httpx.get(
                f"{self.base_url}/productos/recomendaciones",
                params=params,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("productos", [])
        except Exception as e:
            logger.error(f"Error al obtener recomendaciones: {e}")
            return []


inventory_service = InventoryService()