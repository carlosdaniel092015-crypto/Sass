"""Lógica de Stripe: checkout de suscripción y verificación de webhooks."""
import stripe

import _config as cfg

stripe.api_key = cfg.STRIPE_SECRET_KEY


def create_checkout_session(
    email: str, plan: str | None, workflow_id: str | None
) -> stripe.checkout.Session:
    """Crea una sesión de Checkout para la suscripción mensual del plan elegido."""
    price_id = cfg.price_for_plan(plan)
    meta = {
        "n8n_workflow_id": workflow_id or cfg.N8N_DEFAULT_WORKFLOW_ID,
        "plan": plan or "pro",
    }
    return stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        customer_email=email or None,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{cfg.PUBLIC_BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{cfg.PUBLIC_BASE_URL}/cancel",
        # metadata viaja a la suscripción para saber qué bot activar y qué plan es
        subscription_data={"metadata": meta},
        metadata=meta,
    )


def construct_event(payload: bytes, sig_header: str) -> stripe.Event:
    """Verifica la firma del webhook y devuelve el evento."""
    return stripe.Webhook.construct_event(
        payload, sig_header, cfg.STRIPE_WEBHOOK_SECRET
    )


# Estados de Stripe que mantienen el bot ACTIVO
ACTIVE_STATUSES = {"active", "trialing"}
