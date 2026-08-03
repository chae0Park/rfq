"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import DraftEmailViewer from "@/components/dashboard/DraftEmailViewer";

import {
  approveRFQ,
  rejectRFQ,
  generateDraftEmail,
} from "@/services/dashboard";

import type { DraftEmail } from "@/types/emailDraft";

interface ActionButtonsProps {
  rfqId: number;
  // onDraftGenerated: (draft: DraftEmail) => void;
}

export default function ActionButtons({
  rfqId,
  // onDraftGenerated,
}: ActionButtonsProps) {
  const router = useRouter();

  const [loadingAction, setLoadingAction] = useState<
    "approve" | "reject" | "draft" | null
  >(null);

  const [draft, setDraft] = useState<DraftEmail | null>(null);

  const [error, setError] = useState<string | null>(null);

  async function handleApprove() {
    setLoadingAction("approve");
    setError(null);

    try {
      await approveRFQ(rfqId, {
        decision: "APPROVED",
        reviewer: "Chaeyoung Park",
        comment: "Pricing reviewed and approved from the dashboard.",
      });

      router.refresh();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to approve RFQ."
      );
    } finally {
      setLoadingAction(null);
    }
  }

  async function handleReject() {
    setLoadingAction("reject");
    setError(null);

    try {
      await rejectRFQ(rfqId, {
        decision: "REJECTED",
        reviewer: "Chaeyoung Park",
        comment: "RFQ rejected from the dashboard.",
      });

      router.refresh();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to reject RFQ."
      );
    } finally {
      setLoadingAction(null);
    }
  }

  async function handleDraft() {
    setLoadingAction("draft");
    setError(null);

    try {
      const generatedDraft = await generateDraftEmail(rfqId);

      setDraft(generatedDraft);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to generate draft email."
      );
    } finally {
      setLoadingAction(null);
    }
  }

  const isLoading = loadingAction !== null;

  return (
    <div className="action-section">
      <div className="action-buttons">
        <button
          className="approve-button"
          onClick={handleApprove}
          disabled={isLoading}
        >
          {loadingAction === "approve"
            ? "Approving..."
            : "Approve"}
        </button>

        <button
          className="reject-button"
          onClick={handleReject}
          disabled={isLoading}
        >
          {loadingAction === "reject"
            ? "Rejecting..."
            : "Reject"}
        </button>

        <button
          className="draft-button"
          onClick={handleDraft}
          disabled={isLoading}
        >
          {loadingAction === "draft"
            ? "Generating..."
            : "Generate Draft"}
        </button>
      </div>

      {error && (
        <p className="action-error">
          {error}
        </p>
      )}

      <DraftEmailViewer
          draft={draft}
      />
    </div>
  );
}