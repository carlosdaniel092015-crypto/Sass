# 🚀 Guía de activación (Stripe · n8n · YCloud · Supabase)

La app ya está desplegada en Vercel. Para que **cobre de verdad**, conecta cada
servicio con sus variables de entorno en **Vercel → proyecto `sass` → Settings →
Environment Variables**, y luego haz **Redeploy**.

---

## 1) Stripe (cobro mensual)

1. Crea un **producto** con precio **recurrente mensual** (ej: $29 USD/mes).
   - Stripe Dashboard → *Products* → *Add product* → *Recurring* → *Monthly*.
   - Copia el **Price ID** (empieza con `price_...`).
2. Copia tu **Secret Key** (*Developers → API keys*, empieza con `sk_live_...` o `sk_test_...`).
3. Crea el **webhook**:
   - *Developers → Webhooks → Add endpoint*.
   - URL: `https://sass-zeta-gold.vercel.app/api/stripe/webhook`
   - Eventos: `checkout.session.completed`, `customer.subscription.updated`,
     `customer.subscription.deleted`, `invoice.paid`, `invoice.payment_failed`.
   - Copia el **Signing secret** (`whsec_...`).

**Variables a poner en Vercel:**
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PRICE_ID=price_...
STRIPE_WEBHOOK_SECRET=whsec_...
PUBLIC_BASE_URL=https://sass-zeta-gold.vercel.app
```

> 🔐 La Secret Key es sensible: ponla **solo** en Vercel (nunca en el código ni en Git).

---

## 2) n8n (el cerebro del bot)

1. Importa el workflow `n8n/wabu_whatsapp_bot.json` en tu n8n
   (*Workflows → Import from File*).
2. **Activa** el workflow y copia su **ID** (está en la URL del workflow).
3. Copia la URL del nodo *Webhook* (*Entrada WhatsApp*) — es tu `N8N_INBOUND_WEBHOOK_URL`.
4. Genera una **API Key** en *Settings → n8n API*.

**Variables en Vercel:**
```
N8N_BASE_URL=https://tu-n8n.com
N8N_API_KEY=...
N8N_DEFAULT_WORKFLOW_ID=<ID del workflow>
N8N_INBOUND_WEBHOOK_URL=https://tu-n8n.com/webhook/whatsapp-in
```

En tu n8n define también `YCLOUD_API_KEY` y `YCLOUD_FROM_NUMBER` como
*Environment Variables* para que el nodo de respuesta funcione.

---

## 3) YCloud (WhatsApp)

1. Obtén tu **API Key** y tu **número emisor** (formato E.164, ej: `+5215512345678`).
2. Configura el webhook entrante de YCloud hacia:
   `https://sass-zeta-gold.vercel.app/api/whatsapp/webhook`

**Variables en Vercel:**
```
YCLOUD_API_KEY=...
YCLOUD_FROM_NUMBER=+52...
```

---

## 4) Supabase (persistencia)

Ejecuta `supabase_schema.sql` en tu proyecto de Supabase (*SQL Editor*) y copia:
```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
```

---

## ✅ Verificar

Tras el redeploy, abre:
`https://sass-zeta-gold.vercel.app/health`

Debe mostrar `true` en cada servicio que hayas configurado:
```json
{"ok":true,"stripe":true,"n8n":true,"ycloud":true,"supabase":true}
```

### Probar el flujo de impago (modo test de Stripe)
Usa la tarjeta de Stripe que falla en renovación (`4000 0000 0000 0341`) o cancela
la suscripción desde el Dashboard: deberías ver el workflow de n8n pasar a
**inactivo** automáticamente.
