"""
extractor.py
Extrae datos clave del mensaje del usuario: cilindraje y ubicación.
Se ejecuta en cada mensaje ANTES de decidir la respuesta.
"""

import re


# Distritos y ciudades de Perú más comunes que puede mencionar un cliente
LUGARES_PERU = [
    "lima", "miraflores", "san isidro", "surco", "barranco", "chorrillos",
    "la molina", "ate", "santa anita", "san juan de lurigancho", "lurigancho",
    "san martin de porres", "los olivos", "independencia", "comas", "carabayllo",
    "puente piedra", "ventanilla", "callao", "bellavista", "la perla",
    "arequipa", "trujillo", "cusco", "piura", "chiclayo", "iquitos",
    "huancayo", "tacna", "pucallpa", "chimbote", "ica", "sullana",
    "provincias", "provincia", "fuera de lima", "interior del pais",
    "interior del país", "regiones", "region", "región",
]


def extraer_cilindraje(text: str) -> str | None:
    """Detecta cilindraje en el texto. Retorna string limpio o None."""
    patron = r"\b(\d{3,4})\s*(cc)?\b"
    match = re.search(patron, text, re.IGNORECASE)
    if match:
        numero = int(match.group(1))
        if 500 <= numero <= 9000:  # rango razonable de cc
            return f"{numero}cc"
    # Formato 2.0L / 1.6L
    patron_l = r"\b(\d\.\d)\s*l(itros)?\b"
    match_l = re.search(patron_l, text, re.IGNORECASE)
    if match_l:
        return f"{match_l.group(1)}L"
    return None


def extraer_ubicacion(text: str) -> str | None:
    """Detecta si el usuario menciona su ubicación."""
    text_lower = text.lower()
    for lugar in LUGARES_PERU:
        if lugar in text_lower:
            # Capitalizar
            return lugar.title()
    return None


def esta_en_lima(ubicacion: str | None) -> bool:
    """Determina si la ubicación guardada es Lima o alrededores."""
    if not ubicacion:
        return False
    lima_keywords = [
        "lima", "miraflores", "surco", "barranco", "chorrillos", "la molina",
        "ate", "santa anita", "lurigancho", "san martin", "los olivos",
        "independencia", "comas", "carabayllo", "puente piedra",
        "ventanilla", "callao", "bellavista", "la perla", "san isidro",
        "san juan",
    ]
    ub = ubicacion.lower()
    return any(k in ub for k in lima_keywords)