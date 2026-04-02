"""
webhook.py
Endpoint POST /webhook — recibe mensajes de Twilio y responde TwiML.
Orquesta: extracción de contexto → lógica del bot → notificación si aplica → respuesta.
"""

import logging
from fastapi import APIRouter, Form, Response
from twilio.twiml.messaging_response import MessagingResponse

from app.services.bot_logic import get_reply, es_derivacion_humano
from app.services.context_store import (
    get_context, update_context, add_to_history, context_tag
)
from app.services.extractor import extraer_cilindraje, extraer_ubicacion
from app.services.notifier import notificar_asesor

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Webhook"])


@router.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(default=""),
    From: str = Form(default=""),
    To: str = Form(default=""),
):
    phone   = From   # "whatsapp:+51900000000"
    sandbox = To     # número del sandbox de Twilio
    message = Body.strip()

    logger.info(f"📩 [{phone}] '{message}'")

    # 1. Extraer datos del mensaje y actualizar contexto
    cilindraje = extraer_cilindraje(message)
    ubicacion  = extraer_ubicacion(message)
    update_context(phone, motor=cilindraje, ubicacion=ubicacion)
    add_to_history(phone, message)

    # 2. Contexto actual
    ctx = get_context(phone)
    enriched_message = f"{message} {context_tag(phone)}"

    # 3. Obtener respuesta del bot
    reply_text = get_reply(enriched_message, ctx)

    # 4. Si el bot derivó a asesor humano → notificar por WhatsApp
    if es_derivacion_humano(enriched_message):
        notificar_asesor(
            cliente_phone=phone,
            ctx=ctx,
            sandbox_number=sandbox,
        )

    logger.info(f"📤 [{phone}] '{reply_text[:60]}...'")

    # 5. Responder al cliente
    twiml = MessagingResponse()
    twiml.message(reply_text)
    return Response(content=str(twiml), media_type="application/xml")