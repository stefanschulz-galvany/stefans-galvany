-- Technischer Schreibzugriff fuer den geschuetzten Angebots-PDF-Upload.
-- CRM-Benutzer behalten weiterhin ausschliesslich Leserechte.
grant select, insert, update, delete
on table public.galvany_offer_files
to service_role;
