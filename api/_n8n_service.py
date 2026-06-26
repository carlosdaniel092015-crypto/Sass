"""Activa / desactiva el workflow de n8n que actúa como chatbot."""
import httpx

import _config as cfg


def _enabled() -> bool:
    return bool(cfg.N8N_BASE_URL and cfg.N8N_API_KEY)


def _headers() -> dict:
    return {"X-N8N-API-KEY": cfg.N8N_API_KEY, "Accept": "application/json"}


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
