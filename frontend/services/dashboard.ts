import type { RFQ } from "@/types/rfq";
import type { DraftEmail } from "@/types/emailDraft";
import type { Activity } from "@/types/activity";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function getRFQs(): Promise<RFQ[]> {
  const response = await fetch(`${API_BASE_URL}/dashboard/rfqs`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch RFQs: ${response.status}`);
  }

  return response.json();
}


export async function getRFQ(id: number): Promise<RFQ> {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/rfqs/${id}`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch RFQ");
  }

  return response.json();
}

export interface ApprovalRequest {
  decision: string;
  reviewer: string;
  comment: string;
}

export async function approveRFQ(
  rfqId: number,
  request: ApprovalRequest
) {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/rfqs/${rfqId}/approve`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to approve RFQ");
  }

  return response.json();
}

export async function rejectRFQ(
  rfqId: number,
  request: ApprovalRequest
) {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/rfqs/${rfqId}/reject`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to reject RFQ");
  }

  return response.json();
}


export async function generateDraftEmail(
  rfqId: number
): Promise<DraftEmail> {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/rfqs/${rfqId}/draft-email`,
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

export async function getActivities(
  rfqId: number
): Promise<Activity[]> {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/rfqs/${rfqId}/activities`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch activities");
  }

  return response.json();
}