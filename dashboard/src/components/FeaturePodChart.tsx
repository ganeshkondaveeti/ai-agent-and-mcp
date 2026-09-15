"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export function FeaturePodChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return <div className="h-64 flex items-center justify-center text-slate-500">No data available</div>;

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 20, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={true} vertical={false} />
          <XAxis type="number" stroke="#94a3b8" fontSize={12} />
          <YAxis dataKey="pod_name" type="category" stroke="#94a3b8" fontSize={12} width={120} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
            itemStyle={{ fontSize: '14px' }}
            cursor={{ fill: '#334155', opacity: 0.4 }}
          />
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          <Bar dataKey="positive" name="Positive" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} />
          <Bar dataKey="negative" name="Negative" stackId="a" fill="#ef4444" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
