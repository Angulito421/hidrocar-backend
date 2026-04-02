"""
notifier.py
Envía un WhatsApp al asesor cuando un cliente pide hablar con humano.
"""

import os
import logging
from twilio.rest import Client

logger = logging.getLogger(__name__)

ASESOR_PHONE = "whatsapp:+51962691600"


def notificar_asesor(cliente_phone: str, ctx: dict, sandbox_number: str = None) -> bool:
    """
    Envía un WhatsApp al asesor con el resumen del cliente.
    - cliente_phone: número del cliente (ej: "whatsapp:+51900000000")
    - ctx: contexto con motor y ubicación
    - sandbox_number: número desde el que se envía (el To del webhook)
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token  = os.getenv("TWILIO_AUTH_TOKEN")

    # Usar el número que nos envió Twilio (el sandbox), o el del env como fallback
    from_number = sandbox_number or os.getenv("TWILIO_SANDBOX_NUMBER", "whatsapp:+14155238886")

    if not account_sid or not auth_token:
        logger.error("Faltan credenciales de Twilio para notificar al asesor")
        return False

    numero_limpio = cliente_phone.replace("whatsapp:", "")
    motor         = ctx.get("motor") or "no indicado"
    ubicacion     = ctx.get("ubicacion") or "no indicada"

    mensaje = (
        f"🔔 *Nuevo cliente interesado - Hidrocar*\n\n"
        f"📱 Número: *{numero_limpio}*\n"
        f"🔧 Motor: *{motor}*\n"
        f"📍 Ubicación: *{ubicacion}*\n\n"
        f"El cliente pidió hablar con un asesor. "
        f"Probablemente te escribirá pronto. 👆"
    )

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            from_=from_number,
            to=ASESOR_PHONE,
            body=mensaje,
        )
        logger.info(f"✅ Asesor notificado — cliente {numero_limpio}")
        return True
    except Exception as e:
        logger.error(f"❌ Error notificando asesor: {e}")
        return False