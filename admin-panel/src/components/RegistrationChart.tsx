'use client';

import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts';

interface TimeData {
  date: string;
  count: string | number;
}

interface TrendsChartProps {
  registrationData: TimeData[];
  purchaseData: TimeData[];
}

export default function TrendsChart({ registrationData, purchaseData }: TrendsChartProps) {
  // Create a combined data map for all unique dates
  const dataMap: Record<string, { name: string, registrations: number, downloads: number, date: string }> = {};

  // Process registrations
  registrationData.forEach(item => {
    const formattedDate = new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    dataMap[item.date] = {
      name: formattedDate,
      registrations: Number(item.count),
      downloads: 0,
      date: item.date
    };
  });

  // Process purchases
  purchaseData.forEach(item => {
    const formattedDate = new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    if (dataMap[item.date]) {
      dataMap[item.date].downloads = Number(item.count);
    } else {
      dataMap[item.date] = {
        name: formattedDate,
        registrations: 0,
        downloads: Number(item.count),
        date: item.date
      };
    }
  });

  // Convert map to sorted array
  const combinedData = Object.values(dataMap).sort((a, b) => a.date.localeCompare(b.date));

  return (
    <div className="w-full h-full min-h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={combinedData}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorRegistrations" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorDownloads" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
          <XAxis 
            dataKey="name" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 12 }}
            dy={10}
          />
          <YAxis 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 12 }}
            dx={-10}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'rgba(17, 24, 39, 0.8)', 
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '12px',
              backdropFilter: 'blur(8px)',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
            }}
            itemStyle={{ fontSize: '12px', fontWeight: 'bold' }}
            labelStyle={{ color: '#9ca3af', marginBottom: '8px', fontSize: '14px' }}
          />
          <Legend 
            verticalAlign="top" 
            height={36} 
            iconType="circle"
            formatter={(value) => <span className="text-gray-400 text-xs font-semibold uppercase tracking-wider">{value}</span>}
          />
          <Area 
            type="monotone" 
            name="Registrations"
            dataKey="registrations" 
            stroke="#3b82f6" 
            strokeWidth={3}
            fillOpacity={1} 
            fill="url(#colorRegistrations)" 
            animationDuration={1500}
          />
          <Area 
            type="monotone" 
            name="Downloads"
            dataKey="downloads" 
            stroke="#10b981" 
            strokeWidth={3}
            fillOpacity={1} 
            fill="url(#colorDownloads)" 
            animationDuration={1500}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
