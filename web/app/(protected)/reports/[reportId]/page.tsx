export default async function ReportDetailPage({
  params,
}: {
  params: Promise<{ reportId: string }>;
}) {
  const { reportId } = await params;
  return (
    <div>
      <h1 className="text-lg font-semibold">Report {reportId}</h1>
    </div>
  );
}
