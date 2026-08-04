import httpx
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self) -> None:
        self.base_url = (settings.nestjs_api_url or "").rstrip("/")
        self.api_key = settings.nestjs_internal_api_key
        self.sucursal_id = settings.farmacia_sucursal_id
        
        # Debug logging on initialization
        logger.info(f"InventoryService initialized: base_url={bool(self.base_url)}, api_key_set={bool(self.api_key)}, sucursal_id={self.sucursal_id}")

    def get_products_by_tags(self, tags: list[str], limite: int = 5) -> list[dict]:
        if not self.base_url or not self.api_key or not tags:
            logger.warning(
                f"No se pueden obtener productos: base_url={bool(self.base_url)}, "
                f"api_key={bool(self.api_key)}, tags_count={len(tags)}"
            )
            return []

        headers = {
            "x-internal-api-key": self.api_key,
            "x-sucursal-id": str(self.sucursal_id),
        }

        params = {
            "tags": ",".join(tags),
            "limite": limite,
            "stock_minimo": 1,
        }

        url = f"{self.base_url}/productos/recomendaciones"
        logger.info(f"Consultando NestJS: {url} con tags={tags}, params={params}")

        try:
            response = httpx.get(
                url,
                params=params,
                headers=headers,
                timeout=10.0,
            )
            logger.info(f"Respuesta de NestJS: status={response.status_code}, body={response.text[:200] if response.text else 'empty'}")
            response.raise_for_status()
            data = response.json()
            productos = data.get("productos", [])
            logger.info(f"Productos obtenidos: {len(productos)}")
            return productos
        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP {e.response.status_code} desde NestJS: {e.response.text}")
            return []
        except httpx.RequestError as e:
            logger.error(f"Error de conexión con NestJS ({self.base_url}): {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado al obtener recomendaciones: {e}")
            return []


inventory_service = InventoryService()