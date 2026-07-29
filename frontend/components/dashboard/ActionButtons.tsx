"use client";

import { useState } from "react";

import {
  approveRFQ,
  rejectRFQ,
  generateDraftEmail,
} from "@/services/dashboard";

interface Props {
  rfqId: number;
}

export default function ActionButtons({
  rfqId,
}: Props) {
  const [loading, setLoading] = useState(false);

  async function handleApprove() {
    setLoading(true);

    try {
      await approveRFQ(rfqId, {
        decision: "APPROVED",
        reviewer: "Chaeyoung Park",
        comment: "Approved from dashboard.",
      });

      alert("RFQ Approved");
    } finally {
      setLoading(false);
    }
  }

  async function handleReject() {
    setLoading(true);

    try {
      await rejectRFQ(rfqId, {
        decision: "REJECTED",
        reviewer: "Chaeyoung Park",
        comment: "Rejected from dashboard.",
      });

      alert("RFQ Rejected");
    } finally {
      setLoading(false);
    }
  }

  async function handleDraft() {
    setLoading(true);

    try {
      const draft = await generateDraftEmail(rfqId);

      alert(
        `${draft.subject}\n\n${draft.body}`
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="action-buttons">
      <button
        disabled={loading}
        onClick={handleApprove}
      >
        Approve
      </button>

      <button
        disabled={loading}
        onClick={handleReject}
      >
        Reject
      </button>

      <button
        disabled={loading}
        onClick={handleDraft}
      >
        Generate Draft
      </button>
    </div>
  );
}