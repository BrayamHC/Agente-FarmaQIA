import re

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

# Cada entrada: patrón regex -> lista de tags a activar
TAG_MAP: list[tuple[str, list[str]]] = [
    # Dolor general y musculoesquelético
    (r"dolor",              ["dolor"]),
    (r"duele",              ["dolor"]),
    (r"molesti",            ["dolor"]),
    (r"espalda",            ["dolor", "espalda", "musculo"]),
    (r"columna",            ["dolor", "espalda", "musculo"]),
    (r"articulaci",         ["dolor", "articulacion"]),
    (r"rodilla",            ["dolor", "articulacion"]),
    (r"cuello",             ["dolor", "musculo"]),
    (r"m[uú]sculo",        ["dolor", "musculo"]),
    (r"contractura",        ["dolor", "musculo"]),
    (r"lumbar",             ["dolor", "espalda", "musculo"]),
    (r"cabeza",             ["dolor", "cabeza"]),
    (r"migra[ñn]",         ["dolor", "cabeza", "migrana"]),
    # Respiratorio
    (r"grip[ae]",          ["gripa", "resfriado"]),
    (r"resfri",            ["gripa", "resfriado"]),
    (r"tos",               ["tos"]),
    (r"congesti",          ["congestion", "resfriado"]),
    (r"mocos",             ["congestion", "resfriado"]),
    (r"garganta",          ["garganta", "dolor"]),
    (r"fiebre",            ["fiebre"]),
    (r"temperatura",       ["fiebre"]),
    # Digestivo
    (r"n[aá]usea",         ["nauseas"]),
    (r"v[oó]mito",         ["nauseas", "vomito"]),
    (r"estómago|estomago", ["estomago", "dolor"]),
    (r"diarrea",           ["diarrea"]),
    (r"estreñ",            ["estrenimiento"]),
    (r"gastritis",         ["gastritis", "estomago"]),
    (r"acidez",            ["gastritis", "estomago"]),
    # Alergia / piel
    (r"alergi",            ["alergia"]),
    (r"picaz[oó]n",       ["alergia", "piel"]),
    (r"comezon|comezón",  ["alergia", "piel"]),
    (r"ronchas",           ["alergia", "piel"]),
]


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
                    "Productos disponibles en inventario que pueden ayudar al cliente:\n"
                    f"{inventory_context}\n\n"
                    "IMPORTANTE: Menciona estos productos por nombre en tu respuesta. "
                    "El cliente debe saber qué productos específicos tenemos disponibles. "
                    "Nunca menciones precios de caducidad ni que fueron seleccionados por fecha."
                ),
            })

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})
        return messages

    def extract_tags(self, user_message: str) -> list[str]:
        texto = user_message.lower()
        tags: set[str] = set()

        for pattern, tag_list in TAG_MAP:
            if re.search(pattern, texto):
                tags.update(tag_list)

        return list(tags)

    def format_inventory_context(self, productos: list[dict]) -> str:
        if not productos:
            return ""

        lineas: list[str] = []
        for p in productos:
            precio = float(p.get("precio_publico") or 0)
            stock = int(p.get("stock_disponible") or 0)
            presentacion = p.get("presentacion") or "N/A"
            lineas.append(
                f"- {p['nombre']} | {presentacion} | "
                f"Precio: ${precio:.2f} | Stock: {stock} unidades"
            )

        return "\n".join(lineas)


prompt_service = PromptService()