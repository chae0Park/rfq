import { notFound } from "next/navigation";

import RFQDetailClient from "@/components/dashboard/RFQDetailClient";

import { getRFQ } from "@/services/dashboard";

interface RFQDetailPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function RFQDetailPage({
  params,
}: RFQDetailPageProps) {
  const { id } = await params;

  const rfqId = Number(id);

  if (Number.isNaN(rfqId)) {
    notFound();
  }

  const rfq = await getRFQ(rfqId);

  if (!rfq) {
    notFound();
  }

  return (
    <main className="detail-page">
      <RFQDetailClient rfq={rfq} />
    </main>
  );
}