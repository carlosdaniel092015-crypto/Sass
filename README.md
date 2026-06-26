# 🤖 ChatBot SaaS — Venta de chatbots de WhatsApp con cobro mensual

Plataforma en **Python (FastAPI)** lista para **Vercel** que te permite:

1. **Vender** un chatbot de WhatsApp desde una página con suscripción mensual.
2. **Cobrar** automáticamente cada mes con **Stripe** (tarjeta de crédito/débito).
3. **Activar** el bot (workflow de **n8n**) cuando el cliente paga.
4. **Desactivar el bot automáticamente** cuando un pago falla o el cliente cancela.
5. Conectar **WhatsApp vía YCloud** como canal de mensajería.

```
Cliente paga ──► Stripe ──► webhook ──► activa workflow n8n ──► bot vivo en WhatsApp (YCloud)
Pago falla   ──► Stripe ──► webhook ──► desactiva workflow n8n ──► bot apagado
```

---

## 🧱 Arquitectura

| Pieza        | Rol                                                              |
|--------------|-----------------------------------------------------------------|
| **FastAPI**  | Web + API (landing, checkout, webhooks). Corre en Vercel.       |
| **Stripe**   | Suscripción mensual y eventos de pago.                          |
| **n8n**      | "Cerebro" del bot. Se activa/desactiva vía su API REST.        |
| **YCloud**   | Envío/recepción de mensajes de WhatsApp.                        |
| **Supabase** | Guarda clientes, suscripciones y estado del bot.               |

### Archivos
```
api/
  index.py            # App FastAPI: landing, checkout, webhooks
  _config.py          # Lee variables de entorno
  _stripe_service.py  # Checkout + verificación de webhooks
  _n8n_service.py     # Activar / desactivar el workflow (bot)
  _ycloud_service.py  # WhatsApp: enviar y reenviar a n8n
  _storage.py         # Persistencia en Supabase (REST)
vercel.json           # Enruta todo a la app FastAPI
requirements.txt
supabase_schema.sql   # Tabla `subscriptions`
.env.example          # Variables necesarias
```

---

## 🔌 Endpoints

| Método | Ruta                       | Descripción                                   |
|--------|----------------------------|-----------------------------------------------|
| GET    | `/`                        | Página de venta con botón de suscripción.     |
| POST   | `/create-checkout-session` | Crea el pago mensual en Stripe.               |
| GET    | `/success` `/cancel`       | Páginas de retorno tras el pago.              |
| POST   | `/api/stripe/webhook`      | Stripe → activa/desactiva el bot.             |
| POST   | `/api/whatsapp/webhook`    | YCloud → reenvía mensajes entrantes a n8n.    |
| GET    | `/health`                  | Estado de configuración.                      |

---

## 🚀 Puesta en marcha

### 1. Stripe
- Crea un **producto** con precio **recurrente mensual** → copia el `price_id` en `STRIPE_PRICE_ID`.
- Crea un **webhook** apuntando a `https://TU-APP.vercel.app/api/stripe/webhook` y suscríbelo a:
  `checkout.session.completed`, `customer.subscription.updated`,
  `customer.subscription.deleted`, `invoice.paid`, `invoice.payment_failed`.
- Copia el **signing secret** en `STRIPE_WEBHOOK_SECRET`.

### 2. n8n
- Ten tu instancia n8n accesible (n8n Cloud o self-host).
- Genera una **API Key** en *Settings → n8n API* → `N8N_API_KEY`.
- Crea el workflow del bot, copia su **ID** → `N8N_DEFAULT_WORKFLOW_ID`.
- En ese workflow, un nodo **Webhook** recibe los mensajes; pon esa URL en `N8N_INBOUND_WEBHOOK_URL`.

### 3. YCloud (WhatsApp)
- Obtén tu **API Key** → `YCLOUD_API_KEY` y tu número emisor → `YCLOUD_FROM_NUMBER`.
- Configura el webhook de YCloud hacia `https://TU-APP.vercel.app/api/whatsapp/webhook`.

### 4. Supabase
- Crea un proyecto y ejecuta `supabase_schema.sql`.
- Copia `SUPABASE_URL` y la **service_role key** → `SUPABASE_SERVICE_ROLE_KEY`.

### 5. Desplegar en Vercel
1. Importa este repositorio en Vercel (o `vercel --prod` con la CLI).
2. Carga **todas** las variables de `.env.example` en *Project → Settings → Environment Variables*.
3. Pon `PUBLIC_BASE_URL` = la URL final de tu proyecto en Vercel.
4. Deploy. El runtime de Python detecta la app FastAPI automáticamente.

---

## 🧪 Probar en local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # rellena tus claves
uvicorn api.index:app --reload --port 3000
# Reenvía webhooks de Stripe en local:
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

---

## 💡 Cómo funciona la desactivación automática
Cuando Stripe no logra cobrar la mensualidad emite `invoice.payment_failed`.
El webhook llama a `n8n.deactivate_bot()` → el workflow queda **inactivo** y el bot
deja de responder en WhatsApp. Al regularizar el pago (`invoice.paid`) se reactiva solo.
Cada estado queda registrado en Supabase (`status`, `bot_active`).

> Nota: el cobro y la cancelación los gestiona Stripe; esta app sólo reacciona a sus
> eventos. Verifica siempre la firma del webhook (ya implementado) para seguridad.
