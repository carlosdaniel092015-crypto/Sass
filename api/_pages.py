"""Páginas HTML del producto (landing, success, cancel).

Se guardan como strings planos y se devuelven tal cual (sin .format ni
f-strings), por eso las llaves de CSS/JS van SIN escapar.
"""

_HEAD = """
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg:#070b16; --bg2:#0c1222; --panel:#111a2e; --line:#1f2a44;
      --txt:#e8ecf5; --muted:#94a3c4; --brand:#22c55e; --brand2:#14b8a6;
      --accent:#6366f1;
    }
    *{box-sizing:border-box;margin:0;padding:0}
    html{scroll-behavior:smooth}
    body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--txt);
      line-height:1.5;-webkit-font-smoothing:antialiased;overflow-x:hidden}
    a{color:inherit;text-decoration:none}
    .container{max-width:1140px;margin:0 auto;padding:0 24px}
    .grad-text{background:linear-gradient(120deg,#34d399,#22d3ee 60%,#818cf8);
      -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
    .btn{display:inline-flex;align-items:center;gap:8px;justify-content:center;
      font-weight:700;font-size:15px;padding:13px 22px;border-radius:12px;border:0;
      cursor:pointer;transition:.2s;font-family:inherit}
    .btn-primary{background:linear-gradient(120deg,var(--brand),var(--brand2));color:#03130b;
      box-shadow:0 8px 24px -8px rgba(34,197,94,.6)}
    .btn-primary:hover{transform:translateY(-2px);box-shadow:0 12px 30px -8px rgba(34,197,94,.7)}
    .btn-ghost{background:rgba(255,255,255,.05);color:var(--txt);border:1px solid var(--line)}
    .btn-ghost:hover{background:rgba(255,255,255,.1)}

    /* NAV */
    nav{position:sticky;top:0;z-index:50;backdrop-filter:blur(14px);
      background:rgba(7,11,22,.72);border-bottom:1px solid var(--line)}
    .nav-in{display:flex;align-items:center;justify-content:space-between;height:68px}
    .logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:19px}
    .logo .dot{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;
      background:linear-gradient(120deg,var(--brand),var(--brand2));font-size:18px}
    .nav-links{display:flex;gap:30px;align-items:center}
    .nav-links a{color:var(--muted);font-weight:500;font-size:15px}
    .nav-links a:hover{color:var(--txt)}
    @media(max-width:820px){.nav-links{display:none}}

    /* HERO */
    .hero{position:relative;padding:90px 0 60px;overflow:hidden}
    .glow{position:absolute;border-radius:50%;filter:blur(120px);opacity:.5;z-index:-1}
    .glow.a{width:560px;height:560px;background:#16a34a;top:-180px;left:-120px}
    .glow.b{width:480px;height:480px;background:#6366f1;top:-80px;right:-140px}
    .hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
    @media(max-width:900px){.hero-grid{grid-template-columns:1fr;text-align:center}}
    .badge{display:inline-flex;align-items:center;gap:8px;background:rgba(34,197,94,.1);
      border:1px solid rgba(34,197,94,.3);color:#86efac;padding:7px 14px;border-radius:999px;
      font-size:13px;font-weight:600;margin-bottom:22px}
    h1{font-size:clamp(34px,5vw,58px);line-height:1.05;font-weight:900;letter-spacing:-1.5px}
    .hero p.lead{color:var(--muted);font-size:19px;margin:22px 0 32px;max-width:540px}
    @media(max-width:900px){.hero p.lead{margin-left:auto;margin-right:auto}}
    .cta-row{display:flex;gap:14px;flex-wrap:wrap}
    @media(max-width:900px){.cta-row{justify-content:center}}
    .trust{margin-top:30px;color:var(--muted);font-size:13px;display:flex;gap:18px;flex-wrap:wrap}
    @media(max-width:900px){.trust{justify-content:center}}
    .trust b{color:var(--txt)}

    /* PHONE MOCKUP */
    .phone{justify-self:center;width:300px;height:600px;background:#0a0f1c;border-radius:42px;
      border:10px solid #1b2438;box-shadow:0 40px 80px -30px rgba(0,0,0,.8);position:relative;overflow:hidden}
    .phone .wa-top{background:#075e54;padding:34px 16px 12px;display:flex;align-items:center;gap:10px}
    .wa-top .av{width:38px;height:38px;border-radius:50%;background:#25d366;display:grid;place-items:center;font-size:18px}
    .wa-top .nm{font-weight:700;font-size:15px}
    .wa-top .st{font-size:11px;color:#bfe9d8}
    .wa-body{background:#0b141a;height:100%;padding:16px 12px;display:flex;flex-direction:column;gap:10px;
      background-image:radial-gradient(rgba(255,255,255,.03) 1px,transparent 1px);background-size:18px 18px}
    .bub{max-width:78%;padding:9px 12px;border-radius:12px;font-size:13.5px;line-height:1.4;animation:pop .5s both}
    .bub.in{background:#1f2c34;align-self:flex-start;border-top-left-radius:3px}
    .bub.out{background:#005c4b;align-self:flex-end;border-top-right-radius:3px}
    .bub.d1{animation-delay:.2s}.bub.d2{animation-delay:.7s}.bub.d3{animation-delay:1.2s}.bub.d4{animation-delay:1.7s}
    @keyframes pop{from{opacity:0;transform:translateY(8px) scale(.96)}to{opacity:1;transform:none}}

    /* SECTIONS */
    section{padding:80px 0}
    .eyebrow{color:var(--brand);font-weight:700;letter-spacing:1px;text-transform:uppercase;font-size:13px;text-align:center}
    .h2{font-size:clamp(28px,4vw,42px);font-weight:800;text-align:center;margin:10px 0 14px;letter-spacing:-1px}
    .sub{color:var(--muted);text-align:center;max-width:600px;margin:0 auto 50px;font-size:17px}

    .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
    @media(max-width:860px){.grid3{grid-template-columns:1fr}}
    .feature{background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);
      border-radius:18px;padding:28px;transition:.25s}
    .feature:hover{transform:translateY(-4px);border-color:rgba(34,197,94,.4)}
    .feature .ic{width:48px;height:48px;border-radius:12px;display:grid;place-items:center;font-size:24px;
      background:rgba(34,197,94,.12);margin-bottom:16px}
    .feature h3{font-size:18px;margin-bottom:8px}
    .feature p{color:var(--muted);font-size:15px}

    /* STEPS */
    .steps{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;counter-reset:s}
    @media(max-width:860px){.steps{grid-template-columns:1fr}}
    .step{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:28px}
    .step .n{counter-increment:s;font-size:13px;font-weight:800;color:#03130b;width:32px;height:32px;border-radius:9px;
      display:grid;place-items:center;background:linear-gradient(120deg,var(--brand),var(--brand2));margin-bottom:16px}
    .step .n::before{content:counter(s)}
    .step h3{font-size:18px;margin-bottom:8px}.step p{color:var(--muted);font-size:15px}

    /* PRICING */
    .price-wrap{max-width:440px;margin:0 auto}
    .price-card{background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid rgba(34,197,94,.35);
      border-radius:24px;padding:40px 34px;text-align:center;position:relative;
      box-shadow:0 30px 70px -30px rgba(34,197,94,.4)}
    .pill{position:absolute;top:-14px;left:50%;transform:translateX(-50%);background:linear-gradient(120deg,var(--brand),var(--brand2));
      color:#03130b;font-weight:700;font-size:12px;padding:6px 16px;border-radius:999px}
    .amount{font-size:60px;font-weight:900;letter-spacing:-2px;margin:10px 0 2px}
    .amount span{font-size:18px;color:var(--muted);font-weight:500}
    .plist{list-style:none;text-align:left;margin:26px 0}
    .plist li{padding:10px 0 10px 30px;position:relative;color:#cdd6ea}
    .plist li::before{content:"✓";position:absolute;left:0;color:var(--brand);font-weight:800}
    .pn{color:var(--muted);font-size:13px;margin-top:16px}

    /* FAQ */
    .faq{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
    details{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 22px;cursor:pointer}
    details[open]{border-color:rgba(34,197,94,.35)}
    summary{font-weight:600;font-size:16px;list-style:none;display:flex;justify-content:space-between;align-items:center}
    summary::-webkit-details-marker{display:none}
    summary::after{content:"+";color:var(--brand);font-size:22px;font-weight:700}
    details[open] summary::after{content:"–"}
    details p{color:var(--muted);margin-top:12px;font-size:15px}

    /* CTA band */
    .band{background:linear-gradient(120deg,rgba(34,197,94,.14),rgba(99,102,241,.14));
      border:1px solid var(--line);border-radius:24px;padding:54px 30px;text-align:center}

    footer{border-top:1px solid var(--line);padding:40px 0;color:var(--muted);font-size:14px}
    .foot-in{display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;align-items:center}

    /* MODAL + TOAST */
    .modal{position:fixed;inset:0;background:rgba(3,6,14,.7);backdrop-filter:blur(6px);
      display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
    .modal.show{display:flex}
    .modal-card{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:34px;max-width:420px;width:100%}
    .modal-card h3{font-size:22px;margin-bottom:6px}
    .modal-card p{color:var(--muted);font-size:14px;margin-bottom:20px}
    .modal-card input{width:100%;padding:14px;border-radius:12px;border:1px solid var(--line);
      background:var(--bg);color:var(--txt);font-size:15px;font-family:inherit;margin-bottom:14px}
    .modal-card input:focus{outline:none;border-color:var(--brand)}
    .x{float:right;color:var(--muted);font-size:22px;cursor:pointer;line-height:1}
    .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(120px);
      background:var(--panel);border:1px solid var(--line);color:var(--txt);padding:14px 22px;border-radius:12px;
      font-size:14px;z-index:200;transition:.35s;box-shadow:0 20px 40px -16px rgba(0,0,0,.7);max-width:90%}
    .toast.show{transform:translateX(-50%) translateY(0)}
  </style>
"""

LANDING_HTML = """<!doctype html>
<html lang="es">
<head>
  <title>Wabu — Chatbots de WhatsApp con IA, listos en minutos</title>
""" + _HEAD + """
</head>
<body>
  <nav><div class="container nav-in">
    <a class="logo"><span class="dot">🤖</span> Wabu</a>
    <div class="nav-links">
      <a href="#features">Características</a>
      <a href="#how">Cómo funciona</a>
      <a href="#pricing">Precios</a>
      <a href="#faq">FAQ</a>
    </div>
    <button class="btn btn-primary" onclick="openModal()">Empezar ahora</button>
  </div></nav>

  <header class="hero"><div class="container">
    <span class="glow a"></span><span class="glow b"></span>
    <div class="hero-grid">
      <div>
        <span class="badge">● En vivo 24/7 en WhatsApp</span>
        <h1>Vende y atiende por <span class="grad-text">WhatsApp</span> con un bot que nunca duerme</h1>
        <p class="lead">Activa un chatbot con IA conectado a tu WhatsApp en minutos.
           Cobro mensual automático. Si dejas de pagar, se desactiva solo — sin contratos ni sorpresas.</p>
        <div class="cta-row">
          <button class="btn btn-primary" onclick="openModal()">Activar mi bot — $29/mes</button>
          <a href="#how" class="btn btn-ghost">Ver cómo funciona</a>
        </div>
        <div class="trust">
          <span>⚡ <b>Listo en minutos</b></span>
          <span>🔒 <b>Pago seguro con Stripe</b></span>
          <span>🚫 <b>Cancela cuando quieras</b></span>
        </div>
      </div>
      <div class="phone">
        <div class="wa-top">
          <div class="av">🤖</div>
          <div><div class="nm">Bot de Ventas</div><div class="st">en línea</div></div>
        </div>
        <div class="wa-body">
          <div class="bub in d1">¡Hola! 👋 ¿En qué puedo ayudarte hoy?</div>
          <div class="bub out d2">Quiero info de precios</div>
          <div class="bub in d3">Claro 🙌 Tenemos el plan Pro a $29/mes con bot ilimitado. ¿Te comparto el link de pago?</div>
          <div class="bub out d4">Sí, por favor 💳</div>
        </div>
      </div>
    </div>
  </div></header>

  <section id="features"><div class="container">
    <p class="eyebrow">Todo incluido</p>
    <h2 class="h2">Una plataforma, todo el flujo</h2>
    <p class="sub">Desde la página de venta hasta el cobro y la activación del bot. Sin pegar diez herramientas a mano.</p>
    <div class="grid3">
      <div class="feature"><div class="ic">💬</div><h3>WhatsApp con YCloud</h3>
        <p>Mensajería oficial de WhatsApp Business. Recibe y responde a tus clientes en tiempo real.</p></div>
      <div class="feature"><div class="ic">🧠</div><h3>Cerebro en n8n</h3>
        <p>El bot corre sobre un workflow de n8n: lógica, IA e integraciones sin límites.</p></div>
      <div class="feature"><div class="ic">💳</div><h3>Cobro mensual con Stripe</h3>
        <p>Suscripción recurrente con tarjeta. Facturación automática cada mes, sin perseguir pagos.</p></div>
      <div class="feature"><div class="ic">🔌</div><h3>Apagado automático</h3>
        <p>Si un pago falla o el cliente cancela, el bot se desactiva solo. Al regularizar, vuelve a la vida.</p></div>
      <div class="feature"><div class="ic">📊</div><h3>Estado en Supabase</h3>
        <p>Cada cliente, suscripción y bot queda registrado y sincronizado en tu base de datos.</p></div>
      <div class="feature"><div class="ic">⚡</div><h3>Deploy en Vercel</h3>
        <p>Infraestructura serverless en Python. Escala sola y se despliega con un push.</p></div>
    </div>
  </div></section>

  <section id="how" style="background:var(--bg2)"><div class="container">
    <p class="eyebrow">Simple de verdad</p>
    <h2 class="h2">Cómo funciona</h2>
    <p class="sub">Tres pasos y tu cliente ya está hablando con un bot que cobra solo.</p>
    <div class="steps">
      <div class="step"><div class="n"></div><h3>El cliente se suscribe</h3>
        <p>Entra a tu página, paga $29/mes con tarjeta vía Stripe Checkout. Seguro y en segundos.</p></div>
      <div class="step"><div class="n"></div><h3>El bot se activa solo</h3>
        <p>Stripe avisa por webhook y activamos su workflow de n8n. El bot empieza a responder en WhatsApp.</p></div>
      <div class="step"><div class="n"></div><h3>Cobro y control automáticos</h3>
        <p>Cada mes se cobra solo. Si el pago falla, el bot se apaga automáticamente. Cero gestión manual.</p></div>
    </div>
  </div></section>

  <section id="pricing"><div class="container">
    <p class="eyebrow">Precio único</p>
    <h2 class="h2">Sin letra pequeña</h2>
    <p class="sub">Un plan, todo incluido. Cancela cuando quieras desde tu WhatsApp.</p>
    <div class="price-wrap"><div class="price-card">
      <span class="pill">MÁS POPULAR</span>
      <div style="color:var(--muted);font-weight:600">Plan Pro</div>
      <div class="amount">$29<span> USD/mes</span></div>
      <ul class="plist">
        <li>Bot de WhatsApp con IA, ilimitado</li>
        <li>Integración oficial con YCloud</li>
        <li>Workflow n8n personalizable</li>
        <li>Cobro recurrente automático</li>
        <li>Desactivación automática por impago</li>
        <li>Soporte por WhatsApp</li>
      </ul>
      <button class="btn btn-primary" style="width:100%" onclick="openModal()">Suscribirme y activar mi bot</button>
      <p class="pn">Pago seguro con Stripe · Tarjeta de crédito o débito</p>
    </div></div>
  </div></section>

  <section id="faq" style="background:var(--bg2)"><div class="container">
    <p class="eyebrow">Dudas</p>
    <h2 class="h2">Preguntas frecuentes</h2>
    <div class="faq" style="margin-top:40px">
      <details open><summary>¿Qué pasa si no pago un mes?</summary>
        <p>Stripe intenta el cobro y, si falla, recibimos un aviso automático y desactivamos tu bot al instante. En cuanto regularizas el pago, se reactiva solo.</p></details>
      <details><summary>¿Necesito instalar algo?</summary>
        <p>No. Todo corre en la nube (Vercel + n8n + YCloud). Tú solo te suscribes y nosotros activamos tu bot.</p></details>
      <details><summary>¿Puedo cancelar cuando quiera?</summary>
        <p>Sí, sin permanencia. Al cancelar la suscripción el bot deja de funcionar al final del periodo pagado.</p></details>
      <details><summary>¿El bot usa WhatsApp oficial?</summary>
        <p>Sí, a través de YCloud, proveedor oficial de la API de WhatsApp Business. Nada de métodos no autorizados.</p></details>
    </div>
  </div></section>

  <section><div class="container"><div class="band">
    <h2 class="h2" style="margin-top:0">¿List@ para automatizar tu WhatsApp?</h2>
    <p class="sub">Activa tu bot hoy y deja que venda por ti 24/7.</p>
    <button class="btn btn-primary" onclick="openModal()">Empezar ahora — $29/mes</button>
  </div></div></section>

  <footer><div class="container foot-in">
    <a class="logo"><span class="dot">🤖</span> Wabu</a>
    <span>© 2026 Wabu · Chatbots de WhatsApp con IA</span>
  </div></footer>

  <!-- MODAL -->
  <div class="modal" id="modal">
    <div class="modal-card">
      <span class="x" onclick="closeModal()">×</span>
      <h3>Activa tu bot 🚀</h3>
      <p>Escribe tu correo y te llevamos al pago seguro de Stripe.</p>
      <form id="subForm">
        <input type="email" id="email" placeholder="tu@correo.com" required>
        <button class="btn btn-primary" style="width:100%" type="submit" id="subBtn">Ir al pago seguro →</button>
      </form>
    </div>
  </div>
  <div class="toast" id="toast"></div>

  <script>
    const modal=document.getElementById('modal');
    function openModal(){modal.classList.add('show');setTimeout(()=>document.getElementById('email').focus(),50)}
    function closeModal(){modal.classList.remove('show')}
    modal.addEventListener('click',e=>{if(e.target===modal)closeModal()});
    function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
      setTimeout(()=>t.classList.remove('show'),4500)}

    document.getElementById('subForm').addEventListener('submit',async(e)=>{
      e.preventDefault();
      const btn=document.getElementById('subBtn');
      const email=document.getElementById('email').value;
      btn.disabled=true;btn.textContent='Procesando…';
      try{
        const res=await fetch('/create-checkout-session',{
          method:'POST',headers:{'Content-Type':'application/json'},
          body:JSON.stringify({email})});
        const data=await res.json();
        if(data.url){window.location=data.url;return}
        toast(data.error||'No se pudo iniciar el pago. Intenta de nuevo.');
      }catch(err){toast('Error de conexión. Intenta de nuevo.')}
      btn.disabled=false;btn.textContent='Ir al pago seguro →';
    });
  </script>
</body>
</html>"""


def status_page(emoji: str, title: str, text: str, accent: str = "#22c55e") -> str:
    return """<!doctype html><html lang="es"><head>
  <title>""" + title + """ — Wabu</title>""" + _HEAD + """</head>
  <body><section style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px">
    <div style="text-align:center;max-width:480px">
      <div style="font-size:64px;margin-bottom:16px">""" + emoji + """</div>
      <h1 style="font-size:34px;margin-bottom:14px">""" + title + """</h1>
      <p style="color:var(--muted);font-size:17px;margin-bottom:28px">""" + text + """</p>
      <a href="/" class="btn btn-primary">← Volver al inicio</a>
    </div>
  </section></body></html>"""
