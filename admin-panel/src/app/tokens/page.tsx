'use client';

import { useState, useEffect } from 'react';
import { 
  Zap, 
  Search, 
  RefreshCw,
  TrendingUp,
  CreditCard,
  Target,
  Users,
  Loader2,
  Shield,
  ArrowUpRight,
  ExternalLink
} from 'lucide-react';

interface LiteLLMUser {
  user_id: string;
  user_email?: string;
  user_alias?: string;
  spend: number;
  max_budget: number;
  total_tokens?: number;
  tpm_limit?: number;
  rpm_limit?: number;
  models?: string[];
}

export default function TokensPage() {
  const [usage, setUsage] = useState<LiteLLMUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [error, setError] = useState('');

  const fetchTokenStats = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/admin/tokens');
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.details || data.error || 'Failed to fetch token usage');
      }
      
      setUsage(data.usage || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTokenStats();
  }, []);

  const filteredUsage = usage.filter(u => 
    u.user_id.toLowerCase().includes(search.toLowerCase()) || 
    (u.user_email && u.user_email.toLowerCase().includes(search.toLowerCase())) ||
    (u.user_alias && u.user_alias.toLowerCase().includes(search.toLowerCase()))
  );

  const totalSpend = usage.reduce((acc, curr) => acc + (curr.spend || 0), 0);
  const totalBudget = usage.reduce((acc, curr) => acc + (curr.max_budget || 0), 0);
  const totalTokens = usage.reduce((acc, curr) => acc + (curr.total_tokens || 0), 0);

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header section */}
      <div className="flex items-end justify-between">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            <h2 className="text-xl font-bold text-white uppercase tracking-wider">Token Analytics</h2>
          </div>
          <p className="text-gray-500 font-medium tracking-tight">Real-time expenditure and resource allocation from LiteLLM Proxy.</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={fetchTokenStats}
            disabled={loading}
            className="px-4 py-2.5 bg-white/5 border border-white/5 rounded-xl text-sm font-bold text-gray-400 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Global Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { label: 'Cumulative Spend', value: `$${totalSpend.toFixed(2)}`, icon: CreditCard, color: 'emerald' },
          { label: 'Budget Allocation', value: `$${totalBudget.toFixed(2)}`, icon: Target, color: 'indigo' },
          { label: 'Active Consumers', value: usage.length, icon: Users, color: 'yellow' },
        ].map((stat, i) => (
          <div key={i} className="glass rounded-3xl p-6 border-0 group hover:bg-white/[0.04] transition-all duration-500 overflow-hidden relative">
            <div className={`absolute top-0 right-0 w-24 h-24 bg-${stat.color}-500/10 blur-3xl -mr-8 -mt-8 rounded-full group-hover:scale-150 transition-transform duration-700`}></div>
            <div className={`w-12 h-12 rounded-2xl bg-${stat.color}-500/10 border border-${stat.color}-500/20 flex items-center justify-center mb-4`}>
              <stat.icon className={`w-6 h-6 text-${stat.color}-400`} />
            </div>
            <p className="text-gray-500 text-[10px] font-bold uppercase tracking-widest mb-1">{stat.label}</p>
            <h3 className="text-2xl font-black text-white tracking-tight">{stat.value}</h3>
          </div>
        ))}
      </div>

      {/* Search Toolbar */}
      <div className="flex items-center gap-4">
        <div className="flex-1 relative group">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-yellow-500 transition-colors" />
          <input 
            type="text" 
            placeholder="Filter by User ID, Email or Alias..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-12 glass border-0 rounded-2xl pl-12 pr-4 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/20 transition-all placeholder:text-gray-600 font-medium"
          />
        </div>
      </div>

      {/* Error handling */}
      {error && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-500 text-sm font-bold flex items-center gap-2">
          <Shield className="w-4 h-4" />
          {error}
        </div>
      )}

      {/* Token Usage Table */}
      <div className="glass rounded-3xl overflow-hidden border-0">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/[0.03] border-b border-white/[0.05]">
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Internal Identity</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Financials</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-center">Utilization</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-center">Remaining</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.04]">
            {loading && usage.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center">
                  <div className="flex flex-col items-center gap-3">
                    <Loader2 className="w-8 h-8 text-yellow-500 animate-spin" />
                    <p className="text-xs font-bold text-gray-500 uppercase tracking-widest">Polling Proxy Nodes...</p>
                  </div>
                </td>
              </tr>
            ) : filteredUsage.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-500 text-sm italic font-medium">
                  No token usage records found.
                </td>
              </tr>
            ) : filteredUsage.map((user) => {
              const spend = user.spend || 0;
              const budget = user.max_budget || 0;
              const capPercentage = (spend / (budget || 0.01)) * 100;
              // Conversion: $0.25 = 5M tokens -> $1 = 20M tokens
              const remainingBudget = Math.max(0, budget - spend);
              const remainingTokens = Math.floor(remainingBudget * 20000000);
              
              return (
                <tr key={user.user_id} className="group hover:bg-white/[0.02] transition-colors">
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-xl bg-yellow-500/10 border border-white/5 flex items-center justify-center">
                        <TrendingUp className="w-5 h-5 text-yellow-500" />
                      </div>
                      <div>
                        <p className="text-sm font-bold text-white group-hover:text-yellow-400 transition-colors tracking-tight leading-none">
                          {user.user_alias || user.user_id}
                        </p>
                        <p className="text-[11px] text-gray-500 font-bold uppercase tracking-widest mt-1.5 leading-none">
                          {user.user_email || 'No email attached'}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex flex-col gap-1.5">
                      <div className="flex justify-between items-end w-40">
                        <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Spend/Cap</span>
                        <span className="text-[10px] font-bold text-white">${spend.toFixed(4)} / ${budget.toFixed(2)}</span>
                      </div>
                      <div className="w-40 h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div 
                          className={`h-full transition-all duration-1000 ${capPercentage > 80 ? 'bg-red-500' : 'bg-yellow-500'}`}
                          style={{ width: `${Math.min(capPercentage, 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-5 text-center">
                    <p className="text-sm font-black text-white leading-none">{(user.total_tokens || 0).toLocaleString()}</p>
                    <p className="text-[8px] text-gray-600 font-black uppercase tracking-widest mt-1 leading-none">Total Tokens</p>
                  </td>
                  <td className="px-6 py-5 text-center">
                    <p className={`text-sm font-black leading-none ${remainingTokens < 1000000 ? 'text-red-400' : 'text-emerald-400'}`}>
                      {remainingTokens.toLocaleString()}
                    </p>
                    <p className="text-[8px] text-gray-600 font-black uppercase tracking-widest mt-1 leading-none">Available</p>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
