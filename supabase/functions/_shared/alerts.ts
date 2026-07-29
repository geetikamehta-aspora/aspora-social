export async function notifySlack(text: string): Promise<void> {
  const webhookUrl = Deno.env.get("SLACK_WEBHOOK_URL");
  if (!webhookUrl) return;
  await fetch(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

export function notifyIngestionFailure(platform: string, error: string): Promise<void> {
  return notifySlack(`:rotating_light: *${platform}* ingestion failed\n\`\`\`${error}\`\`\``);
}
