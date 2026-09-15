"use client";

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function SentimentTrajectoryChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return <div className="h-64 flex items-center justify-center text-slate-500">No data available</div>;

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorPos" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorNeu" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#fbbf24" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#fbbf24" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
          <XAxis 
            dataKey="date" 
            stroke="#94a3b8" 
            fontSize={12}
            tickFormatter={(val) => {
              const d = new Date(val);
              return `${d.toLocaleString('default', { month: 'short' })} ${d.getDate()}`;
            }}
          />
          <YAxis stroke="#94a3b8" fontSize={12} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
            itemStyle={{ fontSize: '14px' }}
            labelStyle={{ color: '#94a3b8', marginBottom: '8px' }}
          />
          <Area type="monotone" dataKey="positive" stroke="#10b981" fillOpacity={1} fill="url(#colorPos)" />
          <Area type="monotone" dataKey="neutral" stroke="#fbbf24" fillOpacity={1} fill="url(#colorNeu)" />
          <Area type="monotone" dataKey="negative" stroke="#ef4444" fillOpacity={1} fill="url(#colorNeg)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
