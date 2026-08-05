import os
import httpx


class InventoryService:
    def __init__(self) -> None:
        self.base_url = os.getenv("NESTJS_API_URL", "").rstrip("/")
        self.api_key = os.getenv("NESTJS_INTERNAL_API_KEY", "")
        self.sucursal_id = os.getenv("FARMACIA_SUCURSAL_ID", "1")

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
                f"{self.base_url}/productos/recomendaciones/tags",
                params=params,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("productos", [])
        except Exception:
            return []


inventory_service = InventoryService()