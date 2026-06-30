-- ============================================================
--  Wabu / SaaS — Esquema (REST por HTTPS, Supabase self-hosted)
--  Tablas con prefijo sass_ en el esquema public (aisladas por nombre).
--  Ejecutar en: Supabase Studio → SQL Editor (base principal `postgres`).
-- ============================================================

create extension if not exists pgcrypto;  -- para gen_random_uuid()

-- ── Cuentas (cada negocio que se registra = un tenant) ──────
create table if not exists public.sass_accounts (
    id              uuid primary key default gen_random_uuid(),
    email           text unique not null,
    password_hash   text not null,
    business_name   text,
    plan            text default 'trial',          -- trial | starter | pro | business
    status          text default 'trialing',       -- trialing | active | past_due | canceled
    trial_ends_at   timestamptz default (now() + interval '3 days'),
    stripe_customer_id      text,
    stripe_subscription_id  text,
    created_at      timestamptz default now(),
    updated_at      timestamptz default now()
);

-- ── Conexión de WhatsApp por cuenta ─────────────────────────
create table if not exists public.sass_whatsapp (
    id              uuid primary key default gen_random_uuid(),
    account_id      uuid references public.sass_accounts(id) on delete cascade,
    waba_id         text,
    phone_number_id text,
    display_number  text,
    status          text default 'disconnected',   -- disconnected | connected | restricted
    quality_rating  text,
    created_at      timestamptz default now()
);

-- ── Contactos / leads (CRM con pipeline) ────────────────────
create table if not exists public.sass_contacts (
    id          uuid primary key default gen_random_uuid(),
    account_id  uuid references public.sass_accounts(id) on delete cascade,
    name        text,
    phone       text,
    email       text,
    -- pipeline: nuevo | contactado | calificado | interesado | negociacion | cerrado | perdido
    status      text default 'nuevo',
    score       int default 0,
    source      text,                              -- whatsapp | manual | import | ad
    notes       text,
    created_at  timestamptz default now(),
    updated_at  timestamptz default now()
);
create index if not exists idx_sass_contacts_account on public.sass_contacts(account_id);
create index if not exists idx_sass_contacts_status  on public.sass_contacts(account_id, status);

-- ── Conversaciones y mensajes ───────────────────────────────
create table if not exists public.sass_messages (
    id          uuid primary key default gen_random_uuid(),
    account_id  uuid references public.sass_accounts(id) on delete cascade,
    contact_id  uuid references public.sass_contacts(id) on delete cascade,
    role        text not null,                     -- user | assistant | agent | system
    content     text,
    created_at  timestamptz default now()
);
create index if not exists idx_sass_messages_contact on public.sass_messages(contact_id, created_at);

-- ── Citas / agenda ──────────────────────────────────────────
create table if not exists public.sass_appointments (
    id            uuid primary key default gen_random_uuid(),
    account_id    uuid references public.sass_accounts(id) on delete cascade,
    contact_id    uuid references public.sass_contacts(id) on delete set null,
    title         text,
    scheduled_at  timestamptz,
    status        text default 'pending',          -- pending | confirmed | done | canceled
    created_at    timestamptz default now()
);

-- ── Catálogo de productos ───────────────────────────────────
create table if not exists public.sass_products (
    id          uuid primary key default gen_random_uuid(),
    account_id  uuid references public.sass_accounts(id) on delete cascade,
    name        text not null,
    description text,
    price       numeric,
    category    text,
    active      boolean default true,
    created_at  timestamptz default now()
);

-- ── Base de conocimiento (RAG) ──────────────────────────────
create table if not exists public.sass_knowledge (
    id          uuid primary key default gen_random_uuid(),
    account_id  uuid references public.sass_accounts(id) on delete cascade,
    title       text,
    content     text,
    category    text,
    status      text default 'synced',             -- synced | pending
    -- embedding vector(1536)  -- (activar con pgvector en Fase 3)
    created_at  timestamptz default now()
);

-- ── Configuración del agente IA por cuenta ──────────────────
create table if not exists public.sass_agent_config (
    account_id    uuid primary key references public.sass_accounts(id) on delete cascade,
    agent_name    text default 'Asistente',
    agent_role    text default 'asistente de ventas',
    business_type text default 'General',
    personality   text default 'profesional, amable y servicial',
    language      text default 'Español',
    tone          text default 'Formal pero cercano',
    welcome_msg   text,
    updated_at    timestamptz default now()
);

-- ── Funnel de ventas (pasos que guían al agente) ────────────
create table if not exists public.sass_funnel_steps (
    id          uuid primary key default gen_random_uuid(),
    account_id  uuid references public.sass_accounts(id) on delete cascade,
    position    int default 0,
    name        text,
    prompt      text,
    goals       text,
    created_at  timestamptz default now()
);

-- ── Webhooks salientes ──────────────────────────────────────
create table if not exists public.sass_webhooks (
    id          uuid primary key default gen_random_uuid(),
    account_id  uuid references public.sass_accounts(id) on delete cascade,
    url         text not null,
    events      text[] default '{}',
    secret      text,
    active      boolean default true,
    created_at  timestamptz default now()
);

-- ── Bots creados en n8n (vincula workflow a cuenta) ─────────
create table if not exists public.sass_bots (
    id            uuid primary key default gen_random_uuid(),
    account_id    uuid references public.sass_accounts(id) on delete cascade,
    name          text,
    n8n_workflow_id text,
    webhook_url   text,
    active        boolean default false,
    created_at    timestamptz default now()
);

-- updated_at automático en las tablas que lo usan
create or replace function public.sass_touch_updated_at()
returns trigger as $$
begin new.updated_at = now(); return new; end;
$$ language plpgsql;

drop trigger if exists trg_sass_accounts_upd on public.sass_accounts;
create trigger trg_sass_accounts_upd before update on public.sass_accounts
    for each row execute function public.sass_touch_updated_at();
drop trigger if exists trg_sass_contacts_upd on public.sass_contacts;
create trigger trg_sass_contacts_upd before update on public.sass_contacts
    for each row execute function public.sass_touch_updated_at();

-- Refresca el cache de PostgREST para que exponga las tablas nuevas
notify pgrst, 'reload schema';
