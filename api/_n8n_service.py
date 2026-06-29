"""Crea, lista, activa y desactiva los workflows de n8n que actúan como chatbots."""
import re
import uuid

import httpx

import _config as cfg


def _enabled() -> bool:
    return bool(cfg.N8N_BASE_URL and cfg.N8N_API_KEY)


def _headers() -> dict:
    return {"X-N8N-API-KEY": cfg.N8N_API_KEY, "Accept": "application/json"}


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:30] or "bot"


def _build_workflow(name: str, greeting: str, webhook_path: str) -> dict:
    """Genera un workflow Webhook -> Code (respuesta) -> HTTP Request (YCloud)."""
    safe_greeting = (greeting or "¡Hola! 👋 ¿En qué puedo ayudarte hoy?").replace("`", "'")
    code = (
        "const body = $input.first().json.body || $input.first().json;\n"
        "const msg = body.whatsappInboundMessage || body.message || {};\n"
        "const from = msg.from || body.from || '';\n"
        "const text = (msg.text && msg.text.body) || msg.text || body.text || '';\n"
        "const t = String(text).toLowerCase();\n"
        "let reply;\n"
        "if (t.includes('precio') || t.includes('plan')) {\n"
        "  reply = 'Tenemos varios planes desde $19/mes. ¿Te comparto el link de pago? 💳';\n"
        "} else {\n"
        f"  reply = {safe_greeting!r};\n"
        "}\n"
        "return [{ json: { from, text, reply } }];"
    )
    return {
        "name": name,
        "nodes": [
            {
                "parameters": {"httpMethod": "POST", "path": webhook_path, "options": {}},
                "name": "Entrada WhatsApp",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 300],
                "webhookId": webhook_path,
            },
            {
                "parameters": {"jsCode": code},
                "name": "Procesar mensaje",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [520, 300],
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "https://api.ycloud.com/v2/whatsapp/messages",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            {"name": "X-API-Key", "value": "={{ $env.YCLOUD_API_KEY }}"},
                            {"name": "Content-Type", "value": "application/json"},
                        ]
                    },
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": "={{ JSON.stringify({ from: $env.YCLOUD_FROM_NUMBER, to: $json.from, type: 'text', text: { body: $json.reply } }) }}",
                    "options": {},
                },
                "name": "Responder por YCloud",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.2,
                "position": [800, 300],
            },
        ],
        "connections": {
            "Entrada WhatsApp": {
                "main": [[{"node": "Procesar mensaje", "type": "main", "index": 0}]]
            },
            "Procesar mensaje": {
                "main": [[{"node": "Responder por YCloud", "type": "main", "index": 0}]]
            },
        },
        "settings": {"executionOrder": "v1"},
    }


async def create_bot(name: str, greeting: str = "") -> dict:
    """Crea un workflow nuevo en n8n y lo activa. Devuelve id y URL del webhook."""
    if not _enabled():
        raise RuntimeError("n8n no está configurado (N8N_BASE_URL / N8N_API_KEY).")
    path = f"wabu-{_slug(name)}-{uuid.uuid4().hex[:6]}"
    workflow = _build_workflow(name, greeting, path)
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{cfg.N8N_BASE_URL}/api/v1/workflows", headers=_headers(), json=workflow
        )
        resp.raise_for_status()
        created = resp.json()
        wid = created.get("id") or created.get("data", {}).get("id")
        # Activar el workflow recién creado.
        await client.post(
            f"{cfg.N8N_BASE_URL}/api/v1/workflows/{wid}/activate", headers=_headers()
        )
    return {
        "id": wid,
        "name": name,
        "webhook_path": path,
        "webhook_url": f"{cfg.N8N_BASE_URL}/webhook/{path}",
    }


async def list_bots() -> list[dict]:
    """Lista los workflows existentes en n8n."""
    if not _enabled():
        return []
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(
            f"{cfg.N8N_BASE_URL}/api/v1/workflows", headers=_headers()
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", data) if isinstance(data, dict) else data
        return [
            {"id": w.get("id"), "name": w.get("name"), "active": w.get("active")}
            for w in (items or [])
        ]


async def _toggle(workflow_id: str, action: str) -> bool:
    """action = 'activate' | 'deactivate'."""
    if not _enabled() or not workflow_id:
        return False
    url = f"{cfg.N8N_BASE_URL}/api/v1/workflows/{workflow_id}/{action}"
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(url, headers=_headers())
        resp.raise_for_status()
        return True


async def activate_bot(workflow_id: str | None = None) -> bool:
    return await _toggle(workflow_id or cfg.N8N_DEFAULT_WORKFLOW_ID, "activate")


async def deactivate_bot(workflow_id: str | None = None) -> bool:
    return await _toggle(workflow_id or cfg.N8N_DEFAULT_WORKFLOW_ID, "deactivate")
