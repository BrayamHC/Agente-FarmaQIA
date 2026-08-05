import httpx
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


class InventoryService:
    """
    Servicio síncrono para obtener productos por tags desde NestJS.
    Usado en el flujo síncrono de chat_service.
    """
    
    def __init__(self) -> None:
        self.base_url = settings.nestjs_api_url.rstrip("/") if settings.nestjs_api_url else ""
        self.api_key = settings.nestjs_internal_api_key
        self.sucursal_id = settings.farmacia_sucursal_id
        logger.info(
            f"InventoryService initialized: base_url={'✓' if self.base_url else '✗'}, "
            f"sucursal_id={self.sucursal_id}"
        )

    def get_products_by_tags(self, tags: list[str], limite: int = 5) -> list[dict]:
        """
        Obtiene productos recomendados basados en tags/síntomas.
        
        Args:
            tags: Lista de tags para buscar productos
            limite: Máximo número de productos a retornar
            
        Returns:
            list[dict]: Lista de productos con su información básica
        """
        if not self.base_url:
            logger.error("NESTJS_API_URL no configurada")
            return []
            
        if not tags:
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

        try:
            logger.info(f"Consultando inventario: tags={tags}, limite={limite}")
            response = httpx.get(
                f"{self.base_url}/productos/recomendaciones",
                params=params,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            productos = data.get("productos", [])
            logger.info(f"Inventario obtenido: {len(productos)} productos encontrados")
            return productos
        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP al obtener inventario: {e.response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Error al obtener recomendaciones: {e}")
            return []


inventory_service = InventoryService()