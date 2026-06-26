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

import _config as cfg  # noqa: E402
import _n8n_service as n8n  # noqa: E402
import _storage as storage  # noqa: E402
import _stripe_service as stripe_service  # noqa: E402
import _ycloud_service as ycloud  # noqa: E402

app = FastAPI(title="ChatBot SaaS", docs_url=None, redoc_url=None)


# ----------------------------------------------------------------------
#  Landing / página de venta
# ----------------------------------------------------------------------
LANDING_HTML = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bots de WhatsApp con IA — Suscripción mensual</title>
  <style>
    :root {{ --brand:#25D366; --dark:#075E54; }}
    * {{ box-sizing:border-box; font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; }}
    body {{ margin:0; background:#0b141a; color:#e9edef; }}
    .wrap {{ max-width:880px; margin:0 auto; padding:64px 24px; }}
    h1 {{ font-size:42px; line-height:1.1; margin:0 0 16px; }}
    .lead {{ font-size:19px; color:#a8b4ba; max-width:620px; }}
    .card {{ background:#111b21; border:1px solid #2a3942; border-radius:16px;
             padding:32px; margin-top:40px; }}
    .price {{ font-size:48px; font-weight:700; }}
    .price span {{ font-size:18px; color:#a8b4ba; font-weight:400; }}
    ul {{ list-style:none; padding:0; margin:24px 0; }}
    li {{ padding:8px 0; padding-left:28px; position:relative; }}
    li:before {{ content:"✓"; color:var(--brand); position:absolute; left:0; font-weight:700; }}
    .btn {{ display:inline-block; background:var(--brand); color:#04130b; font-weight:700;
            border:none; padding:16px 28px; font-size:17px; border-radius:10px;
            cursor:pointer; text-decoration:none; width:100%; }}
    .btn:hover {{ opacity:.9; }}
    input {{ width:100%; padding:14px; border-radius:10px; border:1px solid #2a3942;
             background:#0b141a; color:#e9edef; font-size:16px; margin-bottom:14px; }}
    .muted {{ color:#667781; font-size:13px; margin-top:14px; text-align:center; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Chatbots de WhatsApp con IA para tu negocio</h1>
    <p class="lead">Automatiza ventas y atención al cliente 24/7 con un bot
       conectado a WhatsApp. Sin instalar nada. Lo activamos por ti.</p>

    <div class="card">
      <div class="price">$29<span> USD / mes</span></div>
      <ul>
        <li>Bot de WhatsApp ilimitado (motor n8n)</li>
        <li>Integración oficial con YCloud</li>
        <li>Respuestas automáticas con IA</li>
        <li>Se desactiva solo si cancelas — sin ataduras</li>
      </ul>
      <form id="f">
        <input type="email" id="email" placeholder="tu@correo.com" required>
        <button class="btn" type="submit">Suscribirme y activar mi bot</button>
      </form>
      <p class="muted">Pago seguro con Stripe · Tarjeta de crédito o débito</p>
    </div>
  </div>

  <script>
    document.getElementById('f').addEventListener('submit', async (e) => {{
      e.preventDefault();
      const email = document.getElementById('email').value;
      const res = await fetch('/create-checkout-session', {{
        method:'POST',
        headers:{{'Content-Type':'application/json'}},
        body: JSON.stringify({{ email }})
      }});
      const data = await res.json();
      if (data.url) {{ window.location = data.url; }}
      else {{ alert(data.error || 'Error al crear la sesión de pago'); }}
    }});
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def landing() -> str:
    return LANDING_HTML


@app.get("/health")
async def health() -> dict:
    return {
        "ok": True,
        "stripe": bool(cfg.STRIPE_SECRET_KEY),
        "n8n": bool(cfg.N8N_BASE_URL and cfg.N8N_API_KEY),
        "ycloud": bool(cfg.YCLOUD_API_KEY),
        "supabase": bool(cfg.SUPABASE_URL),
    }


# ----------------------------------------------------------------------
#  Checkout (suscripción mensual)
# ----------------------------------------------------------------------
@app.post("/create-checkout-session")
async def create_checkout_session(request: Request) -> JSONResponse:
    if not cfg.STRIPE_SECRET_KEY or not cfg.STRIPE_PRICE_ID:
        return JSONResponse({"error": "Stripe no está configurado."}, status_code=500)
    body = await request.json()
    email = (body or {}).get("email", "")
    workflow_id = (body or {}).get("workflow_id")
    try:
        session = stripe_service.create_checkout_session(email, workflow_id)
        return JSONResponse({"url": session.url})
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"error": str(exc)}, status_code=400)


@app.get("/success", response_class=HTMLResponse)
async def success() -> str:
    return _msg("✅ ¡Pago confirmado!", "Tu bot de WhatsApp se está activando. "
                "Recibirás un mensaje de bienvenida en breve.")


@app.get("/cancel", response_class=HTMLResponse)
async def cancel() -> str:
    return _msg("Pago cancelado", "No se realizó ningún cargo. Puedes intentarlo de nuevo cuando quieras.")


def _msg(title: str, text: str) -> str:
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>body{{background:#0b141a;color:#e9edef;font-family:sans-serif;
    display:flex;height:100vh;align-items:center;justify-content:center;margin:0;text-align:center}}
    div{{max-width:440px;padding:24px}}h1{{color:#25D366}}a{{color:#25D366}}</style></head>
    <body><div><h1>{title}</h1><p>{text}</p><p><a href="/">← Volver</a></p></div></body></html>"""


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
