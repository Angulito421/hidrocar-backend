"""
Servicio de lógica del chatbot de Hidrocar.
"""

import re

# --------------------------------------------------------------------------- #
# RESPUESTAS                                                                    #
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
    "¿Quieres saber si es compatible con tu vehículo? "
    "Escribe tu *cilindraje* (ej: 1600, 2000cc) o *motor* para más info. 🚗"
)

SOLICITUD_MOTOR = (
    "🔧 *Compatibilidad con motores*\n\n"
    "Nuestro sistema es compatible con motores a gasolina, diésel y GLP.\n\n"
    "Para confirmar la compatibilidad, indícame el *cilindraje* de tu motor "
    "(ej: 1600, 2000cc, 2.0L) y la marca/modelo si lo tienes a mano.\n\n"
    "Te confirmo al instante. 👇"
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
    "El sistema Hidrocar es compatible con ese motor. ¡Sin problema!\n\n"
    "¿Qué te gustaría hacer ahora?\n\n"
    "💰 Escribe *precio* para conocer el costo\n"
    "📍 Escribe *ubicacion* para ver dónde instalamos\n"
    "🙋 Escribe *asesor* para que te contactemos directamente"
)

INSTALACION_CONTACTO = (
    "🔧 *Instalación del sistema Hidrocar*\n\n"
    "La instalación la realizamos en nuestro taller, incluye:\n"
    "✅ Evaluación del vehículo sin costo\n"
    "✅ Instalación por técnicos certificados\n"
    "✅ Prueba de funcionamiento al final\n\n"
    "📍 Nos encontramos en *Av. Ejemplo 1234, Lima*\n"
    "📞 Llámanos al *+51 900 000 000* para agendar\n\n"
    "También puedes escribir *asesor* y nosotros te llamamos. 👇"
)

PRECIO = (
    "💰 *Precios Hidrocar*\n\n"
    "El precio varía según el cilindraje del motor.\n\n"
    "Para una cotización exacta escribe *asesor* "
    "y te contactamos con el precio para tu vehículo específico. 👇"
)

GRACIAS = (
    "😊 ¡Con gusto! Si tienes otra consulta escríbeme.\n\n"
    "Puedes escribir *menu* para ver todas las opciones "
    "o *asesor* para hablar con alguien del equipo. 👋"
)


# --------------------------------------------------------------------------- #
# MOTOR DE REGLAS                                                               #
# --------------------------------------------------------------------------- #

def get_reply(message: str) -> str:
    text = message.lower().strip()

    # Asesor / contactar directamente
    if _ok(text, ["asesor", "humano", "persona", "agente", "llamar",
                  "llamame", "llámame", "contactar"]) or text == "4":
        return DERIVAR_HUMANO

    # Instalación / cómo me contacto
    if _ok(text, ["instalar", "instalacion", "instalación", "quiero instalar",
                  "como me contacto", "cómo me contacto", "visita",
                  "servicio a domicilio", "vienen a", "van a"]):
        return INSTALACION_CONTACTO

    # Cilindraje suelto — usuario respondió "1600" al flujo de motor
    if _es_solo_cilindraje(text):
        return COMPATIBILIDAD_CONFIRMADA

    # Motor / compatibilidad / opción 2
    if _ok(text, ["motor", "cc", "cilindraje", "gasolina", "diesel", "diésel",
                  "glp", "cilindros", "compatible", "funciona con"]) or text == "2":
        if _contiene_cilindraje(text):
            return COMPATIBILIDAD_CONFIRMADA
        return SOLICITUD_MOTOR

    # Electrólisis / sistema / opción 1
    if _ok(text, ["electrolisis", "electrólisis", "sistema", "hho", "hidrogeno",
                  "hidrógeno", "que es", "qué es", "como funciona",
                  "cómo funciona", "para que sirve", "para qué sirve"]) or text == "1":
        return RESPUESTA_ELECTROLISIS

    # Ubicación / opción 3
    if _ok(text, ["ubicacion", "ubicación", "donde", "dónde", "local", "taller",
                  "direccion", "dirección", "tienda", "lurigancho", "lima",
                  "zona", "distrito", "queda", "quedan"]) or text == "3":
        return UBICACION

    # Precio
    if _ok(text, ["precio", "costo", "cuánto", "cuanto", "vale", "cuesta",
                  "cobran", "tarifa", "cotizacion", "cotización"]):
        return PRECIO

    # Saludos
    if _ok(text, ["hola", "buenas", "buenos", "hi", "hello", "buen dia",
                  "buen día", "start", "menu", "menú", "inicio"]):
        return MENU

    # Agradecimientos / confirmaciones positivas
    if _ok(text, ["gracias", "ok", "okay", "perfecto", "listo", "genial",
                  "excelente", "entendido", "de acuerdo", "dale", "claro"]):
        return GRACIAS

    return _fallback(text)


# --------------------------------------------------------------------------- #
# HELPERS                                                                       #
# --------------------------------------------------------------------------- #

def _ok(text: str, keywords: list) -> bool:
    return any(k in text for k in keywords)


def _contiene_cilindraje(text: str) -> bool:
    patron = r"\b(\d{3,4}\s?cc|\d\.\d\s?l(itros)?|\d{4})\b"
    return bool(re.search(patron, text, re.IGNORECASE))


def _es_solo_cilindraje(text: str) -> bool:
    """El usuario mandó solo un número tipo '1600' o '1600cc' sin más contexto."""
    patron = r"^\s*\d{3,4}\s*(cc?)?\s*$"
    return bool(re.match(patron, text, re.IGNORECASE))


def _fallback(text: str) -> str:
    """
    # --- INTEGRACIÓN OPENAI (descomentar para activar) ---
    # import openai, os
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # response = openai.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": (
    #             "Eres el asistente de WhatsApp de Hidrocar, empresa peruana "
    #             "que vende sistemas de electrólisis para mejorar motores. "
    #             "Responde en español, breve y amigable. "
    #             "Si no sabes algo, invita a hablar con un asesor."
    #         )},
    #         {"role": "user", "content": text}
    #     ],
    #     max_tokens=200,
    # )
    # return response.choices[0].message.content
    # --- FIN INTEGRACIÓN OPENAI ---
    """
    return (
        "No entendí bien tu consulta 😅\n\n"
        "Puedes escribir:\n"
        "1️⃣ Qué es el sistema\n"
        "2️⃣ Compatibilidad con tu motor\n"
        "3️⃣ Ubicación\n"
        "4️⃣ Hablar con un asesor\n\n"
        "O escribe tu pregunta directamente. 👇"
    )