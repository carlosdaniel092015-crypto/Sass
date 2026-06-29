"""
Plataforma SaaS para vender chatbots de WhatsApp (n8n + YCloud)
con cobro mensual por Stripe y desactivación automática del bot
cuando un cliente deja de pagar.

App ASGI (FastAPI) lista para Vercel (runtime Python).
"""
import os
import sys

# Asegura que los módulos hermanos (_config, _stripe_service, ...) sean
# importables tanto en local como en el runtime de Vercel.
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, Request, Response  # noqa: E402
from fastapi.responses import HTMLResponse, JSONResponse  # noqa: E402

import _auth as auth  # noqa: E402
import _config as cfg  # noqa: E402
import _n8n_service as n8n  # noqa: E402
import _pages as pages  # noqa: E402
import _storage as storage  # noqa: E402
import _stripe_service as stripe_service  # noqa: E402
import _ycloud_service as ycloud  # noqa: E402

app = FastAPI(title="ChatBot SaaS", docs_url=None, redoc_url=None)


# ----------------------------------------------------------------------
#  Landing / página de venta
# ----------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def landing() -> str:
    return pages.LANDING_HTML


@app.get("/health")
async def health() -> dict:
    return {
        "ok": True,
        "stripe": bool(cfg.STRIPE_SECRET_KEY),
        "n8n": bool(cfg.N8N_BASE_URL and cfg.N8N_API_KEY),
        "ycloud": bool(cfg.YCLOUD_API_KEY),
        "supabase": bool(cfg.SUPABASE_URL),
        "login": auth.enabled(),
    }


# ----------------------------------------------------------------------
#  Panel de administración (crear/listar bots en n8n)
# ----------------------------------------------------------------------
def _is_admin(request: Request) -> bool:
    # 1) Sesión de login (cookie firmada)
    if auth.verify_session(request.cookies.get(auth.COOKIE_NAME, "")):
        return True
    # 2) Token de API (compatibilidad / uso programático)
    token = request.headers.get("x-admin-token") or request.headers.get(
        "authorization", ""
    ).removeprefix("Bearer ").strip()
    return bool(cfg.ADMIN_TOKEN) and token == cfg.ADMIN_TOKEN


@app.get("/login", response_class=HTMLResponse)
async def login_page() -> str:
    return pages.LOGIN_HTML


@app.post("/api/login")
async def api_login(request: Request) -> JSONResponse:
    if not auth.enabled():
        return JSONResponse(
            {"error": "El login no está configurado (define ADMIN_EMAIL y ADMIN_PASSWORD)."},
            status_code=503,
        )
    body = await request.json() or {}
    if not auth.check_credentials(body.get("email", ""), body.get("password", "")):
        return JSONResponse({"error": "Credenciales incorrectas"}, status_code=401)
    resp = JSONResponse({"ok": True})
    resp.set_cookie(
        auth.COOKIE_NAME,
        auth.make_session(body.get("email", "")),
        max_age=auth.DEFAULT_TTL,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return resp


@app.post("/api/logout")
async def api_logout() -> JSONResponse:
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(auth.COOKIE_NAME, path="/")
    return resp


@app.get("/api/me")
async def api_me(request: Request) -> JSONResponse:
    if not _is_admin(request):
        return JSONResponse({"error": "no autorizado"}, status_code=401)
    email = auth.verify_session(request.cookies.get(auth.COOKIE_NAME, ""))
    return JSONResponse({"ok": True, "email": email})


@app.get("/panel", response_class=HTMLResponse)
async def panel() -> str:
    return pages.PANEL_HTML


@app.get("/api/bots")
async def api_list_bots(request: Request) -> JSONResponse:
    if not _is_admin(request):
        return JSONResponse({"error": "no autorizado"}, status_code=401)
    try:
        return JSONResponse({"bots": await n8n.list_bots()})
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"error": str(exc)}, status_code=502)


@app.post("/api/bots/create")
async def api_create_bot(request: Request) -> JSONResponse:
    if not _is_admin(request):
        return JSONResponse({"error": "no autorizado"}, status_code=401)
    body = await request.json()
    name = (body or {}).get("name", "").strip()
    greeting = (body or {}).get("greeting", "").strip()
    if not name:
        return JSONResponse({"error": "Falta el nombre del bot"}, status_code=400)
    try:
        return JSONResponse(await n8n.create_bot(name, greeting))
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"error": str(exc)}, status_code=502)


# ----------------------------------------------------------------------
#  Onboarding de WhatsApp (Embedded Signup de Meta / YCloud)
# ----------------------------------------------------------------------
@app.get("/api/whatsapp/config")
async def whatsapp_config(request: Request) -> JSONResponse:
    """Expone al frontend los datos públicos del Embedded Signup."""
    if not _is_admin(request):
        return JSONResponse({"error": "no autorizado"}, status_code=401)
    return JSONResponse(
        {
            "app_id": cfg.META_APP_ID,
            "graph_version": cfg.META_GRAPH_VERSION,
            "config_id_signup": cfg.META_CONFIG_ID_SIGNUP,
            "config_id_coexistence": cfg.META_CONFIG_ID_COEXISTENCE,
            "ready": bool(cfg.META_APP_ID and cfg.META_CONFIG_ID_SIGNUP),
        }
    )


@app.post("/api/whatsapp/onboard")
async def whatsapp_onboard(request: Request) -> JSONResponse:
    """Recibe el resultado del Embedded Signup y lo registra en YCloud."""
    if not _is_admin(request):
        return JSONResponse({"error": "no autorizado"}, status_code=401)
    body = await request.json() or {}
    code = body.get("code", "")
    waba_id = body.get("waba_id", "")
    phone_number_id = body.get("phone_number_id", "")
    kind = body.get("kind", "signup")
    if not (waba_id or phone_number_id or code):
        return JSONResponse({"error": "Faltan datos del Embedded Signup"}, status_code=400)
    try:
        result = await ycloud.register_waba(code, waba_id, phone_number_id, kind)
        return JSONResponse({"ok": True, **result})
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"error": str(exc)}, status_code=502)


# ----------------------------------------------------------------------
#  Checkout (suscripción mensual)
# ----------------------------------------------------------------------
@app.post("/create-checkout-session")
async def create_checkout_session(request: Request) -> JSONResponse:
    if not cfg.STRIPE_SECRET_KEY or not cfg.STRIPE_PRICE_ID:
        return JSONResponse(
            {"error": "El pago aún no está activo. Estamos terminando de configurarlo, "
                      "escríbenos para activar tu bot. ✅"},
            status_code=503,
        )
    body = await request.json()
    email = (body or {}).get("email", "")
    plan = (body or {}).get("plan", "pro")
    workflow_id = (body or {}).get("workflow_id")
    if not cfg.price_for_plan(plan):
        return JSONResponse(
            {"error": "Ese plan aún no está disponible. Prueba otro o escríbenos. ✅"},
            status_code=503,
        )
    try:
        session = stripe_service.create_checkout_session(email, plan, workflow_id)
        return JSONResponse({"url": session.url})
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"error": str(exc)}, status_code=400)


@app.get("/success", response_class=HTMLResponse)
async def success() -> str:
    return pages.status_page(
        "🎉", "¡Pago confirmado!",
        "Tu bot de WhatsApp se está activando. Recibirás un mensaje de bienvenida en breve.",
    )


@app.get("/cancel", response_class=HTMLResponse)
async def cancel() -> str:
    return pages.status_page(
        "🛑", "Pago cancelado",
        "No se realizó ningún cargo. Puedes intentarlo de nuevo cuando quieras.",
    )


# ----------------------------------------------------------------------
#  Webhook de Stripe  →  activa / desactiva el bot
# ----------------------------------------------------------------------
@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request) -> Response:
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe_service.construct_event(payload, sig)
    except Exception as exc:  # noqa: BLE001 — firma inválida
        return JSONResponse({"error": f"firma inválida: {exc}"}, status_code=400)

    etype = event["type"]
    obj = event["data"]["object"]

    # 1) Suscripción creada/pagada -> ACTIVAR bot
    if etype == "checkout.session.completed":
        await _on_checkout_completed(obj)

    elif etype in ("customer.subscription.created", "customer.subscription.updated"):
        await _sync_subscription(obj)

    # 2) Pago fallido o suscripción cancelada -> DESACTIVAR bot
    elif etype == "invoice.payment_failed":
        await _on_payment_failed(obj)

    elif etype == "customer.subscription.deleted":
        await _deactivate(obj.get("id"), obj.get("metadata", {}).get("n8n_workflow_id"),
                          status="canceled")

    # 3) Pago recurrente exitoso -> reactivar por si estaba suspendido
    elif etype == "invoice.paid":
        await _on_invoice_paid(obj)

    return JSONResponse({"received": True})


async def _on_checkout_completed(session: dict) -> None:
    workflow_id = (session.get("metadata") or {}).get("n8n_workflow_id") or cfg.N8N_DEFAULT_WORKFLOW_ID
    record = {
        "email": session.get("customer_details", {}).get("email") or session.get("customer_email"),
        "stripe_customer_id": session.get("customer"),
        "stripe_subscription_id": session.get("subscription"),
        "n8n_workflow_id": workflow_id,
        "status": "active",
        "bot_active": True,
    }
    await storage.upsert_subscription(record)
    await n8n.activate_bot(workflow_id)
    # (Opcional) enviar mensaje de bienvenida por WhatsApp requiere el número del cliente.


async def _sync_subscription(sub: dict) -> None:
    workflow_id = (sub.get("metadata") or {}).get("n8n_workflow_id") or cfg.N8N_DEFAULT_WORKFLOW_ID
    status = sub.get("status", "")
    active = status in stripe_service.ACTIVE_STATUSES
    await storage.upsert_subscription({
        "stripe_customer_id": sub.get("customer"),
        "stripe_subscription_id": sub.get("id"),
        "n8n_workflow_id": workflow_id,
        "status": status,
        "bot_active": active,
    })
    if active:
        await n8n.activate_bot(workflow_id)
    else:
        await n8n.deactivate_bot(workflow_id)


async def _on_payment_failed(invoice: dict) -> None:
    sub_id = invoice.get("subscription")
    record = await storage.get_by_subscription(sub_id) if sub_id else None
    workflow_id = (record or {}).get("n8n_workflow_id")
    await _deactivate(sub_id, workflow_id, status="past_due")
    # Aviso al cliente por WhatsApp si tenemos su número
    phone = (record or {}).get("whatsapp")
    if phone:
        await ycloud.send_text(
            phone,
            "⚠️ Tu pago no se procesó y tu bot quedó suspendido. "
            "Actualiza tu método de pago para reactivarlo.",
        )


async def _on_invoice_paid(invoice: dict) -> None:
    sub_id = invoice.get("subscription")
    if not sub_id:
        return
    record = await storage.get_by_subscription(sub_id)
    workflow_id = (record or {}).get("n8n_workflow_id") or cfg.N8N_DEFAULT_WORKFLOW_ID
    await storage.set_status(sub_id, "active", True)
    await n8n.activate_bot(workflow_id)


async def _deactivate(sub_id: str | None, workflow_id: str | None, status: str) -> None:
    if sub_id:
        await storage.set_status(sub_id, status, False)
    await n8n.deactivate_bot(workflow_id)


# ----------------------------------------------------------------------
#  Webhook de WhatsApp (YCloud)  →  reenvía al cerebro n8n
# ----------------------------------------------------------------------
@app.post("/api/whatsapp/webhook")
async def whatsapp_webhook(request: Request) -> JSONResponse:
    payload = await request.json()
    await ycloud.forward_to_n8n(payload)
    return JSONResponse({"received": True})
