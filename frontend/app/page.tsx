import DashboardClient from "@/components/dashboard/DashboardClient";
import { getRFQs } from "@/services/dashboard";
import DashboardNav from "@/components/dashboard/DashboardNav";


export default async function DashboardPage() {
  const rfqs = await getRFQs();

  return (
    <main className="dashboard-page">
      <DashboardNav />
      <div className="dashboard-header">
        <div>
          <span className="dashboard-tag">
            AI Operations Platform
          </span>

          <h1>PromptOps Dashboard</h1>

          <p>
            AI-powered RFQ extraction, quotation,
            approval and draft email generation.
          </p>
        </div>

        <div className="dashboard-summary">
          <div className="summary-number">
            {rfqs.length}
          </div>

          <span>Total RFQs</span>
        </div>
      </div>

      <DashboardClient
        rfqs={rfqs}
      />
    </main>
  );
}