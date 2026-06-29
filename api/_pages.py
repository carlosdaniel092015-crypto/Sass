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
    .plans{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;align-items:stretch}
    @media(max-width:880px){.plans{grid-template-columns:1fr;max-width:440px;margin:0 auto}}
    .price-card{background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);
      border-radius:24px;padding:36px 30px;text-align:center;position:relative;display:flex;flex-direction:column}
    .price-card.feat{border-color:rgba(34,197,94,.5);box-shadow:0 30px 70px -30px rgba(34,197,94,.45);
      transform:scale(1.03)}
    @media(max-width:880px){.price-card.feat{transform:none}}
    .pill{position:absolute;top:-14px;left:50%;transform:translateX(-50%);background:linear-gradient(120deg,var(--brand),var(--brand2));
      color:#03130b;font-weight:700;font-size:12px;padding:6px 16px;border-radius:999px}
    .pname{color:var(--muted);font-weight:600;font-size:15px}
    .amount{font-size:50px;font-weight:900;letter-spacing:-2px;margin:8px 0 2px}
    .amount span{font-size:16px;color:var(--muted);font-weight:500}
    .plist{list-style:none;text-align:left;margin:22px 0;flex:1}
    .plist li{padding:9px 0 9px 28px;position:relative;color:#cdd6ea;font-size:14.5px}
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
    <p class="eyebrow">Planes</p>
    <h2 class="h2">Elige tu plan</h2>
    <p class="sub">Todos incluyen cobro automático y apagado por impago. Cancela cuando quieras.</p>
    <div class="plans">

      <div class="price-card">
        <div class="pname">Starter</div>
        <div class="amount">$19<span> USD/mes</span></div>
        <ul class="plist">
          <li>1 bot de WhatsApp</li>
          <li>Hasta 1.000 mensajes/mes</li>
          <li>Respuestas automáticas</li>
          <li>Integración con YCloud</li>
          <li>Soporte por email</li>
        </ul>
        <button class="btn btn-ghost" style="width:100%" onclick="openModal('starter')">Elegir Starter</button>
      </div>

      <div class="price-card feat">
        <span class="pill">MÁS POPULAR</span>
        <div class="pname">Pro</div>
        <div class="amount">$29<span> USD/mes</span></div>
        <ul class="plist">
          <li>Bot de WhatsApp <b>ilimitado</b></li>
          <li>Respuestas con IA</li>
          <li>Workflow n8n personalizable</li>
          <li>Desactivación automática por impago</li>
          <li>Soporte por WhatsApp</li>
        </ul>
        <button class="btn btn-primary" style="width:100%" onclick="openModal('pro')">Elegir Pro</button>
      </div>

      <div class="price-card">
        <div class="pname">Business</div>
        <div class="amount">$79<span> USD/mes</span></div>
        <ul class="plist">
          <li><b>Hasta 5 bots</b> de WhatsApp</li>
          <li>IA avanzada + base de conocimiento</li>
          <li>Integraciones a medida (CRM, Sheets…)</li>
          <li>Reportes y métricas</li>
          <li>Soporte prioritario</li>
        </ul>
        <button class="btn btn-ghost" style="width:100%" onclick="openModal('business')">Elegir Business</button>
      </div>

    </div>
    <p class="pn" style="text-align:center;margin-top:24px">Pago seguro con Stripe · Tarjeta de crédito o débito</p>
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
      <p>Plan seleccionado: <b id="planLabel">Pro</b>. Escribe tu correo y te llevamos al pago seguro de Stripe.</p>
      <form id="subForm">
        <input type="email" id="email" placeholder="tu@correo.com" required>
        <button class="btn btn-primary" style="width:100%" type="submit" id="subBtn">Ir al pago seguro →</button>
      </form>
    </div>
  </div>
  <div class="toast" id="toast"></div>

  <script>
    const modal=document.getElementById('modal');
    const PLAN_NAMES={starter:'Starter',pro:'Pro',business:'Business'};
    let selectedPlan='pro';
    function openModal(plan){
      selectedPlan=plan||'pro';
      document.getElementById('planLabel').textContent=PLAN_NAMES[selectedPlan]||'Pro';
      modal.classList.add('show');
      setTimeout(()=>document.getElementById('email').focus(),50);
    }
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
          body:JSON.stringify({email,plan:selectedPlan})});
        const data=await res.json();
        if(data.url){window.location=data.url;return}
        toast(data.error||'No se pudo iniciar el pago. Intenta de nuevo.');
      }catch(err){toast('Error de conexión. Intenta de nuevo.')}
      btn.disabled=false;btn.textContent='Ir al pago seguro →';
    });
  </script>
</body>
</html>"""


LOGIN_HTML = """<!doctype html>
<html lang="es">
<head>
  <title>Entrar — Wabu</title>
""" + _HEAD + """
  <style>
    .login-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
    .login-card{background:var(--panel);border:1px solid var(--line);border-radius:20px;
      padding:38px 34px;max-width:400px;width:100%}
    .login-card .logo{justify-content:center;margin-bottom:8px;font-size:22px}
    .login-card h1{font-size:22px;text-align:center;margin-bottom:6px}
    .login-card p.s{color:var(--muted);text-align:center;font-size:14px;margin-bottom:24px}
    .field{margin-bottom:14px}
    .field label{display:block;font-size:13px;color:var(--muted);margin-bottom:6px}
    .field input{width:100%;padding:13px 14px;border-radius:10px;border:1px solid var(--line);
      background:var(--bg);color:var(--txt);font-size:15px;font-family:inherit}
    .field input:focus{outline:none;border-color:var(--brand)}
  </style>
</head>
<body>
  <div class="login-wrap">
    <div class="login-card">
      <div class="logo"><span class="dot">🤖</span> Wabu</div>
      <h1>Entrar al panel</h1>
      <p class="s">Accede para gestionar tus bots y conexiones de WhatsApp.</p>
      <form id="loginForm">
        <div class="field"><label>Email</label>
          <input type="email" id="email" placeholder="tu@correo.com" required autocomplete="username"></div>
        <div class="field"><label>Contraseña</label>
          <input type="password" id="password" placeholder="••••••••" required autocomplete="current-password"></div>
        <button class="btn btn-primary" style="width:100%" type="submit" id="loginBtn">Entrar</button>
      </form>
    </div>
  </div>
  <div class="toast" id="toast"></div>
  <script>
    function toast(m){const t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),4500)}
    document.getElementById('loginForm').addEventListener('submit', async (e)=>{
      e.preventDefault();
      const btn=document.getElementById('loginBtn'); btn.disabled=true; btn.textContent='Entrando…';
      try{
        const res=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},
          body:JSON.stringify({email:document.getElementById('email').value,password:document.getElementById('password').value})});
        const data=await res.json();
        if(res.ok){window.location='/panel';return}
        toast(data.error||'No se pudo iniciar sesión');
      }catch(e){toast('Error de conexión')}
      btn.disabled=false; btn.textContent='Entrar';
    });
  </script>
</body>
</html>"""


PANEL_HTML = """<!doctype html>
<html lang="es">
<head>
  <title>Panel — Wabu</title>
""" + _HEAD + """
  <style>
    .panel{max-width:880px;margin:0 auto;padding:40px 24px}
    .panel h1{font-size:30px;margin-bottom:6px}
    .panel .sub2{color:var(--muted);margin-bottom:28px}
    .box{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:26px;margin-bottom:22px}
    .box h2{font-size:18px;margin-bottom:16px}
    .field{margin-bottom:14px}
    .field label{display:block;font-size:13px;color:var(--muted);margin-bottom:6px}
    .field input,.field textarea{width:100%;padding:12px 14px;border-radius:10px;border:1px solid var(--line);
      background:var(--bg);color:var(--txt);font-size:15px;font-family:inherit}
    .field textarea{min-height:80px;resize:vertical}
    .bot{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px;border:1px solid var(--line);
      border-radius:12px;margin-bottom:10px;background:var(--bg2)}
    .bot .meta{font-size:13px;color:var(--muted)}
    .tag{font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px}
    .tag.on{background:rgba(34,197,94,.15);color:#86efac}
    .tag.off{background:rgba(148,163,184,.15);color:var(--muted)}
    .hidden{display:none}
    code{background:var(--bg);padding:2px 7px;border-radius:6px;font-size:13px;color:#86efac;word-break:break-all}
  </style>
</head>
<body>
  <nav><div class="container nav-in">
    <a class="logo" href="/"><span class="dot">🤖</span> Wabu</a>
    <div class="nav-links"><a href="/">← Sitio</a><a href="#" onclick="logout();return false">Salir</a></div>
  </div></nav>

  <div class="panel">
    <h1>Panel de bots</h1>
    <p class="sub2">Crea y administra tus chatbots de WhatsApp en n8n.</p>

    <!-- App (visible solo con sesión válida) -->
    <div id="app" class="hidden">

      <div class="box">
        <h2>📲 Conectar WhatsApp</h2>
        <p class="meta" style="color:var(--muted);margin-bottom:16px">
          Conecta la cuenta de WhatsApp Business del cliente con el Embedded Signup de Meta.
          Elige crear un número nuevo o usar la app existente (coexistencia).
        </p>
        <div id="waNotReady" class="hidden" style="color:#fca5a5;font-size:14px;margin-bottom:12px">
          ⚠️ Falta configurar Meta (META_APP_ID y META_CONFIG_ID_SIGNUP).
        </div>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <button class="btn btn-primary" id="btnSignup" onclick="launchSignup('signup')">
            ➕ Nuevo número (crear WABA)
          </button>
          <button class="btn btn-ghost" id="btnCoex" onclick="launchSignup('coexistence')">
            📱 Usar app existente (Coexistencia)
          </button>
        </div>
        <div id="waResult" style="margin-top:16px"></div>
      </div>

      <div class="box">
        <h2>➕ Crear bot nuevo</h2>
        <div class="field">
          <label>Nombre del bot</label>
          <input id="botName" placeholder="Bot de Ventas - Cliente X">
        </div>
        <div class="field">
          <label>Mensaje de bienvenida / por defecto</label>
          <textarea id="botGreeting" placeholder="¡Hola! 👋 Soy el asistente de... ¿En qué te ayudo?"></textarea>
        </div>
        <button class="btn btn-primary" id="createBtn" onclick="createBot()">Crear bot en n8n</button>
        <div id="createResult" style="margin-top:16px"></div>
      </div>

      <div class="box">
        <h2>🤖 Tus bots</h2>
        <div id="botList"><p class="meta" style="color:var(--muted)">Cargando…</p></div>
      </div>
    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    let META = null;            // config del Embedded Signup
    let sessionInfo = {};       // waba_id / phone_number_id que envía Meta
    const $ = id => document.getElementById(id);
    function toast(m){const t=$('toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),4500)}
    function headers(){return {'Content-Type':'application/json'}}  // la sesión va por cookie
    async function logout(){ try{await fetch('/api/logout',{method:'POST'})}catch(e){} window.location='/login'; }

    // --- Embedded Signup de Meta (Facebook Login for Business) ---
    window.addEventListener('message', (event) => {
      if (!String(event.origin).endsWith('facebook.com')) return;
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'WA_EMBEDDED_SIGNUP') {
          // data.data: { phone_number_id, waba_id, ... }
          sessionInfo = data.data || {};
        }
      } catch (e) {}
    });

    function initFB(){
      if(!META || !META.app_id || window.FB) return;
      window.fbAsyncInit = function(){
        FB.init({ appId: META.app_id, autoLogAppEvents:true, xfbml:true, version: META.graph_version });
      };
      const s=document.createElement('script');
      s.async=true;s.defer=true;s.src='https://connect.facebook.net/en_US/sdk.js';
      document.body.appendChild(s);
    }

    function launchSignup(kind){
      if(!window.FB){toast('Meta aún no está listo. Revisa META_APP_ID.');return}
      const config_id = kind==='coexistence' ? META.config_id_coexistence : META.config_id_signup;
      if(!config_id){toast('Falta el config_id para '+kind);return}
      const extras = { setup:{}, sessionInfoVersion:'3' };
      if(kind==='coexistence') extras.featureType='whatsapp_business_app_onboarding';
      sessionInfo = {};
      FB.login(function(response){
        const code = response && response.authResponse && response.authResponse.code;
        if(!code){toast('Conexión cancelada');return}
        onboard(code, kind);
      }, { config_id, response_type:'code', override_default_response_type:true, extras });
    }

    async function onboard(code, kind){
      $('waResult').innerHTML='⏳ Registrando cuenta…';
      try{
        const res = await fetch('/api/whatsapp/onboard',{method:'POST',headers:headers(),
          body:JSON.stringify({code, waba_id:sessionInfo.waba_id, phone_number_id:sessionInfo.phone_number_id, kind})});
        const data = await res.json();
        if(res.ok){
          $('waResult').innerHTML = `✅ WhatsApp conectado (${kind==='coexistence'?'coexistencia':'nuevo número'}).<br>`+
            `WABA: <code>${sessionInfo.waba_id||'—'}</code><br>Phone ID: <code>${sessionInfo.phone_number_id||'—'}</code>`+
            (data.registered? '' : '<br><span class="meta">⚠️ '+(data.note||'Pendiente registrar en YCloud')+'</span>');
        }else{$('waResult').innerHTML='';toast(data.error||'No se pudo conectar')}
      }catch(e){$('waResult').innerHTML='';toast('Error de conexión')}
    }

    async function loadMeta(){
      try{
        const res = await fetch('/api/whatsapp/config',{headers:headers()});
        if(!res.ok) return;
        META = await res.json();
        if(META.ready){initFB();}
        else{$('waNotReady').classList.remove('hidden');$('btnSignup').disabled=true;$('btnCoex').disabled=true;}
      }catch(e){}
    }

    async function gate(){
      // Verifica la sesión; si no hay, manda al login.
      try{
        const res = await fetch('/api/me');
        if(!res.ok){window.location='/login';return}
      }catch(e){window.location='/login';return}
      $('app').classList.remove('hidden');
      loadBots(true);
      loadMeta();
    }

    async function loadBots(silent){
      try{
        const res = await fetch('/api/bots',{headers:headers()});
        if(res.status===401){return false}
        const data = await res.json();
        const list = $('botList');
        if(!data.bots || !data.bots.length){list.innerHTML='<p class="meta">Aún no hay bots. Crea el primero arriba 👆</p>';return true}
        list.innerHTML = data.bots.map(b=>`<div class="bot">
          <div><b>${b.name||'(sin nombre)'}</b><div class="meta">ID: ${b.id}</div></div>
          <span class="tag ${b.active?'on':'off'}">${b.active?'Activo':'Inactivo'}</span>
        </div>`).join('');
        return true;
      }catch(e){if(!silent)toast('Error de conexión');return false}
    }

    async function createBot(){
      const name = $('botName').value.trim();
      const greeting = $('botGreeting').value.trim();
      if(!name){toast('Ponle un nombre al bot');return}
      const btn = $('createBtn'); btn.disabled=true; btn.textContent='Creando…';
      try{
        const res = await fetch('/api/bots/create',{method:'POST',headers:headers(),body:JSON.stringify({name,greeting})});
        const data = await res.json();
        if(res.ok){
          $('createResult').innerHTML = `✅ Bot creado. Configura este webhook en YCloud:<br><code>${data.webhook_url}</code>`;
          $('botName').value=''; $('botGreeting').value='';
          loadBots(true);
        }else{toast(data.error||'No se pudo crear el bot')}
      }catch(e){toast('Error de conexión')}
      btn.disabled=false; btn.textContent='Crear bot en n8n';
    }

    // Al cargar, verifica sesión y muestra el panel (o redirige al login)
    gate();
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
