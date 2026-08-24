"use client";

import { useRouter } from "next/navigation";

import type { RFQ } from "@/types/rfq";
import StatusBadge from "@/components/dashboard/StatusBadge";

interface RFQTableProps {
  rfqs: RFQ[];
}

export default function RFQTable({
  rfqs,
}: RFQTableProps) {
  const router = useRouter();

  if (rfqs.length === 0) {
    return (
      <div className="empty-state">
        No RFQs found.
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="rfq-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Client</th>
            <th>Project</th>
            <th>Country</th>
            <th>Sample Size</th>
            <th>Total</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {rfqs.map((rfq) => (
            <tr
              key={rfq.id}
              className="rfq-row"
              onClick={() =>
                router.push(`/rfqs/${rfq.id}`)
              }
            >
              <td>#{rfq.id}</td>

              <td>
                <div className="client-cell">
                  <strong>
                    {rfq.client_name ||
                      "Unknown client"}
                  </strong>

                  <span>
                    {rfq.client_email || "-"}
                  </span>
                </div>
              </td>

              <td>
                {rfq.project_name ||
                  "Untitled project"}
              </td>

              <td>{rfq.country || "-"}</td>

              <td>
                {rfq.sample_size
                  ? rfq.sample_size.toLocaleString(
                      "en-US"
                    )
                  : "-"}
              </td>

              <td>
                {rfq.total_cost !== null
                  ? `${rfq.currency} ${rfq.total_cost.toLocaleString(
                      "en-US"
                    )}`
                  : "-"}
              </td>

              <td>
                <StatusBadge
                  status={rfq.status}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}