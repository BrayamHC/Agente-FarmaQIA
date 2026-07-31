SYSTEM_PROMPT = """
Eres el asistente virtual de una farmacia. Tu rol es el de un asesor
farmacéutico amable y profesional.

Reglas estrictas:
- Nunca diagnosticas enfermedades.
- Nunca prescribes tratamientos ni dosis.
- Nunca sustituyes la opinión de un médico.
- Si detectas síntomas graves o preocupantes, recomienda acudir a un
  médico o servicio de urgencias de inmediato.
- Puedes explicar información general sobre medicamentos.
- No menciones información interna del inventario ni fechas de caducidad.
- Mantienes un tono cálido, claro y profesional.
"""


class PromptService:
    def build_messages(
        self,
        user_message: str,
        history: list[dict] | None = None,
        inventory_context: str | None = None,
    ) -> list[dict]:
        messages = [{"role": "system", "content": SYSTEM_PROMPT.strip()}]

        if inventory_context:
            messages.append({
                "role": "system",
                "content": (
                    "Contexto interno de inventario disponible:\n"
                    f"{inventory_context}\n\n"
                    "Usa esta información solo para recomendar productos disponibles. "
                    "Nunca menciones al cliente que fueron priorizados por caducidad."
                ),
            })

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})
        return messages

    def extract_tags(self, user_message: str) -> list[str]:
        texto = user_message.lower()

        mapa = {
            "gripa": ["gripa", "gripe", "resfriado"],
            "gripe": ["gripa", "gripe", "resfriado"],
            "tos": ["tos"],
            "congestión": ["congestión", "resfriado"],
            "congestion": ["congestión", "resfriado"],
            "dolor muscular": ["dolor muscular", "músculo"],
            "dolores musculares": ["dolor muscular", "músculo"],
            "músculo": ["músculo"],
            "musculo": ["músculo"],
            "fiebre": ["fiebre"],
            "dolor": ["dolor"],
        }

        tags: set[str] = set()

        for clave, valores in mapa.items():
            if clave in texto:
                tags.update(valores)

        return list(tags)

    def format_inventory_context(self, productos: list[dict]) -> str:
        if not productos:
            return "No hay productos disponibles para esos tags."

        lineas: list[str] = []
        for producto in productos:
            lineas.append(
                f"- ID: {producto['producto_id']} | "
                f"SKU: {producto['sku']} | "
                f"Nombre: {producto['nombre']} | "
                f"Presentación: {producto.get('presentacion') or 'N/A'} | "
                f"Precio: ${float(producto.get('precio_publico') or 0):.2f} | "
                f"Stock: {int(producto.get('stock_disponible') or 0)}"
            )

        return "\n".join(lineas)


prompt_service = PromptService()