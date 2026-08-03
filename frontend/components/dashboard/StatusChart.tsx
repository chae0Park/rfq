"use client";

import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface Props {
  approved: number;
  rejected: number;
  pending: number;
}

const COLORS = [
  "#12B76A",
  "#F04438",
  "#F79009",
];

export default function StatusChart({
  approved,
  rejected,
  pending,
}: Props) {
  const data = [
    {
      name: "Approved",
      value: approved,
    },
    {
      name: "Rejected",
      value: rejected,
    },
    {
      name: "Pending",
      value: pending,
    },
  ];

  return (
    <div className="chart-card">
      <h2>Status Distribution</h2>

      <ResponsiveContainer
        width="100%"
        height={320}
      >
        <PieChart>
          <Pie
            data={data}
            innerRadius={70}
            outerRadius={105}
            dataKey="value"
            paddingAngle={4}
          >
            {data.map((_, index) => (
              <Cell
                key={index}
                fill={COLORS[index]}
              />
            ))}
          </Pie>

          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}