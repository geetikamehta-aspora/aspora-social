/**
 * Drive-upload bridge for the Aspora Leadership Dashboard.
 *
 * The dashboard's /settings/uploads form still does the "mapping" step
 * (brand/platform/account/period) — this script is only the file-storage
 * backend: it receives the file bytes from the Next.js server (never
 * directly from the browser, so the shared secret below never reaches the
 * client), saves them into Drive under
 *   <DEFAULT_FOLDER_ID>/<date>/<platform>/<brand>/<filename>
 * (creating any missing folders along the way), sets link-sharing to
 * "anyone with the link" (so the Python parser can fetch it with a plain
 * HTTP GET, no Drive API auth needed there), and returns the file ID + a
 * viewable link for the review-queue UI.
 *
 * Setup:
 *   1. Open this script by its script ID at script.google.com, paste this
 *      file in as Code.gs.
 *   2. Project Settings -> Script Properties, add:
 *        SHARED_SECRET     — a random string; must match GAS_UPLOAD_SHARED_SECRET
 *                             in web/.env.local (server-only, never NEXT_PUBLIC_)
 *        DEFAULT_FOLDER_ID — the root Drive folder ID (e.g. 1EHnr0R53edAY9XFy3KkNV5okGmgPhLzy)
 *   3. Deploy -> New deployment -> type "Web app".
 *        Execute as: Me
 *        Who has access: Anyone
 *      Copy the resulting /exec URL into web/.env.local as
 *      GAS_UPLOAD_WEBHOOK_URL.
 *   4. After any edit to this file: Deploy -> Manage deployments -> Edit ->
 *      New version — saving alone does not update the live /exec endpoint.
 */

// Apps Script Web Apps can't set an arbitrary HTTP status code on doPost
// responses (they're always 200 unless the script itself throws) — the
// caller (Next.js route) checks for an `error` key in the JSON body rather
// than relying on HTTP status.
function doPost(e) {
  try {
    var body = JSON.parse(e.postData.contents);

    var expectedSecret = PropertiesService.getScriptProperties().getProperty("SHARED_SECRET");
    if (!expectedSecret || body.secret !== expectedSecret) {
      return jsonResponse({ error: "unauthorized" });
    }

    if (!body.filename || !body.mimeType || !body.base64Data) {
      return jsonResponse({ error: "missing filename, mimeType, or base64Data" });
    }

    var rootFolderId = PropertiesService.getScriptProperties().getProperty("DEFAULT_FOLDER_ID");
    if (!rootFolderId) {
      return jsonResponse({ error: "DEFAULT_FOLDER_ID is not configured in Script Properties" });
    }
    var rootFolder = DriveApp.getFolderById(rootFolderId);

    // pathParts e.g. ["2026-07-29", "instagram", "aspora"] -> date > platform > brand
    var pathParts = body.pathParts || [];
    var targetFolder = getOrCreateNestedFolder(rootFolder, pathParts);

    var decodedBytes = Utilities.base64Decode(body.base64Data);
    var blob = Utilities.newBlob(decodedBytes, body.mimeType, body.filename);
    var file = targetFolder.createFile(blob);

    // "Anyone with the link can view" — no Google auth needed to fetch it,
    // which is what lets the Python parser download with a plain GET.
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

    var fileId = file.getId();
    return jsonResponse({
      fileId: fileId,
      viewUrl: "https://drive.google.com/file/d/" + fileId + "/view",
      downloadUrl: "https://drive.google.com/uc?export=download&id=" + fileId,
    });
  } catch (err) {
    return jsonResponse({ error: String(err) });
  }
}

/** Walks pathParts under `folder`, creating any missing subfolder, and
 * returns the innermost folder. Reuses an existing subfolder by exact name
 * match rather than creating duplicates on repeated uploads for the same
 * date/platform/brand. */
function getOrCreateNestedFolder(folder, pathParts) {
  var current = folder;
  for (var i = 0; i < pathParts.length; i++) {
    var name = String(pathParts[i]);
    var existing = current.getFoldersByName(name);
    current = existing.hasNext() ? existing.next() : current.createFolder(name);
  }
  return current;
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}

/**
 * Run this manually from the Apps Script editor (select "testDriveAccess"
 * in the function dropdown next to the Run button, then click Run) — NOT
 * via the deployed Web App. Two things this catches that the Web App error
 * hides:
 *   1. First-ever Drive access from this script triggers Google's
 *      authorization consent screen right here in the editor — accept it.
 *   2. If DEFAULT_FOLDER_ID is wrong, or belongs to a different Google
 *      account than whichever one you're logged into right now (this
 *      script always runs as "you" when deployed as "Execute as: Me"),
 *      you'll see the real permission error immediately in the execution
 *      log instead of the vague "unexpected error" the Web App wraps it in.
 */
function testDriveAccess() {
  var folderId = PropertiesService.getScriptProperties().getProperty("DEFAULT_FOLDER_ID");
  Logger.log("DEFAULT_FOLDER_ID = " + folderId);
  var folder = DriveApp.getFolderById(folderId);
  Logger.log("Folder name: " + folder.getName());
  Logger.log("SUCCESS — this account can access the folder.");
}
