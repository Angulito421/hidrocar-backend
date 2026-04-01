"""
Router del webhook de Twilio.
Recibe mensajes de WhatsApp y responde usando la lógica del bot.
"""

import logging
from fastapi import APIRouter, Form, Request, Response
from twilio.twiml.messaging_response import MessagingResponse

from app.services.bot_logic import get_reply

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["Webhook"])


@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(default=""),
    From: str = Form(default=""),
    To: str = Form(default=""),
):
    """
    Endpoint POST que Twilio llama cada vez que llega un mensaje de WhatsApp.

    Parámetros clave enviados por Twilio:
    - Body: texto del mensaje del usuario
    - From: número del remitente (whatsapp:+51XXXXXXXXX)
    - To: número del sandbox de Twilio
    """
    logger.info(f"📩 Mensaje recibido de {From}: '{Body}'")

    # Obtener respuesta del motor de reglas
    reply_text = get_reply(Body)

    # Construir respuesta TwiML
    twiml = MessagingResponse()
    twiml.message(reply_text)

    logger.info(f"📤 Respondiendo: '{reply_text[:60]}...'")

    return Response(content=str(twiml), media_type="application/xml")