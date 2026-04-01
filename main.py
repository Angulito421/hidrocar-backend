from fastapi import FastAPI
from app.routers import webhook

app = FastAPI(
    title="Hidrocar WhatsApp Bot",
    description="Chatbot de WhatsApp para Hidrocar vía Twilio",
    version="1.0.0",
)

app.include_router(webhook.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Hidrocar Bot 🚗💧"}