"use client";

import { useState } from "react";

import ActionButtons from "@/components/dashboard/ActionButtons";
import DraftEmailViewer from "@/components/dashboard/DraftEmailViewer";
import QuotationSummary from "@/components/dashboard/QuotationSummary";
import StatusBadge from "@/components/dashboard/StatusBadge";

import type { DraftEmail } from "@/types/emailDraft";
import type { RFQ } from "@/types/rfq";

interface RFQDetailClientProps {
  rfq: RFQ;
}

export default function RFQDetailClient({
  rfq,
}: RFQDetailClientProps) {
  const [draft, setDraft] =
    useState<DraftEmail | null>(null);

  return (
    <>
      <div className="detail-header">
        <div>
          <p className="eyebrow">
            RFQ Detail
          </p>

          <h1>
            {rfq.project_name ??
              "Untitled Project"}
          </h1>

          <p>RFQ #{rfq.id}</p>
        </div>

        <StatusBadge status={rfq.status} />
      </div>

      <div className="detail-grid">
        <section className="detail-card">
          <h2>Client</h2>

          <div className="info-row">
            <span>Name</span>

            <strong>
              {rfq.client_name ?? "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Email</span>

            <strong>
              {rfq.client_email ?? "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Company</span>

            <strong>
              {rfq.client ?? "-"}
            </strong>
          </div>
        </section>

        <section className="detail-card">
          <h2>Project</h2>

          <div className="info-row">
            <span>Country</span>

            <strong>
              {rfq.country ?? "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Methodology</span>

            <strong>
              {rfq.methodology ?? "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Sample Size</span>

            <strong>
              {rfq.sample_size
                ? rfq.sample_size.toLocaleString()
                : "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Timeline</span>

            <strong>
              {rfq.timeline ?? "-"}
            </strong>
          </div>
        </section>
      </div>

      {rfq.quotation && (
        <QuotationSummary
          quotation={rfq.quotation}
        />
      )}

      <ActionButtons
        rfqId={rfq.id}
        // onDraftGenerated={setDraft}
      />

      <DraftEmailViewer
        draft={draft}
      />
    </>
  );
}