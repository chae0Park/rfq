import RFQTable from "@/components/dashboard/RFQTable";
import { getRFQs } from "@/services/dashboard";

export default async function DashboardPage() {
  const rfqs = await getRFQs();

  return (
    <main className="dashboard-page">
      <section className="dashboard-header">
        <div>
          <p className="eyebrow">AI Operations</p>
          <h1>RFQ Dashboard</h1>
          <p className="dashboard-description">
            Review extracted RFQs and manage quotation workflows.
          </p>
        </div>

        <div className="summary-card">
          <span>Total RFQs</span>
          <strong>{rfqs.length}</strong>
        </div>
      </section>

      <section className="dashboard-card">
        <div className="card-header">
          <div>
            <h2>RFQ Requests</h2>
            <p>Recently received client requests</p>
          </div>
        </div>

        <RFQTable rfqs={rfqs} />
      </section>
    </main>
  );
}