# 🔗 Cómo activar "Conectar WhatsApp" (Embedded Signup)

El panel muestra `⚠️ Falta configurar Meta` hasta que definas las variables del
Embedded Signup. Hay **dos formas** de onboardear el WhatsApp de tus clientes.
Elige según qué tan rápido quieras lanzar.

---

## ✅ Opción 1 — Onboarding por la consola de YCloud (rápido, sin Meta App)

La más sencilla para empezar. **No** usas el Embedded Signup de tu página.

1. Entra a YCloud → **WhatsApp accounts** → *Get started*.
2. Conecta el número del cliente (WhatsApp Business API o Coexistence) dentro de YCloud.
3. YCloud te entrega, por cada cuenta:
   - una **API Key**
   - el **número emisor** (E.164)
4. Pega en Vercel:
   ```
   YCLOUD_API_KEY=...
   YCLOUD_FROM_NUMBER=+52...
   ```
5. Crea el bot en tu panel (`/panel` → Crear bot) y pon su webhook en YCloud.

➡️ Con esto el bot ya funciona. Las tarjetas "Comenzar" del panel son opcionales.

---

## 🏗️ Opción 2 — Embedded Signup dentro de tu propia página

Es lo que activa los botones **Comenzar** del panel. Requiere una **App de Meta**
configurada como Tech Provider (o que YCloud te dé sus credenciales de partner).

### A) Pregunta primero a YCloud
Como tu BSP es YCloud, lo correcto es preguntarles:
> "¿Ofrecen Embedded Signup para partners/ISV? ¿Me dan un `config_id` y `App ID`
> para incrustar el onboarding en mi propia plataforma, y a qué endpoint envío el
> `code`?"

Si te dan esos datos → pégalos directo (ve al paso D) y listo.

### B) Si vas con tu propia App de Meta (ser tú el Tech Provider)
1. Ve a https://developers.facebook.com/apps → **Create App** → tipo **Business**.
   - El **App ID** aparece en el panel → es tu `META_APP_ID`.
2. Agrega los productos:
   - **WhatsApp**
   - **Facebook Login for Business**
3. Verifica tu **Meta Business** (Business Verification) y acepta los
   **términos de Tech Provider**.

### C) Crea las "Login configurations" (de aquí salen los config_id)
En *Facebook Login for Business → Configurations → Create configuration*:
1. Configuración para **crear WABA / número nuevo**:
   - Tipo de acceso: WhatsApp Embedded Signup.
   - Guarda → copia su **Configuration ID** → `META_CONFIG_ID_SIGNUP`.
2. Configuración para **Coexistence** (segunda config con el feature de
   *WhatsApp Business App onboarding*):
   - Copia su Configuration ID → `META_CONFIG_ID_COEXISTENCE`.

### D) App Review (para usarlo con clientes reales)
Solicita **Advanced Access** a:
- `whatsapp_business_management`
- `whatsapp_business_messaging`

(Mientras esté en modo desarrollo, solo funciona con tus propios usuarios de prueba.)

### E) Variables en Vercel (Settings → Environment Variables) y Redeploy
```
META_APP_ID=...
META_GRAPH_VERSION=v21.0
META_CONFIG_ID_SIGNUP=...
META_CONFIG_ID_COEXISTENCE=...
# Endpoint de YCloud que recibe el `code` para finalizar el alta (te lo da YCloud):
YCLOUD_ONBOARD_ENDPOINT=...
```

### F) Verifica
- `https://<tu-dominio>/health` debe mostrar que Meta está configurado.
- En `/panel`, el aviso amarillo desaparece y los botones **Comenzar** abren el popup de Meta.

---

## 🧭 ¿Cuál elijo?

| | Opción 1 (YCloud console) | Opción 2 (Embedded Signup propio) |
|---|---|---|
| Velocidad | Hoy mismo | Semanas (App Review) |
| Requisitos | Cuenta YCloud | Meta App + verificación + review |
| Experiencia | Onboarding en YCloud | Todo dentro de tu marca |
| Recomendado para | Lanzar y validar ya | Cuando tengas volumen / quieras white-label total |

**Sugerencia:** empieza con la **Opción 1** para tener clientes funcionando, y migra a la
**Opción 2** cuando YCloud te habilite el partner o completes tu App Review.
