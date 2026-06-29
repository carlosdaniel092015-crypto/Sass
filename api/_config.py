"""Configuración central: lee variables de entorno."""
import os


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()


# Stripe
STRIPE_SECRET_KEY = _env("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = _env("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = _env("STRIPE_WEBHOOK_SECRET")

# Planes: un Price ID (recurrente mensual) por plan.
# STRIPE_PRICE_ID se mantiene por compatibilidad y como fallback del plan Pro.
STRIPE_PRICE_ID = _env("STRIPE_PRICE_ID")
STRIPE_PRICE_STARTER = _env("STRIPE_PRICE_STARTER")
STRIPE_PRICE_PRO = _env("STRIPE_PRICE_PRO") or STRIPE_PRICE_ID
STRIPE_PRICE_BUSINESS = _env("STRIPE_PRICE_BUSINESS")

# Mapa plan -> Price ID. Lo usa el checkout para cobrar el plan elegido.
PRICE_BY_PLAN = {
    "starter": STRIPE_PRICE_STARTER,
    "pro": STRIPE_PRICE_PRO,
    "business": STRIPE_PRICE_BUSINESS,
}


def price_for_plan(plan: str) -> str:
    """Devuelve el Price ID del plan (cae a Pro si el plan no existe/está vacío)."""
    return PRICE_BY_PLAN.get(plan or "pro") or STRIPE_PRICE_PRO

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

# Token para proteger el panel de administración (/panel) y sus endpoints.
ADMIN_TOKEN = _env("ADMIN_TOKEN")
