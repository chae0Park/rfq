// const BASE_URL = "http://localhost:8000";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function getRFQs() {
  const response = await fetch(`${BASE_URL}/dashboard/rfqs`);

  if (!response.ok) {
    throw new Error("Failed to fetch RFQs");
  }

  return response.json();
}

export async function getRFQ(rfqId: number) {
  const response = await fetch(`${BASE_URL}/dashboard/rfqs/${rfqId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch RFQ");
  }

  return response.json();
}