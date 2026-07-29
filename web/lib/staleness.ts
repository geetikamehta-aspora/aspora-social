export type StalenessLevel = "fresh" | "stale" | "very-stale" | "never";

/** Thresholds match the process-uploads.yml Slack-nudge threshold (~40h) —
 * the dashboard badge should go amber/red before the alert even fires, so a
 * gap is visible on the page before anyone has to check Slack.
 */
export function getStalenessLevel(lastIngestedAt: string | null): StalenessLevel {
  if (!lastIngestedAt) return "never";
  const hours = (Date.now() - new Date(lastIngestedAt).getTime()) / (1000 * 60 * 60);
  if (hours < 24) return "fresh";
  if (hours < 48) return "stale";
  return "very-stale";
}

export function formatRelativeTime(lastIngestedAt: string | null): string {
  if (!lastIngestedAt) return "never updated";
  const ms = Date.now() - new Date(lastIngestedAt).getTime();
  const hours = Math.floor(ms / (1000 * 60 * 60));
  if (hours < 1) return "updated <1h ago";
  if (hours < 24) return `updated ${hours}h ago`;
  return `updated ${Math.floor(hours / 24)}d ago`;
}
