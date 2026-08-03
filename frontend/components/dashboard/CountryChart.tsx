"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface Props {
  countries: Record<string, number>;
}

export default function CountryChart({
  countries,
}: Props) {
  const data = Object.entries(
    countries
  ).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <div className="chart-card">
      <h2>Country Distribution</h2>

      <ResponsiveContainer
        width="100%"
        height={320}
      >
        <BarChart
          layout="vertical"
          data={data}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis type="number" />

          <YAxis
            dataKey="name"
            type="category"
            width={100}
          />

          <Tooltip />

          <Bar
            dataKey="value"
            radius={[8, 8, 8, 8]}
            fill="#175CD3"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}