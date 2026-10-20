import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors = {
  "access-control-allow-origin": "*",
  "access-control-allow-headers": "authorization, x-client-info, apikey, content-type, x-galvany-automation-token",
  "access-control-allow-methods": "POST, OPTIONS",
};

function response(status: number, body: Record<string, unknown>) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "content-type": "application/json; charset=utf-8" },
  });
}

function safeName(value: string) {
  return value.normalize("NFKD").replace(/[^a-zA-Z0-9._-]+/g, "_").slice(-120) || "angebot.pdf";
}

function decodeBase64(value: string) {
  const clean = value.replace(/^data:application\/pdf;base64,/, "");
  const binary = atob(clean);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
  if (req.method !== "POST") return response(405, { error: "Method not allowed" });

  const expected = Deno.env.get("GALVANY_AUTOMATION_TOKEN") || "";
  const supplied = req.headers.get("x-galvany-automation-token") || "";
  if (!expected || supplied !== expected) return response(401, { error: "Unauthorized" });

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return response(400, { error: "Invalid JSON" });
  }

  const leadId = String(body.lead_id || "");
  const messageKey = String(body.message_key || "");
  const filename = String(body.filename || "");
  const pdfBase64 = String(body.pdf_base64 || "");
  const sentAt = String(body.sent_at || "");
  if (!/^[0-9a-f-]{36}$/i.test(leadId) || !messageKey || !filename || !pdfBase64 || !sentAt) {
    return response(400, { error: "Missing or invalid fields" });
  }

  let pdf: Uint8Array;
  try {
    pdf = decodeBase64(pdfBase64);
  } catch {
    return response(400, { error: "Invalid PDF encoding" });
  }
  if (pdf.length < 5 || pdf.length > 15 * 1024 * 1024 ||
      String.fromCharCode(...pdf.slice(0, 5)) !== "%PDF-") {
    return response(400, { error: "Invalid PDF" });
  }

  const digest = await crypto.subtle.digest("SHA-256", pdf);
  const sha256 = [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
  const year = /^\d{4}/.test(sentAt) ? sentAt.slice(0, 4) : "unknown";
  const storagePath = `${leadId}/${year}/${sha256.slice(0, 16)}-${safeName(filename)}`;

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    { auth: { persistSession: false } },
  );

  const { data: lead, error: leadError } = await supabase
    .from("galvany_leads").select("id").eq("id", leadId).maybeSingle();
  if (leadError || !lead) return response(404, { error: "Lead not found" });

  const { error: uploadError } = await supabase.storage
    .from("galvany-offers")
    .upload(storagePath, pdf, { contentType: "application/pdf", upsert: true });
  if (uploadError) {
    console.error("offer upload storage stage failed:", uploadError.message);
    return response(502, { error: "PDF upload failed" });
  }

  const record = {
    lead_id: leadId,
    message_key: messageKey,
    filename,
    storage_path: storagePath,
    sha256,
    offer_no: body.offer_no || null,
    manufacturer: body.manufacturer || null,
    capacity_kw: body.capacity_kw || null,
    tcap_code: body.tcap_code || null,
    gross: body.gross || null,
    sent_at: sentAt,
  };
  const { error: dbError } = await supabase
    .from("galvany_offer_files")
    .upsert(record, { onConflict: "lead_id,message_key,filename" });
  if (dbError) {
    await supabase.storage.from("galvany-offers").remove([storagePath]);
    console.error("offer upload metadata stage failed:", dbError.code, dbError.message);
    const statusByCode: Record<string, number> = {
      "23514": 541,
      "22P02": 542,
      "42P01": 543,
      "42501": 544,
      "23505": 546,
    };
    const diagnosticStatus = String(dbError.code || "").startsWith("PGRST")
      ? 545
      : (statusByCode[String(dbError.code || "")] || 547);
    return response(diagnosticStatus, { error: "Metadata write failed" });
  }

  return response(200, { ok: true, storage_path: storagePath, sha256 });
});
