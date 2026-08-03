"use client";

import type { DraftEmail } from "@/types/emailDraft";

interface DraftEmailViewerProps {
  draft: DraftEmail | null;
}

export default function DraftEmailViewer({
  draft,
}: DraftEmailViewerProps) {
  if (!draft) {
    return null;
  }

  return (
    <section className="detail-card">
      <h2>Draft Email Preview</h2>

      <div className="draft-section">
        <label>Subject</label>

        <div className="draft-box">
          {draft.subject}
        </div>
      </div>

      <div className="draft-section">
        <label>Body</label>

        <div className="draft-box draft-body">
          {draft.body}
        </div>
      </div>
    </section>
  );
}