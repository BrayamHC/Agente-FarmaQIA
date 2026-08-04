import httpx
from app.config.settings import settings


class WhatsAppProvider:
    def __init__(self) -> None:
        self.base_url = (
            f"https://graph.facebook.com/{settings.WHATSAPP_API_VERSION}/"
            f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        )

    async def send_text_message(self, to: str, body: str) -> dict:
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
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