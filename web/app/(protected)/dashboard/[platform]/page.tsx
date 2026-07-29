export default async function PlatformDetailPage({
  params,
}: {
  params: Promise<{ platform: string }>;
}) {
  const { platform } = await params;
  return (
    <div>
      <h1 className="text-lg font-semibold capitalize">{platform} — deep dive</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Per-platform follower/engagement charts and posts table — build order step 6+.
      </p>
    </div>
  );
}
