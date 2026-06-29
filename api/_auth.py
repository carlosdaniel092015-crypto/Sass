"""Login de dueño (Fase 1) — sesión firmada con HMAC, sin base de datos.

Las credenciales viven en variables de entorno (ADMIN_EMAIL / ADMIN_PASSWORD).
Al iniciar sesión se emite un token firmado que se guarda en una cookie httpOnly.
"""
import base64
import hashlib
import hmac
import json
import time

import _config as cfg

COOKIE_NAME = "wabu_session"
DEFAULT_TTL = 7 * 24 * 3600  # 7 días


def enabled() -> bool:
    return bool(cfg.ADMIN_EMAIL and cfg.ADMIN_PASSWORD)


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _sign(raw: str) -> str:
    secret = cfg.SESSION_SECRET.encode()
    return _b64(hmac.new(secret, raw.encode(), hashlib.sha256).digest())


def make_session(email: str, ttl: int = DEFAULT_TTL) -> str:
    payload = {"email": email, "exp": int(time.time()) + ttl}
    raw = _b64(json.dumps(payload).encode())
    return f"{raw}.{_sign(raw)}"


def verify_session(token: str) -> str | None:
    if not token or "." not in token:
        return None
    raw, sig = token.rsplit(".", 1)
    if not hmac.compare_digest(sig, _sign(raw)):
        return None
    try:
        payload = json.loads(_unb64(raw))
    except Exception:  # noqa: BLE001
        return None
    if int(payload.get("exp", 0)) < time.time():
        return None
    return payload.get("email")


def check_credentials(email: str, password: str) -> bool:
    if not enabled():
        return False
    email_ok = hmac.compare_digest(
        (email or "").strip().lower(), cfg.ADMIN_EMAIL.strip().lower()
    )
    pass_ok = hmac.compare_digest(password or "", cfg.ADMIN_PASSWORD)
    return email_ok and pass_ok
