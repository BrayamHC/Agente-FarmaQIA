from pydantic import BaseModel


class WhatsAppTextMessage(BaseModel):
    body: str


class WhatsAppMessage(BaseModel):
    from_: str | None = None
    id: str | None = None
    text: WhatsAppTextMessage | None = None
    type: str | None = None

    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class WhatsAppValue(BaseModel):
    messages: list[dict] | None = None


class WhatsAppChange(BaseModel):
    value: dict
    field: str


class WhatsAppEntry(BaseModel):
    id: str
    changes: list[WhatsAppChange]


class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: list[WhatsAppEntry]