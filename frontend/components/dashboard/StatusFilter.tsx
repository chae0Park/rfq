"use client";

interface StatusFilterProps {
  value: string;
  onChange: (value: string) => void;
}

const options = [
  "ALL",
  "RECEIVED",
  "VALIDATED",
  "QUOTED",
  "PRICE_REVIEWED",
  "APPROVED",
  "REJECTED",
];

export default function StatusFilter({
  value,
  onChange,
}: StatusFilterProps) {
  return (
    <select
      className="status-filter"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      {options.map((option) => (
        <option
          key={option}
          value={option}
        >
          {option}
        </option>
      ))}
    </select>
  );
}