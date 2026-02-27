'use client';

import { useState, useEffect } from 'react';
import { 
  Users, 
  Bot, 
  TrendingUp, 
  Activity, 
  CreditCard,
  ArrowUpRight,
  Zap,
  Loader2,
  TrendingUp as ChartIcon
} from 'lucide-react';
import RegistrationChart from '@/components/RegistrationChart';
import TokenConsumptionChart from '@/components/TokenConsumptionChart';

interface Stats {
  totalUsers: string;
  totalPurchases: string;
  activeAgents: string;
  tokenUsage: string;
}

import { useRouter } from 'next/navigation';

interface Event {
  type: string;
  text: string;
  time: string;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [registrationData, setRegistrationData] = useState<any[]>([]);
  const [purchaseData, setPurchaseData] = useState<any[]>([]);
  const [tokenConsumptionData, setTokenConsumptionData] = useState<any[]>([]);
  const router = useRouter();

  const fetchStats = async () => {
    setRefreshing(true);
    try {
      const res = await fetch('/api/admin/stats');
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.details || data.error || 'Failed to fetch stats');
      }
      
      setStats(data.stats || null);
      setRegistrationData(data.registrationData || []);
      setPurchaseData(data.purchaseData || []);
      setTokenConsumptionData(data.tokenConsumptionData || []);
      setEvents(data.recentEvents || []);
    } catch (err: any) {
      console.error('Failed to fetch stats:', err.message);
      setEvents([]);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);


  const statCards = [
    { name: 'Total Users', value: stats?.totalUsers || '0', href: '/users', icon: Users, color: 'from-blue-500 to-cyan-400' },
    { name: 'Total Agents Download', value: stats?.totalPurchases || '0', href: '/users', icon: CreditCard, color: 'from-emerald-500 to-teal-400' },
    { name: 'Active Agents', value: stats?.activeAgents || '0', href: '/agents', icon: Bot, color: 'from-purple-500 to-indigo-400' },
    { name: 'Token Usage', value: stats?.tokenUsage || '0', href: '/tokens', icon: Zap, color: 'from-amber-500 to-orange-400' },
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Welcome Section */}
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 mt-1 font-medium">Marketplace performance and identity synchronization metrics.</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={fetchStats}
            disabled={refreshing}
            className="px-4 py-2 bg-primary-500 hover:bg-primary-600 rounded-xl text-sm font-semibold text-white transition-all shadow-lg shadow-primary-500/20 flex items-center gap-2"
          >
            {refreshing ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            System Fresh
          </button>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 glass animate-pulse rounded-2xl" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((stat) => (
            <div key={stat.name} className="glass group hover:bg-white/[0.08] transition-all duration-300 p-6 rounded-2xl relative overflow-hidden">
              <div className={`absolute -right-4 -top-4 w-24 h-24 bg-gradient-to-br ${stat.color} opacity-10 blur-2xl group-hover:opacity-20 transition-opacity`} />
              
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-xl bg-gradient-to-br ${stat.color} shadow-lg shadow-primary-500/10`}>
                  <stat.icon className="w-5 h-5 text-white" />
                </div>
                <div className="flex items-center gap-1 text-primary-400 opacity-0 group-hover:opacity-100 transition-opacity">
                  <span className="text-[10px] font-bold uppercase tracking-widest">Manage</span>
                  <ArrowUpRight className="w-3 h-3" />
                </div>
              </div>
              
              <p className="text-gray-500 text-sm font-medium">{stat.name}</p>
              <div className="flex items-baseline justify-between gap-2 mt-1">
                <h3 className="text-2xl font-bold text-white tracking-tight">{stat.value}</h3>
                <button 
                  onClick={() => router.push(stat.href)}
                  className="p-1.5 rounded-lg bg-white/5 text-gray-500 hover:text-white hover:bg-white/10 transition-all lg:hidden"
                >
                  <ArrowUpRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activity Feed */}
        <div className="lg:col-span-2 glass p-6 rounded-2xl h-[400px] flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <ChartIcon className="w-5 h-5 text-primary-400" />
              <h3 className="text-lg font-bold text-white">Platform Activity Trends (14 Days)</h3>
            </div>
          </div>
          
          <div className="flex-1 border border-dashed border-white/5 rounded-xl bg-white/[0.02] p-4">
            {registrationData.length > 0 || purchaseData.length > 0 ? (
              <RegistrationChart registrationData={registrationData} purchaseData={purchaseData} />
            ) : (
              <div className="h-full flex items-center justify-center text-gray-600 text-sm italic">
                {refreshing ? "Fetching platform trends..." : "No activity data available for the last 14 days."}
              </div>
            )}
          </div>
        </div>

        {/* Token Consumption Chart */}
        <div className="glass p-6 rounded-2xl h-[400px] flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-500" />
              <h3 className="text-lg font-bold text-white">Top Token Consumers</h3>
            </div>
          </div>
          
          <div className="flex-1 border border-dashed border-white/5 rounded-xl bg-white/[0.02] p-4">
             {tokenConsumptionData.length > 0 ? (
               <TokenConsumptionChart data={tokenConsumptionData} />
             ) : (
               <div className="h-full flex items-center justify-center text-gray-600 text-sm italic">
                 {refreshing ? "Fetching token data..." : "No token consumption data available."}
               </div>
             )}
          </div>
        </div>
      </div>

      {/* Registry Stream */}
      <div className="glass p-6 rounded-2xl h-[300px] overflow-hidden flex flex-col">
        <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
          <Activity className="w-5 h-5 text-emerald-400" />
          Registry Stream
        </h3>
        <div className="space-y-4 overflow-y-auto pr-2 flex-1 scrollbar-hide">
          {loading ? (
            [...Array(5)].map((_, i) => <div key={i} className="h-12 bg-white/5 rounded-xl animate-pulse" />)
          ) : events.length === 0 ? (
            <p className="text-center text-gray-600 text-sm italic mt-12">No recent events logged.</p>
          ) : events.map((event, i) => (
            <div key={i} className="flex items-start gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors cursor-pointer group">
              <div className="w-1.5 h-1.5 rounded-full bg-primary-400 mt-2" />
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-200 group-hover:text-primary-400 transition-colors tracking-tight">{event.text}</p>
                <p className="text-[10px] text-gray-600 font-bold uppercase tracking-widest mt-1">
                  {event.type} • {new Date(event.time).toLocaleTimeString()}
                </p>
              </div>
              <ArrowUpRight className="w-4 h-4 text-gray-700 group-hover:text-primary-400 transition-colors" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
