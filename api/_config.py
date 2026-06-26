"""Configuración central: lee variables de entorno."""
import os


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()


# Stripe
STRIPE_SECRET_KEY = _env("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = _env("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = _env("STRIPE_WEBHOOK_SECRET")
STRIPE_PRICE_ID = _env("STRIPE_PRICE_ID")

# n8n
N8N_BASE_URL = _env("N8N_BASE_URL").rstrip("/")
N8N_API_KEY = _env("N8N_API_KEY")
N8N_DEFAULT_WORKFLOW_ID = _env("N8N_DEFAULT_WORKFLOW_ID")

# YCloud (WhatsApp)
YCLOUD_API_KEY = _env("YCLOUD_API_KEY")
YCLOUD_FROM_NUMBER = _env("YCLOUD_FROM_NUMBER")
N8N_INBOUND_WEBHOOK_URL = _env("N8N_INBOUND_WEBHOOK_URL")

# Supabase
SUPABASE_URL = _env("SUPABASE_URL").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = _env("SUPABASE_SERVICE_ROLE_KEY")

# App
PUBLIC_BASE_URL = _env("PUBLIC_BASE_URL", "http://localhost:3000").rstrip("/")
