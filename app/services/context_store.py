"""
context_store.py
Memoria RAM por número de WhatsApp.
Guarda: motor (cc), ubicacion, y los últimos 2 mensajes del usuario.
Se reinicia si el servidor se cae — suficiente para pruebas y MVP.
"""

from typing import Optional

# { "whatsapp:+51900000000": { "motor": "1600", "ubicacion": "Lima, Chorrillos", "history": [...] } }
_store: dict[str, dict] = {}


def get_context(phone: str) -> dict:
    if phone not in _store:
        _store[phone] = {"motor": None, "ubicacion": None, "history": []}
    return _store[phone]


def update_context(phone: str, motor: Optional[str] = None, ubicacion: Optional[str] = None) -> None:
    ctx = get_context(phone)
    if motor:
        ctx["motor"] = motor
    if ubicacion:
        ctx["ubicacion"] = ubicacion


def add_to_history(phone: str, message: str) -> None:
    ctx = get_context(phone)
    ctx["history"].append(message)
    ctx["history"] = ctx["history"][-2:]  # solo últimos 2 mensajes


def context_tag(phone: str) -> str:
    """
    Genera el tag de contexto que se añade al mensaje del usuario.
    Ejemplo: "[motor: 1600cc | ubicacion: Lima, Chorrillos]"
    """
    ctx = get_context(phone)
    motor = ctx["motor"] or "NA"
    ubicacion = ctx["ubicacion"] or "NA"
    return f"[motor: {motor} | ubicacion: {ubicacion}]"