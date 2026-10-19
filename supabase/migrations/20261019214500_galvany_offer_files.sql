-- Private Angebots-PDFs fuer das GALVANY CRM
-- PDFs bleiben privat; nur angemeldete CRM-Benutzer duerfen sie lesen.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('galvany-offers', 'galvany-offers', false, 15728640, array['application/pdf'])
on conflict (id) do update
set public = false,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

create table if not exists public.galvany_offer_files (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid not null references public.galvany_leads(id) on delete cascade,
  message_key text not null,
  filename text not null,
  storage_path text not null unique,
  sha256 text not null,
  offer_no text,
  manufacturer text check (manufacturer in ('P','V')),
  capacity_kw text,
  tcap_code text check (tcap_code in ('M','L')),
  gross text,
  sent_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (lead_id, message_key, filename)
);

create index if not exists galvany_offer_files_lead_sent_idx
  on public.galvany_offer_files (lead_id, sent_at desc);

alter table public.galvany_offer_files enable row level security;

drop policy if exists "crm users read offer metadata" on public.galvany_offer_files;
create policy "crm users read offer metadata"
on public.galvany_offer_files
for select
to authenticated
using (true);

drop policy if exists "crm users read offer pdfs" on storage.objects;
create policy "crm users read offer pdfs"
on storage.objects
for select
to authenticated
using (bucket_id = 'galvany-offers');

revoke insert, update, delete on public.galvany_offer_files from anon, authenticated;
grant select on public.galvany_offer_files to authenticated;
