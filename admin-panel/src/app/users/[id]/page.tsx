'use client';

import { useState, useEffect, use } from 'react';
import Link from 'next/link';
import { 
  User, 
  ArrowLeft, 
  Mail, 
  Shield, 
  Calendar, 
  Zap, 
  Bot, 
  History,
  TrendingUp,
  ExternalLink,
  Lock,
  MessageSquare,
  Loader2,
  AlertCircle
} from 'lucide-react';

interface UserDetail {
  user: {
    id: number;
    name: string;
    email: string;
    joined: string;
    status: string;
  };
  purchases: Array<{
    id: string;
    name: string;
    purchasedAt: string;
  }>;
  tokenInfo: {
    spend: string;
    rawSpend: number;
    totalTokens: number;
    budget: number;
  } | null;
}

export default function UserDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [data, setData] = useState<UserDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState('');

  const fetchDetail = async () => {
    try {
      const res = await fetch(`/api/admin/users/${id}`);
      if (!res.ok) throw new Error('Failed to fetch user details');
      const detail = await res.json();
      setData(detail);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetail();
  }, [id]);

  const toggleStatus = async () => {
    if (!data) return;
    const newStatus = data.user.status === 'active' ? 'inactive' : 'active';
    if (!confirm(`Are you sure you want to set this user to ${newStatus}?`)) return;

    setUpdating(true);
    try {
      const res = await fetch(`/api/admin/users/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      if (res.ok) {
        await fetchDetail();
      } else {
        alert('Failed to update status');
      }
    } catch (err) {
      alert('Error updating status');
    } finally {
      setUpdating(false);
    }
  };

  const handleModify = () => {
    alert('Modification Interface Restricted: Profile updates for participants are handled through the decentralized Identity provider. Direct overrides are temporarily locked.');
  };

  const handleAccountAction = (action: string) => {
    alert(`${action} triggered for ${data?.user.name}. Communication with Identity Stream initiated...`);
  };

  if (loading) {
    return (
      <div className="h-full flex flex-col items-center justify-center space-y-4 animate-pulse">
        <Loader2 className="w-12 h-12 text-primary-500 animate-spin" />
        <p className="text-xs font-bold text-gray-500 uppercase tracking-widest">Compiling user records...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="h-full flex flex-col items-center justify-center space-y-4">
        <AlertCircle className="w-12 h-12 text-red-500" />
        <p className="text-sm font-bold text-gray-400">{error || 'User not found'}</p>
        <Link href="/users" className="text-xs font-bold text-primary-400 uppercase tracking-widest hover:underline">Back to Directory</Link>
      </div>
    );
  }

  const { user, purchases, tokenInfo } = data;

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Navigation & Header */}
      <div className="flex items-center justify-between">
        <Link 
          href="/users" 
          className="flex items-center gap-2 text-gray-400 hover:text-white transition-all group"
        >
          <div className="p-2 rounded-xl bg-white/5 group-hover:bg-white/10 transition-all border border-white/5">
             <ArrowLeft className="w-4 h-4" />
          </div>
          <span className="text-sm font-bold uppercase tracking-widest">Registry Backlink</span>
        </Link>
        <div className="flex gap-3">
           <button 
            onClick={toggleStatus}
            disabled={updating}
            className={`px-4 py-2 border rounded-xl text-xs font-bold uppercase tracking-widest transition-all flex items-center gap-2 ${
              user.status === 'active' 
                ? 'bg-red-500/10 text-red-500 border-red-500/20 hover:bg-red-500/20' 
                : 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20 hover:bg-emerald-500/20'
            }`}
           >
            {updating ? <Loader2 className="w-3 h-3 animate-spin" /> : null}
            {user.status === 'active' ? 'Revoke Access' : 'Enable Access'}
           </button>
           <button 
            onClick={handleModify}
            className="px-4 py-2 bg-white/5 border border-white/5 rounded-xl text-xs font-bold uppercase tracking-widest hover:bg-white/10 transition-all text-gray-400"
           >
            Modify Record
           </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Sidebar */}
        <div className="space-y-6">
          <div className="glass p-8 rounded-3xl text-center relative overflow-hidden">
             <div className="absolute inset-0 bg-gradient-to-br from-primary-500 to-indigo-600 opacity-5 blur-3xl -z-10" />
             <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-primary-400 to-indigo-600 mx-auto mb-6 p-1">
                <div className="w-full h-full rounded-[22px] bg-admin-bg flex items-center justify-center font-bold text-3xl text-white">
                  {user.name.charAt(0)}
                </div>
             </div>
             <h2 className="text-2xl font-bold text-white tracking-tight leading-none">{user.name}</h2>
             <div className="flex items-center justify-center gap-1 mt-2 mb-6">
                <Mail className="w-3.5 h-3.5 text-gray-600" />
                <span className="text-xs text-gray-500 font-medium">{user.email}</span>
             </div>
             
             <div className="p-4 rounded-2xl bg-white/[0.03] space-y-4">
                <div className="flex items-center justify-between">
                   <div className="flex items-center gap-2">
                     <Shield className="w-4 h-4 text-primary-400" />
                     <span className="text-xs font-bold text-gray-400 uppercase tracking-tight">ID</span>
                   </div>
                   <span className="text-xs font-black text-white uppercase tracking-widest">#{user.id}</span>
                </div>
                <div className="flex items-center justify-between">
                   <div className="flex items-center gap-2">
                     <Calendar className="w-4 h-4 text-primary-400" />
                     <span className="text-xs font-bold text-gray-400 uppercase tracking-tight">Joined</span>
                   </div>
                   <span className="text-xs font-bold text-gray-300">
                     {new Date(user.joined).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                   </span>
                </div>
                <div className="flex items-center justify-between">
                   <div className="flex items-center gap-2">
                     <History className="w-4 h-4 text-primary-400" />
                     <span className="text-xs font-bold text-gray-400 uppercase tracking-tight">Status</span>
                   </div>
                   <span className={`px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-500 text-[9px] font-black uppercase tracking-widest ${user.status === 'active' ? 'text-emerald-500' : 'text-red-500'}`}>
                     {user.status}
                   </span>
                </div>
             </div>
          </div>

          <div className="glass p-6 rounded-3xl space-y-4">
             <h3 className="text-sm font-bold text-white uppercase tracking-widest px-2">Account Actions</h3>
              <div className="space-y-1">
                 {[
                   { icon: Lock, text: 'Reset Identity', color: 'hover:text-amber-400' },
                   { icon: Zap, text: 'Audit Tokens', color: 'hover:text-primary-400' },
                   { icon: MessageSquare, text: 'Direct Comm', color: 'hover:text-indigo-400' },
                 ].map((action, i) => (
                   <button
                    key={i}
                    onClick={() => handleAccountAction(action.text)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/5 transition-all text-gray-500 ${action.color} group`}
                   >
                     <action.icon className="w-4 h-4 transition-transform group-hover:scale-110" />
                     <span className="text-sm font-semibold">{action.text}</span>
                   </button>
                 ))}
              </div>
          </div>
        </div>

        {/* Analytics & Lists */}
        <div className="lg:col-span-2 space-y-6">
          {/* Spend Analytics */}
          <div className="glass p-8 rounded-3xl relative overflow-hidden">
             <div className="absolute right-0 top-0 w-32 h-32 bg-primary-500/10 blur-[80px]" />
             <div className="flex items-end justify-between mb-8">
                <div>
                   <div className="flex items-center gap-2 mb-1">
                      <TrendingUp className="w-5 h-5 text-emerald-400" />
                      <h3 className="text-lg font-bold text-white tracking-tight">LiteLLM Analytics</h3>
                   </div>
                   <p className="text-xs text-gray-500 font-medium">Real-time expenditure and usage traffic</p>
                </div>
                <p className="text-3xl font-black text-white tracking-tighter">{tokenInfo?.spend || '$0.00'}</p>
             </div>

             <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                 {[
                   { label: 'Total Events', value: tokenInfo?.totalTokens?.toLocaleString() || '0', color: 'text-primary-400' },
                   { label: 'Max Budget', value: tokenInfo?.budget ? `$${tokenInfo.budget}` : 'Unlimited', color: 'text-indigo-400' },
                   { 
                     label: 'Remaining', 
                     value: tokenInfo ? Math.floor(Math.max(0, (tokenInfo.budget || 0) - (tokenInfo.rawSpend || 0)) * 20000000).toLocaleString() : '0', 
                     color: 'text-emerald-400' 
                   },
                   { label: 'Traffic Hub', value: 'Live', color: 'text-emerald-400' },
                 ].map((metric, i) => (
                   <div key={i} className="bg-white/[0.02] border border-white/5 p-4 rounded-2xl">
                      <p className="text-[10px] font-bold text-gray-600 uppercase tracking-widest mb-1">{metric.label}</p>
                      <p className={`text-xl font-bold ${metric.color}`}>{metric.value}</p>
                   </div>
                 ))}
             </div>
          </div>

          {/* Agent Library */}
          <div className="glass p-8 rounded-3xl">
             <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                   <Bot className="w-5 h-5 text-indigo-400" />
                   <h3 className="text-lg font-bold text-white tracking-tight">Purchased Agents</h3>
                </div>
                <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">{purchases.length} Items</span>
             </div>

             <div className="space-y-3">
                {purchases.length === 0 ? (
                  <div className="p-8 text-center border border-dashed border-white/5 rounded-2xl bg-white/[0.01]">
                    <p className="text-gray-600 text-sm italic font-medium">No agents purchased by this user.</p>
                  </div>
                ) : purchases.map((agent) => (
                  <div key={agent.id} className="flex items-center justify-between p-4 rounded-2xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-all group cursor-pointer">
                     <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center border border-white/5">
                           <Bot className="w-6 h-6 text-indigo-400" />
                        </div>
                        <div>
                           <p className="font-bold text-white group-hover:text-primary-400 transition-colors">{agent.name}</p>
                           <p className="text-[10px] text-gray-600 font-bold uppercase tracking-widest mt-0.5">
                             Acquired {new Date(agent.purchasedAt).toLocaleDateString()}
                           </p>
                        </div>
                     </div>
                     <button className="p-2 rounded-lg bg-white/5 text-gray-600 hover:text-white hover:bg-white/10 transition-all">
                        <ExternalLink className="w-4 h-4" />
                     </button>
                  </div>
                ))}
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
