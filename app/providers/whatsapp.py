import httpx
from app.config.settings import settings


class WhatsAppProvider:
    def __init__(self) -> None:
        self.base_url = (
            f"https://graph.facebook.com/{settings.whatsapp_api_version}/"
            f"{settings.whatsapp_phone_number_id}/messages"
        )

    async def send_text_message(self, to: str, body: str) -> dict:
        headers = {
            "Authorization": f"Bearer {settings.whatsapp_access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": body},
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.base_url, headers=headers, json=payload)
            if response.is_error:
                print("WhatsApp response status:", response.status_code)
                print("WhatsApp response body:", response.text)
            response.raise_for_status()
            return response.json()


whatsapp_provider = WhatsAppProvider()