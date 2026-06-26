-- ============================================================
--  Esquema de base de datos (Supabase / Postgres)
--  Guarda el estado de cada cliente/suscripción y su bot.
-- ============================================================

create table if not exists public.subscriptions (
    id                      uuid primary key default gen_random_uuid(),
    email                   text,
    whatsapp                text,                 -- número del cliente (E.164) para avisos
    stripe_customer_id      text,
    stripe_subscription_id  text unique,          -- clave de conflicto en upsert
    n8n_workflow_id         text,                 -- workflow que actúa como bot
    status                  text default 'inactive',  -- active | past_due | canceled | inactive
    bot_active              boolean default false,
    created_at              timestamptz default now(),
    updated_at              timestamptz default now()
);

create index if not exists idx_subscriptions_customer
    on public.subscriptions (stripe_customer_id);

-- Mantener updated_at al día
create or replace function public.set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_subscriptions_updated_at on public.subscriptions;
create trigger trg_subscriptions_updated_at
    before update on public.subscriptions
    for each row execute function public.set_updated_at();

-- La API usa la service_role key (acceso server-side), por lo que RLS
-- puede quedar activado sin políticas públicas. Si lo activas:
alter table public.subscriptions enable row level security;
