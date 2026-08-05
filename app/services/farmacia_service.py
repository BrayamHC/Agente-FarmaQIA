import httpx
import logging
from typing import Optional
from app.config.settings import settings

logger = logging.getLogger(__name__)


class ProductoRecomendacionService:
    """
    Servicio dedicado a obtener recomendaciones de productos desde NestJS.
    Consume el endpoint GET /productos/recomendaciones con tags, aplicando FEFO.
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
            f"ProductoRecomendacionService initialized: base_url={'✓' if self.base_url else '✗'}, "
            f"api_key_set={'✓' if self.api_key else '✗'}, sucursal_id={self.sucursal_id}"
        )

    async def obtener_recomendaciones(
        self,
        tags: list[str],
        limite: int = 8,
        stock_minimo: int = 1,
    ) -> dict:
        """
        Consulta productos por tags aplicando FEFO en NestJS.
        Retorna lista limpia sin información de caducidad.
        
        Args:
            tags: Lista de tags/síntomas para buscar productos
            limite: Máximo número de productos a retornar
            stock_minimo: Stock mínimo requerido
            
        Returns:
            dict con estructura: {"success": bool, "total": int, "productos": list}
        """
        if not self.base_url:
            logger.error("NESTJS_API_URL no configurada")
            return {"success": False, "total": 0, "productos": []}
        
        if not tags:
            logger.warning("No se proporcionaron tags para la búsqueda")
            return {"success": False, "total": 0, "productos": []}

        params = {
            "tags": ",".join(tags),
            "limite": limite,
            "stock_minimo": stock_minimo,
        }
        
        logger.info(f"Consultando NestJS: {self.base_url}/productos/recomendaciones con tags={tags}")

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/productos/recomendaciones",
                    params=params,
                    headers=self.headers,
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Respuesta de NestJS: status={response.status_code}, total={data.get('total', 0)} productos")
                return data
            except httpx.HTTPStatusError as e:
                logger.error(f"Error HTTP desde NestJS: {e.response.status_code} - {e.response.text[:200]}")
                return {"success": False, "total": 0, "productos": []}
            except httpx.TimeoutException as e:
                logger.error(f"Timeout al conectar con NestJS: {e}")
                return {"success": False, "total": 0, "productos": []}
            except Exception as e:
                logger.error(f"Error al conectar con NestJS: {e}")
                return {"success": False, "total": 0, "productos": []}


producto_recomendacion_service = ProductoRecomendacionService()