'use client';

import { useState, useEffect } from 'react';
import {
  Bot,
  Search,
  Filter,
  RefreshCw,
  Plus,
  ArrowUpRight,
  Shield,
  Tag,
  DollarSign,
  Layers,
  Loader2,
  Eye,
  EyeOff,
  Upload
} from 'lucide-react';

interface Agent {
  id: string;
  slug: string;
  name: string;
  description: string;
  category: string;
  version: string;
  author: string;
  price: number;
  pricingModel: string;
  usageCount: number;
  isVisible: boolean;
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [error, setError] = useState('');
  const [syncing, setSyncing] = useState(false);

  const fetchAgents = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/admin/agents');
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.details || data.error || 'Failed to fetch agents');
      }

      setAgents(data.agents || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSync = async () => {
    setSyncing(true);
    setError('');
    try {
      const res = await fetch('/api/admin/agents/sync', { method: 'POST' });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.details || data.error || 'Failed to sync agents');
      }

      await fetchAgents();
      alert('S3 Registry synced with Database successfully!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSyncing(false);
    }
  };

  const handleVisibilityToggle = async (slug: string, currentVisibility: boolean) => {
    try {
      const res = await fetch('/api/admin/agents/visibility', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ slug, isVisible: !currentVisibility })
      });

      if (!res.ok) throw new Error('Failed to toggle visibility');

      setAgents(prev => prev.map(a => a.slug === slug ? { ...a, isVisible: !currentVisibility } : a));
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.zip')) {
      setError('Please upload a ZIP file');
      return;
    }

    setSyncing(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch('/api/admin/agents/upload', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.details || data.error || 'Upload failed');

      alert('Agent uploaded and registered successfully!');
      fetchAgents();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSyncing(false);
      // Reset input
      e.target.value = '';
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const filteredAgents = agents.filter(agent =>
    agent.name.toLowerCase().includes(search.toLowerCase()) ||
    agent.slug?.toLowerCase().includes(search.toLowerCase()) ||
    agent.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header section */}
      <div className="flex items-end justify-between">
        <div>
          <p className="text-gray-500 font-medium tracking-tight">Direct registry of all AI entities stored in marketplace database.</p>
        </div>
        <div className="flex gap-3">
          <label className="px-4 py-2.5 bg-primary-500/10 border border-primary-500/20 rounded-xl text-sm font-bold text-primary-400 hover:text-white hover:bg-primary-500/20 transition-all flex items-center gap-2 cursor-pointer">
            <Upload className="w-4 h-4" />
            Add New Agent (ZIP)
            <input
              type="file"
              accept=".zip"
              onChange={handleUpload}
              className="hidden"
              disabled={syncing || loading}
            />
          </label>
          <button
            onClick={handleSync}
            disabled={syncing || loading}
            className="px-4 py-2.5 bg-white/5 border border-white/5 rounded-xl text-sm font-bold text-gray-400 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${syncing ? 'animate-spin' : ''}`} />
            {syncing ? 'Syncing...' : 'Sync S3 to DB'}
          </button>
        </div>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="flex items-center gap-4">
        <div className="flex-1 relative group">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-primary-400 transition-colors" />
          <input
            type="text"
            placeholder="Search agents by name, ID or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-12 glass border-0 rounded-2xl pl-12 pr-4 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20 transition-all placeholder:text-gray-600 font-medium"
          />
        </div>
        <button
          onClick={() => alert('Agent Classification filters (Category, Economics, Version) are currently being indexed for the S3 registry.')}
          className="h-12 w-12 glass flex items-center justify-center rounded-2xl text-gray-400 hover:text-white hover:bg-white/10 transition-all"
        >
          <Filter className="w-5 h-5" />
        </button>
      </div>

      {/* Error handling */}
      {error && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-500 text-sm font-bold flex items-center gap-2 leading-none">
          <Shield className="w-4 h-4" />
          {error}
        </div>
      )}

      {/* Agents Grid/Table */}
      <div className="glass rounded-3xl overflow-hidden border-0">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/[0.03] border-b border-white/[0.05]">
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Agent Entity</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Classification</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Economics</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-center">Installations</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-right">Visibility</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.04]">
            {loading && agents.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center">
                  <div className="flex flex-col items-center gap-3">
                    <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
                    <p className="text-xs font-bold text-gray-500 uppercase tracking-widest">Scanning Registry...</p>
                  </div>
                </td>
              </tr>
            ) : filteredAgents.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-500 text-sm italic font-medium">
                  No agents found in the registry.
                </td>
              </tr>
            ) : filteredAgents.map((agent) => (
              <tr key={agent.slug} className="group hover:bg-white/[0.02] transition-colors">
                <td className="px-6 py-5">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-white/5 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                      <Bot className="w-6 h-6 text-indigo-400" />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-white group-hover:text-primary-400 transition-colors tracking-tight leading-none">{agent.name}</p>
                      <p className="text-[11px] text-gray-500 font-bold uppercase tracking-widest mt-1.5 flex items-center gap-1.5 leading-none">
                        <Layers className="w-3 h-3" />
                        v{agent.version} • {agent.author}
                      </p>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-5">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-400 text-[10px] font-black uppercase tracking-widest border border-indigo-500/20 leading-none">
                      {agent.category}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-5">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-emerald-500/5 text-emerald-500">
                      <DollarSign className="w-3.5 h-3.5" />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-white leading-none">{agent.price > 0 ? `$${agent.price}` : 'Free'}</p>
                      <p className="text-[9px] text-gray-600 font-bold uppercase tracking-widest mt-1 leading-none">{agent.pricingModel}</p>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-5 text-center">
                  <div className="flex flex-col items-center">
                    <p className="text-sm font-black text-white leading-none">{agent.usageCount}</p>
                    <p className="text-[8px] text-gray-600 font-black uppercase tracking-widest mt-1 leading-none">Active Users</p>
                  </div>
                </td>
                <td className="px-6 py-5 text-right">
                  <button
                    onClick={() => handleVisibilityToggle(agent.slug, agent.isVisible)}
                    className={`p-2.5 rounded-xl border transition-all ${agent.isVisible
                      ? 'bg-emerald-500/5 border-emerald-500/10 text-emerald-500 hover:bg-emerald-500/10'
                      : 'bg-white/5 border-white/5 text-gray-500 hover:bg-white/10'}`}
                    title={agent.isVisible ? 'Hide from Marketplace' : 'Show in Marketplace'}
                  >
                    {agent.isVisible ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
