"""Lógica de Stripe: checkout de suscripción y verificación de webhooks."""
import stripe

import _config as cfg

stripe.api_key = cfg.STRIPE_SECRET_KEY


def create_checkout_session(email: str, workflow_id: str | None) -> stripe.checkout.Session:
    """Crea una sesión de Checkout para una suscripción mensual recurrente."""
    return stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        customer_email=email or None,
        line_items=[{"price": cfg.STRIPE_PRICE_ID, "quantity": 1}],
        success_url=f"{cfg.PUBLIC_BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{cfg.PUBLIC_BASE_URL}/cancel",
        # metadata viaja a la suscripción para saber qué bot activar
        subscription_data={
            "metadata": {"n8n_workflow_id": workflow_id or cfg.N8N_DEFAULT_WORKFLOW_ID}
        },
        metadata={"n8n_workflow_id": workflow_id or cfg.N8N_DEFAULT_WORKFLOW_ID},
    )


def construct_event(payload: bytes, sig_header: str) -> stripe.Event:
    """Verifica la firma del webhook y devuelve el evento."""
    return stripe.Webhook.construct_event(
        payload, sig_header, cfg.STRIPE_WEBHOOK_SECRET
    )


# Estados de Stripe que mantienen el bot ACTIVO
ACTIVE_STATUSES = {"active", "trialing"}
