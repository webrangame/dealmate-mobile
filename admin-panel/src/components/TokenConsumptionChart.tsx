'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

interface TokenConsumer {
  name: string;
  spend: number;
  tokens: number;
}

interface TokenConsumptionChartProps {
  data: TokenConsumer[];
}

export default function TokenConsumptionChart({ data }: TokenConsumptionChartProps) {
  // Sort data by spend just in case, though API should probably do it
  const sortedData = [...data].sort((a, b) => b.spend - a.spend);

  return (
    <div className="w-full h-full min-h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={sortedData}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 40, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="rgba(255,255,255,0.05)" />
          <XAxis 
            type="number" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={(value) => `$${value.toFixed(2)}`}
          />
          <YAxis 
            dataKey="name" 
            type="category" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#9ca3af', fontSize: 12, fontWeight: 500 }}
            width={100}
          />
          <Tooltip 
            cursor={{ fill: 'rgba(255,255,255,0.05)' }}
            contentStyle={{ 
              backgroundColor: 'rgba(17, 24, 39, 0.9)', 
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '12px',
              backdropFilter: 'blur(8px)',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
            }}
            itemStyle={{ fontSize: '12px', fontWeight: 'bold' }}
            labelStyle={{ color: '#e5e7eb', marginBottom: '8px', fontSize: '14px', fontWeight: 'bold' }}
            formatter={(value: any, name: any) => {
              if (name === 'spend') return [`$${Number(value).toFixed(4)}`, 'Estimated Cost'];
              if (name === 'tokens') return [Number(value).toLocaleString(), 'Total Tokens'];
              return [value, name];
            }}
          />
          <Bar 
            dataKey="spend" 
            radius={[0, 4, 4, 0]}
            barSize={20}
            animationDuration={1500}
          >
            {sortedData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={index < 3 ? '#eab308' : '#ca8a04'} fillOpacity={index < 3 ? 1 : 0.7} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
