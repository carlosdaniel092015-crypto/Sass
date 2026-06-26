"""Persistencia de suscripciones en Supabase (vía REST).

Tabla `subscriptions` (ver supabase_schema.sql):
    email, stripe_customer_id, stripe_subscription_id,
    n8n_workflow_id, status, bot_active
"""
import httpx

import _config as cfg

TABLE = "subscriptions"


def _enabled() -> bool:
    return bool(cfg.SUPABASE_URL and cfg.SUPABASE_SERVICE_ROLE_KEY)


def _headers() -> dict:
    return {
        "apikey": cfg.SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {cfg.SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation,resolution=merge-duplicates",
    }


def _url() -> str:
    return f"{cfg.SUPABASE_URL}/rest/v1/{TABLE}"


async def upsert_subscription(record: dict) -> dict | None:
    """Inserta o actualiza por stripe_subscription_id (clave única)."""
    if not _enabled():
        return None
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            _url(),
            headers={**_headers(), "Prefer": "resolution=merge-duplicates,return=representation"},
            params={"on_conflict": "stripe_subscription_id"},
            json=record,
        )
        resp.raise_for_status()
        data = resp.json()
        return data[0] if data else None


async def get_by_subscription(subscription_id: str) -> dict | None:
    if not _enabled():
        return None
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(
            _url(),
            headers=_headers(),
            params={"stripe_subscription_id": f"eq.{subscription_id}", "limit": 1},
        )
        resp.raise_for_status()
        data = resp.json()
        return data[0] if data else None


async def get_by_customer(customer_id: str) -> dict | None:
    if not _enabled():
        return None
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(
            _url(),
            headers=_headers(),
            params={"stripe_customer_id": f"eq.{customer_id}", "limit": 1},
        )
        resp.raise_for_status()
        data = resp.json()
        return data[0] if data else None


async def set_status(subscription_id: str, status: str, bot_active: bool) -> None:
    if not _enabled():
        return
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.patch(
            _url(),
            headers=_headers(),
            params={"stripe_subscription_id": f"eq.{subscription_id}"},
            json={"status": status, "bot_active": bot_active},
        )
        resp.raise_for_status()
