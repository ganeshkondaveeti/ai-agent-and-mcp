"use client";

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const COLORS = ['#10b981', '#3b82f6']; // Emerald for Android, Blue for iOS

export function StoreEcologyChart({ data }: { data: any }) {
  if (!data || Object.keys(data).length === 0) return <div className="h-64 flex items-center justify-center text-slate-500">No data available</div>;

  const chartData = [
    { name: 'Android', value: data.android?.total_reviews || 0 },
    { name: 'iOS', value: data.ios?.total_reviews || 0 }
  ];

  return (
    <div className="h-[250px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
            itemStyle={{ fontSize: '14px' }}
          />
          <Legend verticalAlign="bottom" height={36}/>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
