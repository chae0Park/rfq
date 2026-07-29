import { notFound } from "next/navigation";

import { getRFQ } from "@/services/dashboard";
import StatusBadge from "@/components/dashboard/StatusBadge";

import ActionButtons from "@/components/dashboard/ActionButtons";

interface Props {
  params: Promise<{
    id: string;
  }>;
}

export default async function RFQDetailPage({ params }: Props) {
  const { id } = await params;

  const rfq = await getRFQ(Number(id));

  if (!rfq) {
    notFound();
  }

  return (
    <main className="detail-page">
      <div className="detail-header">
        <div>
          <h1>{rfq.project_name}</h1>
          <p>RFQ #{rfq.id}</p>
        </div>

        <StatusBadge status={rfq.status} />
      </div>

      <div className="detail-grid">
        <section className="detail-card">
          <h2>Client</h2>

          <div className="info-row">
            <span>Name</span>
            <strong>{rfq.client_name}</strong>
          </div>

          <div className="info-row">
            <span>Email</span>
            <strong>{rfq.client_email}</strong>
          </div>

          <div className="info-row">
            <span>Company</span>
            <strong>{rfq.client ?? "-"}</strong>
          </div>
        </section>

        <section className="detail-card">
          <h2>Project</h2>

          <div className="info-row">
            <span>Country</span>
            <strong>{rfq.country}</strong>
          </div>

          <div className="info-row">
            <span>Methodology</span>
            <strong>{rfq.methodology}</strong>
          </div>

          <div className="info-row">
            <span>Sample Size</span>
            <strong>{rfq.sample_size}</strong>
          </div>

          <div className="info-row">
            <span>Timeline</span>
            <strong>{rfq.timeline}</strong>
          </div>
        </section>
      </div>

      {/* <div className="action-buttons">
        <button>Approve</button>
        <button>Reject</button>
        <button>Generate Draft</button>
      </div> */}
      <ActionButtons rfqId={rfq.id} />
    </main>
  );
}