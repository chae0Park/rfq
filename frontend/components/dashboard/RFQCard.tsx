import Link from "next/link";

import StatusBadge from "./StatusBadge";

import type { RFQ } from "@/types/rfq";

interface Props {
  rfq: RFQ;
}

export default function RFQCard({ rfq }: Props) {
  return (
    <Link
      href={`/rfqs/${rfq.id}`}
      className="rfq-card"
    >
      <div className="rfq-card-header">
        <h3>{rfq.project_name}</h3>

        <StatusBadge
          status={rfq.status}
        />
      </div>

      <div className="rfq-card-content">
        <p>{rfq.client_name}</p>
        <p>{rfq.country}</p>
      </div>
    </Link>
  );
}