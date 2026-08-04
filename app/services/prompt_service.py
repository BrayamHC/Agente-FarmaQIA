SYSTEM_PROMPT = """
Eres el asistente virtual de FarmaQIA. Tu rol es el de un asesor
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

Instrucción de venta:
- Cuando recomiendes productos disponibles, SIEMPRE termina tu mensaje
  invitando amablemente al cliente a ACERCARSE A LA FARMACIA para adquirirlos.
- Menciona que tenemos atención rápida y los productos están disponibles
  para entrega inmediata.
- Ejemplo de cierre: "Te invito a visitarnos en nuestra sucursal más cercana
  para que puedas adquirirlo. ¡Con gusto te atendemos!"
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

        # Mapa simplificado: clave = palabra a buscar, valor = tags a activar
        mapa = {
            "gripa": ["gripa", "resfriado"],
            "gripe": ["gripa", "resfriado"],
            "resfriado": ["gripa", "resfriado"],
            "tos": ["tos"],
            "congestión": ["congestion", "resfriado"],
            "congestion": ["congestion", "resfriado"],
            "dolor muscular": ["dolor", "musculo"],
            "dolores musculares": ["dolor", "musculo"],
            "músculo": ["musculo"],
            "musculo": ["musculo"],
            "fiebre": ["fiebre"],
            "dolor": ["dolor"],
            "náuseas": ["nauseas", "náuseas", "vómito"],
            "cabeza": ["cabeza", "dolor"],
            "estómago": ["estomago"],
            "estomago": ["estomago"],
            "diarrea": ["diarrea"],
            "alergia": ["alergia"],
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