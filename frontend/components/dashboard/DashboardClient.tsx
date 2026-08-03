"use client";

import { useMemo, useState } from "react";

import KPICards from "./KPICards";
import RFQTable from "./RFQTable";
import SearchBar from "./SearchBar";
import StatusFilter from "./StatusFilter";
import StatusChart from "./StatusChart";
import CountryChart from "./CountryChart";

import type { RFQ } from "@/types/rfq";

interface Props {
  rfqs: RFQ[];
}

export default function DashboardClient({
  rfqs,
}: Props) {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("ALL");

  const filtered = useMemo(() => {
    return rfqs.filter((rfq) => {
      const keyword =
        search.toLowerCase();

      const matchedKeyword =
        (rfq.client_name ?? "")
          .toLowerCase()
          .includes(keyword) ||
        (rfq.project_name ?? "")
          .toLowerCase()
          .includes(keyword);

      const matchedStatus =
        status === "ALL" ||
        rfq.status === status;

      return (
        matchedKeyword &&
        matchedStatus
      );
    });
  }, [rfqs, search, status]);

  const approved = filtered.filter(
    (rfq) =>
      rfq.status === "APPROVED"
  ).length;


  const countries: Record<string, number> = {};

  filtered.forEach((rfq) => {
    const key = rfq.country ?? "Unknown";

    countries[key] =
      (countries[key] ?? 0) + 1;
  });


  const rejected = filtered.filter(
    (rfq) =>
      rfq.status === "REJECTED"
  ).length;

  return (
    <>
      <KPICards
        total={filtered.length}
        approved={approved}
        rejected={rejected}
        pending={
          filtered.length -
          approved -
          rejected
        }
      />

      <div className="dashboard-toolbar">
        <SearchBar
          value={search}
          onChange={setSearch}
        />

        <StatusFilter
          value={status}
          onChange={setStatus}
        />
      </div>

      <div className="chart-grid">
        
      <StatusChart
        approved={approved}
        rejected={rejected}
        pending={
          filtered.length -
          approved -
          rejected
        }
      />

      <CountryChart
        countries={countries}
      />
    </div>

      <RFQTable
        rfqs={filtered}
      />
    </>
  );
}