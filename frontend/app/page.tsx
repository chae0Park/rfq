import { getRFQs } from "@/services/api";

export default async function Home() {
  const rfqs = await getRFQs();

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold">RFQ Dashboard</h1>

      <p className="mt-4">
        Total RFQs: {rfqs.length}
      </p>

      <pre className="mt-6">
        {JSON.stringify(rfqs, null, 2)}
      </pre>
    </main>
  );
}