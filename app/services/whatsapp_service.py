from app.providers.whatsapp import whatsapp_provider
from app.services.chat_service import chat_service


class WhatsAppService:
    async def process_incoming_message(self, payload: dict) -> None:
        entries = payload.get("entry", [])

        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    if message.get("type") != "text":
                        continue

                    from_number = message.get("from")
                    text = message.get("text", {}).get("body", "").strip()

                    if not from_number or not text:
                        continue

                    reply = chat_service.handle_message(text)

                    try:
                        await whatsapp_provider.send_text_message(
                            to=from_number,
                            body=reply[:4096],
                        )
                    except Exception as error:
                        print(f"WhatsApp send error: {error}")


whatsapp_service = WhatsAppService()