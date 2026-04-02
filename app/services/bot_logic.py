"""
bot_logic.py
Motor de respuestas del chatbot Hidrocar.
Recibe el mensaje enriquecido con contexto y devuelve la respuesta correcta.
"""

import re
import os
from app.services.extractor import esta_en_lima

# --------------------------------------------------------------------------- #
# RESPUESTAS                                                                    #
# --------------------------------------------------------------------------- #

MENU = (
    "👋 ¡Hola! Soy el asistente de *Hidrocar*.\n\n"
    "¿En qué te puedo ayudar hoy?\n\n"
    "1️⃣ Cómo funciona el equipo y sus beneficios\n"
    "2️⃣ Compatibilidad con tu motor\n"
    "3️⃣ Precios y costos\n"
    "4️⃣ Ubicación y cómo llegar\n"
    "5️⃣ Garantía y mantenimiento\n"
    "6️⃣ Hablar con un asesor\n\n"
    "✍️ Escribe el número o hazme tu pregunta directamente."
)

RESPUESTA_ELECTROLISIS = (
    "⚡ *¿Cómo funciona el sistema Hidrocar?*\n\n"
    "Nuestro equipo usa electricidad del propio vehículo para separar el agua (H₂O) "
    "en hidrógeno (H₂) y oxígeno (O₂) mediante electrólisis.\n\n"
    "Ese gas se inyecta directamente en la cámara de combustión del motor, logrando:\n\n"
    "✅ *Mayor potencia* y combustión más eficiente\n"
    "✅ *Hasta 20% menos* en consumo de combustible\n"
    "✅ *50% menos* de emisiones contaminantes\n"
    "✅ *10–20% más* de vida útil del motor\n\n"
    "Es compatible con motores a gasolina, diésel y GLP. "
    "¿Quieres saber si funciona con tu vehículo? Escríbeme el cilindraje (ej: 1600, 2000cc) 🚗"
)

SOLICITUD_MOTOR = (
    "🔧 *Compatibilidad con motores*\n\n"
    "¡Buenas noticias! El sistema Hidrocar funciona con *todo tipo de cilindraje* "
    "— gasolina, diésel y GLP.\n\n"
    "Para darte el costo exacto y confirmar el modelo ideal para tu vehículo, "
    "indícame:\n\n"
    "• El *cilindraje* de tu motor (ej: 1600cc, 2.0L)\n"
    "• La *marca y modelo* si lo tienes a mano\n\n"
    "Te respondo al instante 👇"
)

COMPATIBILIDAD_CONFIRMADA = (
    "✅ *¡Compatible sin problema!*\n\n"
    "El sistema Hidrocar funciona perfectamente con ese motor.\n\n"
    "¿Qué quieres hacer ahora?\n\n"
    "💰 Escribe *precio* para ver el costo\n"
    "📍 Escribe *ubicacion* para saber cómo llegar\n"
    "🙋 Escribe *asesor* para que te contactemos directamente"
)

def _precio(ctx: dict) -> str:
    motor = ctx.get("motor")
    ubicacion = ctx.get("ubicacion")
    en_lima = esta_en_lima(ubicacion)

    if not motor:
        return (
            "💰 *Precios Hidrocar*\n\n"
            "El costo varía según el cilindraje de tu motor.\n\n"
            "Indícame el *cilindraje* (ej: 1600cc, 2000cc) y te doy el precio exacto "
            "para tu vehículo. 👇"
        )

    base = (
        f"💰 *Precio para motor {motor}*\n\n"
        "• Equipo: *XXX soles*\n"
        "• Instalación: *XXX soles*\n\n"
    )

    if en_lima:
        return base + (
            "La instalación la hacemos en nuestro taller en Ventanilla, Lima. "
            "Incluye evaluación del vehículo sin costo adicional. 🔧\n\n"
            "¿Te gustaría agendar una cita? Escribe *asesor* y te contactamos."
        )
    elif ubicacion and ubicacion != "NA":
        return base + (
            f"Veo que estás en *{ubicacion}*. En ese caso podemos *enviarte el equipo* "
            "para que lo instale tu mecánico de confianza — también podemos guiarlo "
            "paso a paso si lo necesita. 📦\n\n"
            "¿Te interesa? Escribe *asesor* y coordinamos el envío."
        )
    else:
        return base + (
            "Si estás en Lima, la instalación la hacemos en nuestro taller en Ventanilla.\n"
            "Si estás en provincias, enviamos el equipo para que lo instale tu mecánico. 📦\n\n"
            "¿Dónde te encuentras? Así te doy el detalle exacto."
        )

UBICACION = (
    "📍 *Dónde encontrarnos*\n\n"
    "📌 *Calle Canopus 201, Ventanilla, Lima*\n"
    "🕘 Atención: todos los días de *8am a 10pm*\n"
    "📞 *+51 962 691 600*\n\n"
    "Si estás en provincias no hay problema — "
    "enviamos el equipo a todo el Perú 🇵🇪\n\n"
    "¿Deseas agendar una visita o tienes alguna otra consulta?"
)

GARANTIA = (
    "🛡️ *Garantía y Mantenimiento*\n\n"
    "*Garantía:* 1 año en todos nuestros equipos.\n\n"
    "*Mantenimiento:*\n"
    "Para que el equipo opere en óptimas condiciones, "
    "recomendamos mantenimiento cada *8 meses a 1 año* "
    "(dependiendo del uso del vehículo y condiciones externas).\n\n"
    "💰 Costo del mantenimiento: *250 soles*\n\n"
    "Si no puedes venir a nuestro taller, no hay problema — "
    "podemos explicarle el procedimiento al mecánico de tu confianza para que lo realice. 🔧\n\n"
    "¿Tienes alguna otra consulta?"
)

INSTALACION_CONTACTO = (
    "🔧 *Instalación del sistema Hidrocar*\n\n"
    "La instalación incluye:\n"
    "✅ Evaluación del vehículo sin costo\n"
    "✅ Instalación por técnicos certificados\n"
    "✅ Prueba de funcionamiento al terminar\n\n"
    "📍 *Calle Canopus 201, Ventanilla, Lima*\n"
    "📞 *+51 962 691 600*\n\n"
    "Si estás en provincias podemos enviarte el equipo 📦 "
    "y guiar a tu mecánico en la instalación.\n\n"
    "Escribe *asesor* y coordinamos todo. 👇"
)

DERIVAR_HUMANO = (
    "🙋 *Hablemos directamente*\n\n"
    "Nuestro equipo está listo para ayudarte con tu consulta, "
    "guiarte en la compra o coordinar la instalación.\n\n"
    "📞 *+51 962 691 600*\n"
    "🕘 Disponibles todos los días de *8am a 10pm*\n\n"
    "Puedes llamarnos o escribirnos por este mismo WhatsApp. "
    "¡Gracias por confiar en Hidrocar! 💧"
)

GRACIAS = (
    "😊 ¡Con gusto! Estoy aquí si tienes más preguntas.\n\n"
    "Escribe *menu* para ver todas las opciones "
    "o *asesor* para hablar con alguien del equipo. 👋"
)


# --------------------------------------------------------------------------- #
# MOTOR DE REGLAS                                                               #
# --------------------------------------------------------------------------- #

def get_reply(message: str, ctx: dict = {}) -> str:
    # Limpiar tag de contexto antes de evaluar reglas
    clean_message = re.sub(r"\[motor:.*?\]", "", message, flags=re.IGNORECASE).strip()
    text = clean_message.lower().strip()

    # Asesor / opción 6
    if _ok(text, ["asesor", "humano", "persona", "agente", "llamar",
                  "llamame", "llámame", "contactar", "quiero hablar"]) or text.startswith("6"):
        return DERIVAR_HUMANO

    # Garantía / mantenimiento / opción 5
    if _ok(text, ["garantia", "garantía", "mantenimiento", "vida util",
                  "vida útil", "duracion", "duración", "cuanto dura",
                  "cuánto dura"]) or text.startswith("5"):
        return GARANTIA

    # Instalación
    if _ok(text, ["instalar", "instalacion", "instalación", "quiero instalar",
                  "como me contacto", "cómo me contacto", "visita",
                  "servicio a domicilio", "vienen a", "van a"]):
        return INSTALACION_CONTACTO

    # Cilindraje suelto — usuario responde "1600" al flujo de motor
    if _es_solo_cilindraje(text):
        return COMPATIBILIDAD_CONFIRMADA

    # Motor / compatibilidad / opción 2
    if _ok(text, ["motor", "cc", "cilindraje", "gasolina", "diesel", "diésel",
                  "glp", "cilindros", "compatible", "funciona con",
                  "sirve para"]) or text.startswith("2"):
        if _contiene_cilindraje(text):
            return COMPATIBILIDAD_CONFIRMADA
        return SOLICITUD_MOTOR

    # Electrólisis / cómo funciona / opción 1
    if _ok(text, ["electrolisis", "electrólisis", "sistema", "hho", "hidrogeno",
                  "hidrógeno", "que es", "qué es", "como funciona",
                  "cómo funciona", "para que sirve", "para qué sirve",
                  "beneficios", "ventajas"]) or text.startswith("1"):
        return RESPUESTA_ELECTROLISIS

    # Precio / costo / opción 3
    if _ok(text, ["precio", "costo", "cuánto", "cuanto", "vale", "cuesta",
                  "cobran", "tarifa", "cotizacion", "cotización",
                  "cuanto sale", "cuánto sale"]) or text.startswith("3"):
        return _precio(ctx)

    # Ubicación / opción 4
    if _ok(text, ["ubicacion", "ubicación", "donde", "dónde", "local", "taller",
                  "direccion", "dirección", "tienda", "como llegar",
                  "cómo llegar", "queda", "quedan",
                  "vivo en", "estoy en", "soy de", "vivo", "estoy"]) or text.startswith("4"):
        return UBICACION

    # Saludos / menú
    if _ok(text, ["hola", "buenas", "buenos", "hi", "hello", "buen dia",
                  "buen día", "start", "menu", "menú", "inicio", "opciones"]):
        return MENU

    # Agradecimientos
    if _ok(text, ["gracias", "ok", "okay", "perfecto", "listo", "genial",
                  "excelente", "entendido", "de acuerdo", "dale", "claro",
                  "chevere", "chévere"]):
        return GRACIAS

    # Fallback → OpenAI
    return _fallback(message, ctx)



def es_derivacion_humano(message: str) -> bool:
    """
    Detecta si el mensaje del usuario activa la derivación a asesor.
    Lo usa webhook.py para saber si debe notificar al asesor.
    """
    text = re.sub(r"\[motor:.*?\]", "", message, flags=re.IGNORECASE).lower().strip()
    return (
        any(k in text for k in ["asesor", "humano", "persona", "agente",
                                  "llamar", "llamame", "llámame",
                                  "contactar", "quiero hablar"])
        or text.startswith("6")
    )

# --------------------------------------------------------------------------- #
# HELPERS                                                                       #
# --------------------------------------------------------------------------- #

def _ok(text: str, keywords: list) -> bool:
    return any(k in text for k in keywords)


def _contiene_cilindraje(text: str) -> bool:
    patron = r"\b(\d{3,4}\s?cc|\d\.\d\s?l(itros)?|\d{4})\b"
    return bool(re.search(patron, text, re.IGNORECASE))


def _es_solo_cilindraje(text: str) -> bool:
    # Captura "1600", "1600cc", "2.0l" solos sin contexto adicional
    patron = r"^\s*\d{3,4}\s*(cc?)?\s*$"
    return bool(re.match(patron, text, re.IGNORECASE))


def _fallback(message: str, ctx: dict) -> str:
    """
    Fallback con OpenAI — responde preguntas no cubiertas por las reglas.
    Siempre orienta hacia la conversión (compra o contacto con asesor).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "No entendí bien tu consulta 😅\n\n"
            "Puedes escribir:\n"
            "1️⃣ Cómo funciona el sistema\n"
            "2️⃣ Compatibilidad con tu motor\n"
            "3️⃣ Precios\n"
            "4️⃣ Ubicación\n"
            "5️⃣ Garantía y mantenimiento\n"
            "6️⃣ Hablar con un asesor\n\n"
            "O cuéntame tu consulta directamente. 👇"
        )

    motor    = ctx.get("motor") or "no informado"
    ubicacion = ctx.get("ubicacion") or "no informada"

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=220,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres el asistente de WhatsApp de Hidrocar, empresa peruana que vende "
                        "sistemas de electrólisis para mejorar el rendimiento de motores de vehículos.\n\n"
                        "Datos del producto:\n"
                        "- Usa electrólisis para generar gas HHO que se inyecta al motor\n"
                        "- Beneficios: hasta 20% menos combustible, 50% menos emisiones, mayor vida útil del motor\n"
                        "- Compatible con gasolina, diésel y GLP, cualquier cilindraje\n"
                        "- Precio: varía según cilindraje (poner XXX si preguntan precio exacto)\n"
                        "- Garantía: 1 año. Mantenimiento: 250 soles cada 8-12 meses\n"
                        "- Taller: Calle Canopus 201, Ventanilla, Lima. Tel: +51 962 691 600\n"
                        "- Horario: 8am–10pm todos los días\n"
                        "- Envíos a provincias disponibles\n\n"
                        f"Contexto del cliente:\n"
                        f"- Motor: {motor}\n"
                        f"- Ubicación: {ubicacion}\n\n"
                        "Instrucciones:\n"
                        "- Responde en español, de forma cálida, breve (máx 3 párrafos cortos) y amigable\n"
                        "- Usa emojis con moderación\n"
                        "- SIEMPRE termina orientando hacia una acción concreta: "
                        "agendar, cotizar, escribir 'asesor' o llamar al +51 962 691 600\n"
                        "- Si no sabes algo, dilo con honestidad e invita al cliente a hablar con un asesor\n"
                        "- Nunca inventes precios exactos, solo di que varían según el cilindraje"
                    )
                },
                {"role": "user", "content": message}
            ],
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "Disculpa, tuve un problema procesando tu consulta 😅\n\n"
            "Puedes escribirnos directamente al *+51 962 691 600* "
            "o escribir *asesor* y te contactamos. 🙋"
        )