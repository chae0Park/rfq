import {
  CheckCircle2,
  Clock3,
  FileText,
  XCircle,
} from "lucide-react";

interface KPICardsProps {
  total: number;
  approved: number;
  rejected: number;
  pending: number;
}

export default function KPICards({
  total,
  approved,
  rejected,
  pending,
}: KPICardsProps) {
  const cards = [
    {
      title: "Total RFQs",
      value: total,
      icon: <FileText size={22} />,
      className: "blue",
    },
    {
      title: "Approved",
      value: approved,
      icon: <CheckCircle2 size={22} />,
      className: "green",
    },
    {
      title: "Rejected",
      value: rejected,
      icon: <XCircle size={22} />,
      className: "red",
    },
    {
      title: "Pending",
      value: pending,
      icon: <Clock3 size={22} />,
      className: "orange",
    },
  ];

  return (
    <section className="kpi-grid">
      {cards.map((card) => (
        <div
          key={card.title}
          className={`kpi-card ${card.className}`}
        >
          <div className="kpi-header">
            <div className="kpi-icon">
              {card.icon}
            </div>

            <span>{card.title}</span>
          </div>

          <h2>{card.value}</h2>
        </div>
      ))}
    </section>
  );
}