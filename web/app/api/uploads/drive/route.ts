import { NextResponse } from "next/server";

/**
 * Thin relay: browser -> here -> Google Apps Script Web App -> Drive.
 * The only reason this hop exists is that the GAS shared secret can't live
 * in the browser. It does NOT touch Supabase — the file_uploads row is
 * still inserted directly from the browser via supabase-js, same as the
 * rest of the dashboard's writes.
 *
 * No auth check here — there's no server-side session to check anymore
 * (see sql/003_rls.sql's header comment on the Firebase-only auth model).
 * The /settings/uploads UI is only shown to admins client-side; this route
 * itself will relay for anyone who calls it directly, same trade-off as
 * every other write in this app. See gas/README.md.
 */
export async function POST(request: Request) {
  const webhookUrl = process.env.GAS_UPLOAD_WEBHOOK_URL;
  const sharedSecret = process.env.GAS_UPLOAD_SHARED_SECRET;
  if (!webhookUrl || !sharedSecret) {
    return NextResponse.json({ error: "Drive-upload bridge is not configured yet" }, { status: 500 });
  }

  const formData = await request.formData();
  const file = formData.get("file");
  if (!(file instanceof File)) {
    return NextResponse.json({ error: "Missing file" }, { status: 400 });
  }

  // e.g. ["2026-07-29", "instagram", "aspora"] -> date/platform/brand under
  // the root Drive folder (gas/Code.gs builds any missing subfolders).
  const pathPartsRaw = formData.get("pathParts");
  const pathParts = typeof pathPartsRaw === "string" ? JSON.parse(pathPartsRaw) : [];

  const bytes = await file.arrayBuffer();
  const base64Data = Buffer.from(bytes).toString("base64");

  const gasResponse = await fetch(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      secret: sharedSecret,
      filename: file.name,
      mimeType: file.type || "application/octet-stream",
      base64Data,
      pathParts,
    }),
  });

  const result = await gasResponse.json();
  if (result.error) {
    return NextResponse.json({ error: result.error }, { status: 502 });
  }

  return NextResponse.json(result);
}
