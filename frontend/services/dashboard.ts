import type { RFQ } from "@/types/rfq";
import type { DraftEmail } from "@/types/emailDraft";
import type { Activity } from "@/types/activity";


// ============================================================
// API URLs
// ============================================================

// Browser(Client Component) → FastAPI
// Local: http://localhost:8000
// Production: Railway URL
const PUBLIC_API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

// Next.js Server Component → FastAPI
// Docker 내부에서는 backend라는 service name으로 접근
const INTERNAL_API_BASE_URL =
  process.env.INTERNAL_API_BASE_URL ??
  "http://backend:8000";


// ============================================================
// RFQ List
// Server Component
// ============================================================

export async function getRFQs(): Promise<RFQ[]> {
  const response = await fetch(
    `${INTERNAL_API_BASE_URL}/dashboard/rfqs`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch RFQs: ${response.status}`
    );
  }

  return response.json();
}


// ============================================================
// RFQ Detail
// Server Component
// ============================================================

export async function getRFQ(id: number): Promise<RFQ> {
  const response = await fetch(
    `${INTERNAL_API_BASE_URL}/dashboard/rfqs/${id}`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    }
  );

  if (!response.ok) {
    const errorBody = await response.text();

    throw new Error(
      `Failed to fetch RFQ (${response.status}): ${errorBody}`
    );
  }

  return response.json();
}


// ============================================================
// Approval
// Client Component
// ============================================================

export interface ApprovalRequest {
  decision: "APPROVE" | "REJECT";
  reviewer: string;
  comment: string;
}


export async function approveRFQ(
  rfqId: number,
  request: ApprovalRequest
) {
  const response = await fetch(
    `${PUBLIC_API_BASE_URL}/dashboard/rfqs/${rfqId}/approve`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    const errorBody = await response
      .json()
      .catch(() => null);

    throw new Error(
      errorBody?.detail ??
        `Failed to approve RFQ: ${response.status}`
    );
  }

  return response.json();
}


// ============================================================
// Reject
// Client Component
// ============================================================

export async function rejectRFQ(
  rfqId: number,
  request: ApprovalRequest
) {
  const response = await fetch(
    `${PUBLIC_API_BASE_URL}/dashboard/rfqs/${rfqId}/reject`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    const errorBody = await response
      .json()
      .catch(() => null);

    throw new Error(
      errorBody?.detail ??
        `Failed to reject RFQ: ${response.status}`
    );
  }

  return response.json();
}


// ============================================================
// Generate Draft Email
// Client Component
// ============================================================

export async function generateDraftEmail(
  rfqId: number
): Promise<DraftEmail> {
  const response = await fetch(
    `${PUBLIC_API_BASE_URL}/dashboard/rfqs/${rfqId}/draft-email`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
    }
  );

  if (!response.ok) {
    const errorBody = await response
      .json()
      .catch(() => null);

    throw new Error(
      errorBody?.detail ??
        `Failed to generate draft email: ${response.status}`
    );
  }

  return response.json();
}


// ============================================================
// Activities
// Server Component
// ============================================================

export async function getActivities(
  rfqId: number
): Promise<Activity[]> {
  const response = await fetch(
    `${INTERNAL_API_BASE_URL}/dashboard/rfqs/${rfqId}/activities`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch activities: ${response.status}`
    );
  }

  return response.json();
}