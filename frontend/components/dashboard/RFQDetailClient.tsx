"use client";

import { useState } from "react";

import ActionButtons from "@/components/dashboard/ActionButtons";
import DraftEmailViewer from "@/components/dashboard/DraftEmailViewer";
import QuotationSummary from "@/components/dashboard/QuotationSummary";
import StatusBadge from "@/components/dashboard/StatusBadge";

import { updateRFQ } from "@/services/dashboard";

import type { DraftEmail } from "@/types/emailDraft";
import type { RFQ } from "@/types/rfq";

interface RFQDetailClientProps {
  rfq: RFQ;
}

export default function RFQDetailClient({
  rfq,
}: RFQDetailClientProps) {
  // 현재 화면에 표시되는 RFQ
  const [currentRFQ, setCurrentRFQ] =
    useState<RFQ>(rfq);

  const [draft, setDraft] =
    useState<DraftEmail | null>(null);

  // Edit mode
  const [isEditing, setIsEditing] =
    useState(false);

  const [isSaving, setIsSaving] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  // Edit form
  const [country, setCountry] =
    useState(currentRFQ.country ?? "");

  const [sampleSize, setSampleSize] =
    useState(
      currentRFQ.sample_size?.toString() ?? ""
    );

  const [loi, setLoi] =
    useState(
      currentRFQ.loi?.toString() ?? ""
    );

  const [ir, setIr] =
    useState(
      currentRFQ.ir?.toString() ?? ""
    );

  const handleEdit = () => {
    // 항상 현재 RFQ 값을 기준으로 form 초기화
    setCountry(currentRFQ.country ?? "");

    setSampleSize(
      currentRFQ.sample_size?.toString() ?? ""
    );

    setLoi(
      currentRFQ.loi?.toString() ?? ""
    );

    setIr(
      currentRFQ.ir?.toString() ?? ""
    );

    setError(null);
    setIsEditing(true);
  };

  const handleCancel = () => {
    setError(null);
    setIsEditing(false);
  };

  const handleSave = async () => {
    setIsSaving(true);
    setError(null);

    try {
      const updatedRFQ = await updateRFQ(
        currentRFQ.id,
        {
          country: country.trim(),
          sample_size: Number(sampleSize),
          loi: Number(loi),
          ir: Number(ir),
        }
      );

      setCurrentRFQ(updatedRFQ);
      setIsEditing(false);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to update RFQ."
      );
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      <div className="detail-header">
        <div>
          <p className="eyebrow">
            RFQ Detail
          </p>

          <h1>
            {currentRFQ.project_name ??
              "Untitled Project"}
          </h1>

          <p>RFQ #{currentRFQ.id}</p>
        </div>

        <StatusBadge
          status={currentRFQ.status}
        />
      </div>

      <div className="detail-grid">
        <section className="detail-card">
          <h2>Client</h2>

          <div className="info-row">
            <span>Name</span>

            <strong>
              {currentRFQ.client_name ?? "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Email</span>

            <strong>
              {currentRFQ.client_email ?? "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Company</span>

            <strong>
              {currentRFQ.client ?? "-"}
            </strong>
          </div>
        </section>

        <section className="detail-card">
          <div className="detail-card-header">
            <h2>Project</h2>

            {!isEditing && (
              <button
                type="button"
                onClick={handleEdit}
              >
                Edit
              </button>
            )}
          </div>

          {isEditing ? (
            <>
              <div className="info-row">
                <label htmlFor="country">
                  Country
                </label>

                <input
                  id="country"
                  type="text"
                  value={country}
                  onChange={(event) =>
                    setCountry(event.target.value)
                  }
                />
              </div>

              <div className="info-row">
                <label htmlFor="sample-size">
                  Sample Size
                </label>

                <input
                  id="sample-size"
                  type="number"
                  min="1"
                  value={sampleSize}
                  onChange={(event) =>
                    setSampleSize(
                      event.target.value
                    )
                  }
                />
              </div>

              <div className="info-row">
                <label htmlFor="loi">
                  LOI (minutes)
                </label>

                <input
                  id="loi"
                  type="number"
                  min="1"
                  value={loi}
                  onChange={(event) =>
                    setLoi(event.target.value)
                  }
                />
              </div>

              <div className="info-row">
                <label htmlFor="ir">
                  IR (%)
                </label>

                <input
                  id="ir"
                  type="number"
                  min="0"
                  max="100"
                  value={ir}
                  onChange={(event) =>
                    setIr(event.target.value)
                  }
                />
              </div>

              {error && (
                <p className="edit-error">
                  {error}
                </p>
              )}

              <div className="edit-actions">
                <button
                  type="button"
                  onClick={handleCancel}
                  disabled={isSaving}
                >
                  Cancel
                </button>

                <button
                  type="button"
                  onClick={handleSave}
                  disabled={isSaving}
                >
                  {isSaving
                    ? "Saving..."
                    : "Save Changes"}
                </button>
              </div>
            </>
          ) : (
            <>
              <div className="info-row">
                <span>Country</span>

                <strong>
                  {currentRFQ.country ?? "-"}
                </strong>
              </div>

              <div className="info-row">
                <span>Methodology</span>

                <strong>
                  {currentRFQ.methodology ??
                    "-"}
                </strong>
              </div>

              <div className="info-row">
                <span>Sample Size</span>

                <strong>
                  {currentRFQ.sample_size
                    ? currentRFQ.sample_size.toLocaleString()
                    : "-"}
                </strong>
              </div>

              <div className="info-row">
                <span>LOI</span>

                <strong>
                  {currentRFQ.loi != null
                    ? `${currentRFQ.loi} min`
                    : "-"}
                </strong>
              </div>

              <div className="info-row">
                <span>IR</span>

                <strong>
                  {currentRFQ.ir != null
                    ? `${currentRFQ.ir}%`
                    : "-"}
                </strong>
              </div>

              <div className="info-row">
                <span>Timeline</span>

                <strong>
                  {currentRFQ.timeline ?? "-"}
                </strong>
              </div>
            </>
          )}
        </section>
      </div>

      {currentRFQ.quotation && (
        <QuotationSummary
          quotation={currentRFQ.quotation}
        />
      )}

      <ActionButtons
        rfqId={currentRFQ.id}
        // onDraftGenerated={setDraft}
      />

      <DraftEmailViewer
        draft={draft}
      />
    </>
  );
}