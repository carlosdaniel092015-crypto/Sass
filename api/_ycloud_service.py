"""Integración WhatsApp vía YCloud.

- Envía mensajes salientes (avisos de pago, bienvenida, etc.).
- Reenvía mensajes entrantes al webhook de n8n (cerebro del bot).
Docs: https://docs.ycloud.com/
"""
import httpx

import _config as cfg

YCLOUD_API = "https://api.ycloud.com/v2/whatsapp/messages"


def _enabled() -> bool:
    return bool(cfg.YCLOUD_API_KEY and cfg.YCLOUD_FROM_NUMBER)


def _headers() -> dict:
    return {"X-API-Key": cfg.YCLOUD_API_KEY, "Content-Type": "application/json"}


async def send_text(to_number: str, text: str) -> dict | None:
    """Envía un mensaje de texto de WhatsApp por YCloud."""
    if not _enabled():
        return None
    payload = {
        "from": cfg.YCLOUD_FROM_NUMBER,
        "to": to_number,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(YCLOUD_API, headers=_headers(), json=payload)
        resp.raise_for_status()
        return resp.json()


async def forward_to_n8n(payload: dict) -> bool:
    """Reenvía el evento entrante de WhatsApp al webhook de n8n."""
    if not cfg.N8N_INBOUND_WEBHOOK_URL:
        return False
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(cfg.N8N_INBOUND_WEBHOOK_URL, json=payload)
        resp.raise_for_status()
        return True
