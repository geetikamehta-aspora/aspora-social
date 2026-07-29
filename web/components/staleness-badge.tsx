import { Badge } from "@/components/ui/badge";
import { formatRelativeTime, getStalenessLevel } from "@/lib/staleness";

const VARIANT_BY_LEVEL = {
  fresh: "success",
  stale: "warning",
  "very-stale": "danger",
  never: "danger",
} as const;

export function StalenessBadge({ lastIngestedAt }: { lastIngestedAt: string | null }) {
  const level = getStalenessLevel(lastIngestedAt);
  return <Badge variant={VARIANT_BY_LEVEL[level]}>{formatRelativeTime(lastIngestedAt)}</Badge>;
}
