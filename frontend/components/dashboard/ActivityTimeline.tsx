import type { Activity } from "@/types/activity";

interface Props {
  activities: Activity[];
}

export default function ActivityTimeline({
  activities,
}: Props) {
  return (
    <section className="detail-card">
      <h2>Activity</h2>

      <div className="timeline">
        {activities.map((activity) => (
          <div
            key={activity.id}
            className="timeline-item"
          >
            <div className="timeline-dot" />

            <div className="timeline-content">
              <strong>{activity.type}</strong>

              <p>{activity.message}</p>

              <span>
                {new Date(
                  activity.created_at
                ).toLocaleString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}