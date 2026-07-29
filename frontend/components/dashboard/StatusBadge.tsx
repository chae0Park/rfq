interface StatusBadgeProps {
  status: string;
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const normalizedStatus = status?.toUpperCase() || "UNKNOWN";

  return (
    <span className={`status-badge status-${normalizedStatus.toLowerCase()}`}>
      {normalizedStatus}
    </span>
  );
}