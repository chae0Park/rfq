import {
  getAllLLMLogs,
  getLLMMonitoringSummary,
} from "@/services/dashboard";

import styles from "./monitoring.module.css";
import DashboardNav from "@/components/dashboard/DashboardNav";


export default async function MonitoringPage() {
  const [summary, logs] = await Promise.all([
    getLLMMonitoringSummary(),
    getAllLLMLogs(),
  ]);

  return (
    <main className="dashboard-page">
      <DashboardNav />
      <div className="dashboard-header">
        <div>
          <span className="dashboard-tag">
            LLM Observability
          </span>

          <h1>AI Monitoring</h1>

          <p>
            Monitor LLM usage, latency, token consumption,
            estimated cost and failures.
          </p>
        </div>
      </div>

      <div className={styles.summaryGrid}>
        <div className={styles.card}>
          <span>Total LLM Calls</span>
          <strong>{summary.total_calls}</strong>
        </div>

        <div className={styles.card}>
          <span>Success Rate</span>
          <strong>
            {summary.success_rate.toFixed(1)}%
          </strong>
        </div>

        <div className={styles.card}>
          <span>Total Tokens</span>
          <strong>
            {summary.total_tokens.toLocaleString()}
          </strong>
        </div>

        <div className={styles.card}>
          <span>Estimated Cost</span>
          <strong>
            ${summary.total_estimated_cost.toFixed(6)}
          </strong>
        </div>

        <div className={styles.card}>
          <span>Average Latency</span>
          <strong>
            {(summary.average_latency_ms / 1000).toFixed(2)}s
          </strong>
        </div>
      </div>

      <section className={styles.history}>
        <div className={styles.sectionHeader}>
          <h2>LLM Call History</h2>
          <p>
            Individual AI calls across the RFQ workflow.
          </p>
        </div>

        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>RFQ</th>
                <th>Task</th>
                <th>Model</th>
                <th>Status</th>
                <th>Tokens</th>
                <th>Latency</th>
                <th>Cost</th>
              </tr>
            </thead>

            <tbody>
              {logs.map((log) => {
                const totalTokens =
                  (log.input_tokens ?? 0) +
                  (log.output_tokens ?? 0);

                return (
                  <tr key={log.id}>
                    <td>{log.rfq_id ?? "-"}</td>

                    <td>{log.task_type}</td>

                    <td>{log.model}</td>

                    <td>
                      <span
                        className={`${styles.status} ${
                          log.status === "SUCCESS"
                            ? styles.success
                            : styles.failed
                        }`}
                      >
                        {log.status}
                      </span>
                    </td>

                    <td>
                      {totalTokens.toLocaleString()}
                    </td>

                    <td>
                      {log.latency_ms !== null
                        ? `${(
                            log.latency_ms / 1000
                          ).toFixed(2)}s`
                        : "-"}
                    </td>

                    <td>
                      {log.estimated_cost !== null
                        ? `$${log.estimated_cost.toFixed(6)}`
                        : "-"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

    </main>
  );
}