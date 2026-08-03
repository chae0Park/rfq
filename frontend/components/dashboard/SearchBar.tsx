"use client";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

export default function SearchBar({
  value,
  onChange,
}: SearchBarProps) {
  return (
    <input
      className="search-input"
      type="text"
      placeholder="Search client or project..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}