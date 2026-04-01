"""
Servicio de lógica del chatbot de Hidrocar.
Aquí vive toda la lógica de respuestas: reglas, menú, y (opcionalmente) IA.
"""

# --------------------------------------------------------------------------- #
# RESPUESTAS PREDEFINIDAS                                                       #
# --------------------------------------------------------------------------- #

MENU = (
    "👋 ¡Hola! Soy el asistente de *Hidrocar*.\n\n"
    "¿En qué te puedo ayudar?\n\n"
    "1️⃣ Qué es el sistema de electrólisis\n"
    "2️⃣ Compatibilidad con tu motor\n"
    "3️⃣ Ubicación y contacto\n"
    "4️⃣ Hablar con un asesor humano\n\n"
    "✍️ Escribe el número o tu pregunta directamente."
)

RESPUESTA_ELECTROLISIS = (
    "⚡ *Sistema Hidrocar de Electrólisis*\n\n"
    "Nuestro dispositivo usa electrólisis para separar el agua (H₂O) en "
    "hidrógeno (H₂) y oxígeno (O₂).\n\n"
    "Ese gas HHO se inyecta en la admisión del motor, logrando:\n"
    "✅ Mayor eficiencia en la combustión\n"
    "✅ Reducción de hasta un 30% en consumo de combustible\n"
    "✅ Menor emisión de gases contaminantes\n"
    "✅ Más potencia y respuesta del motor\n\n"
    "¿Quieres saber si es compatible con tu vehículo? Escribe *motor* o el cilindraje de tu auto. 🚗"
)

SOLICITUD_MOTOR = (
    "🔧 *Compatibilidad con motores*\n\n"
    "Nuestro sistema es compatible con motores a gasolina, diésel y GLP.\n\n"
    "Para confirmar la compatibilidad con tu vehículo, "
    "indícame el *cilindraje* de tu motor (ej: 1600cc, 2000cc, 2.0L) "
    "y la *marca/modelo* si lo tienes a mano.\n\n"
    "Te confirmo la compatibilidad al instante. 👇"
)

UBICACION = (
    "📍 *Ubicación de Hidrocar*\n\n"
    "Nos encontramos en:\n"
    "📌 Av. Ejemplo 1234, Lima, Perú\n"
    "🕘 Lunes a Viernes: 9am – 6pm\n"
    "🕘 Sábados: 9am – 1pm\n\n"
    "📞 Teléfono: +51 900 000 000\n"
    "🌐 Web: www.hidrocar.pe\n\n"
    "¿Deseas agendar una visita o tienes otra consulta?"
)

DERIVAR_HUMANO = (
    "🙋 *Conectándote con un asesor...*\n\n"
    "Un miembro de nuestro equipo se pondrá en contacto contigo "
    "en los próximos minutos.\n\n"
    "Si es urgente, también puedes llamarnos al:\n"
    "📞 +51 900 000 000\n\n"
    "¡Gracias por confiar en Hidrocar! 💧"
)

COMPATIBILIDAD_CONFIRMADA = (
    "✅ *¡Buenas noticias!*\n\n"
    "El sistema Hidrocar es compatible con motores en ese rango de cilindraje.\n\n"
    "¿Te gustaría conocer el precio, el proceso de instalación "
    "o agendar una cita con nuestros técnicos?\n\n"
    "Escribe tu consulta o escribe *asesor* para hablar con alguien del equipo."
)


# --------------------------------------------------------------------------- #
# MOTOR DE REGLAS                                                               #
# --------------------------------------------------------------------------- #

def get_reply(message: str) -> str:
    """
    Recibe el texto del usuario y retorna la respuesta apropiada.
    El orden de las condiciones importa: de más específico a más general.
    """
    text = message.lower().strip()

    # -- Opción 4 del menú: asesor humano
    if any(k in text for k in ["4", "asesor", "humano", "persona", "agente"]):
        return DERIVAR_HUMANO

    # -- Compatibilidad con motores / cilindraje  (va ANTES para capturar "1600cc" correctamente)
    if any(k in text for k in ["motor", "cc", "cilindraje", "gasolina", "diesel", "diésel", "glp", "cilindros"]) \
            or text.strip() == "2":
        # Si ya mencionó un número que parece cilindraje (ej: 1600, 2.0)
        if _contiene_cilindraje(text):
            return COMPATIBILIDAD_CONFIRMADA
        return SOLICITUD_MOTOR

    # -- Electrólisis / sistema / qué es
    if any(k in text for k in ["electrolisis", "electrólisis", "sistema", "hho", "hidrogeno", "hidrógeno"]) \
            or text.strip() == "1":
        return RESPUESTA_ELECTROLISIS

    # -- Ubicación / dónde / local
    if any(k in text for k in ["3", "ubicacion", "ubicación", "donde", "dónde", "local", "direccion", "dirección", "tienda"]):
        return UBICACION

    # -- Saludos (no mostrar menú completo, sólo bienvenida + menú)
    if any(k in text for k in ["hola", "buenas", "buenos", "hi", "hello", "inicio", "inicio", "start", "menu", "menú"]):
        return MENU

    # -- Precio
    if any(k in text for k in ["precio", "costo", "cuánto", "cuanto", "vale", "cuesta"]):
        return (
            "💰 *Precios Hidrocar*\n\n"
            "El precio varía según el tipo y cilindraje del motor.\n"
            "Para darte una cotización exacta, indícame:\n\n"
            "• Marca y modelo de tu vehículo\n"
            "• Cilindraje del motor\n\n"
            "O si prefieres, escribe *asesor* y te contactamos directamente. 👇"
        )

    # -- Fallback: menú principal
    return _fallback(text)


def _contiene_cilindraje(text: str) -> bool:
    """Detecta si el texto ya tiene información de cilindraje."""
    import re
    # Patrones: 1600cc, 2000 cc, 1.6l, 2.0 l, 1600
    patron = r"\b([\d]{3,4}\s?cc|[\d]\.\d\s?l(itros)?|[\d]{4})\b"
    return bool(re.search(patron, text, re.IGNORECASE))


def _fallback(text: str) -> str:
    """
    Respuesta cuando no se reconoce la intención del usuario.
    
    Aquí puedes integrar OpenAI como fallback:
    
    # --- INTEGRACIÓN OPENAI (descomentar para activar) ---
    # import openai, os
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    #
    # response = openai.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": (
    #                 "Eres el asistente de WhatsApp de Hidrocar, una empresa peruana "
    #                 "que vende un equipo que combina el agua (el gas hidrógeno obteniedo por electrólisis) para mejorar el rendimiento de la gasolina motores en potencia, reduciendo coste y cuidando el motor. "
    #                 "Responde en español, de forma breve y amigable. "
    #                 "Si no sabes algo, invita al usuario a hablar con un asesor."
    #             )
    #         },
    #         {"role": "user", "content": text}
    #     ],
    #     max_tokens=200,
    # )
    # return response.choices[0].message.content
    # --- FIN INTEGRACIÓN OPENAI ---
    """
    return MENU