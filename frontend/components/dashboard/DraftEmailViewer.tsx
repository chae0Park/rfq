"use client";

import type { DraftEmail } from "@/types/emailDraft";
import { Copy,Download,Mail  } from "lucide-react";

interface DraftEmailViewerProps {
  draft: DraftEmail | null;
}

export default function DraftEmailViewer({
  draft,
}: DraftEmailViewerProps) {
  if (!draft) {
    return null;
  }

  async function copy(text: string) {
    await navigator.clipboard.writeText(text);
  }

  function openGmail() {
    const subject = encodeURIComponent(draft?.subject ?? "");
    const body = encodeURIComponent(draft?.body ?? "");

    window.open(
      `https://mail.google.com/mail/?view=cm&fs=1&su=${subject}&body=${body}`,
      "_blank"
    );
  }


  function downloadDraft() {
    if (!draft) return;

    const content = `Subject

  ${draft.subject}

  ----------------------------------------

  ${draft.body}`;

    const blob = new Blob([content], {
      type: "text/plain;charset=utf-8",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "draft-email.txt";

    link.click();

    URL.revokeObjectURL(url);
  }

  return (
    <section className="detail-card">
      <h2>Draft Email Preview</h2>

      <div className="draft-section">
        <label>Subject</label>

        <div className="draft-box">
          <div className="draft-toolbar">
            <button
              onClick={() => copy(draft.subject)}
            >
              <Copy size={16} />
              Copy
            </button>
          </div>

          {draft.subject}
        </div>
      </div>

      <div className="draft-section">
        <label>Body</label>

        <div className="draft-box draft-body">
          <div className="draft-toolbar">
            <button
              onClick={() => copy(draft.body)}
            >
              <Copy size={16} />
              Copy
            </button>
          </div>

          {draft.body}
        </div>
      </div>

      <div className="draft-actions">
        <button
            className="download-button"
            onClick={downloadDraft}
        >
            <Download size={18} />
            Download
        </button>

        <button
            className="gmail-button"
            onClick={openGmail}
        >
            <Mail size={18} />
            Open Gmail
        </button>
      </div>
    </section>
  );
}