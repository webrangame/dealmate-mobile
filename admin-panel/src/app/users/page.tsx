'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Users, 
  Search, 
  Filter, 
  MoreVertical,
  Mail,
  Calendar,
  Shield,
  Eye,
  Trash2,
  ExternalLink,
  Loader2
} from 'lucide-react';

interface MarketplaceUser {
  id: number;
  name: string;
  email: string;
  joined: string;
  status: string;
}

export default function UserManagementPage() {
  const [users, setUsers] = useState<MarketplaceUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [error, setError] = useState('');

  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/admin/users');
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.details || data.error || 'Failed to fetch users');
      }
      
      setUsers(data.users || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleExport = () => {
    const headers = ['ID', 'Name', 'Email', 'Joined', 'Status'];
    const csvContent = [
      headers.join(','),
      ...users.map(u => [u.id, u.name, u.email, u.joined, u.status].join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `user_registry_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const filteredUsers = users.filter(user => 
    user.name.toLowerCase().includes(search.toLowerCase()) || 
    user.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header section */}
      <div className="flex items-end justify-between">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-5 h-5 text-primary-400" />
            <h2 className="text-xl font-bold text-white uppercase tracking-wider">User Directory</h2>
          </div>
          <p className="text-gray-500 font-medium tracking-tight">Managing marketplace participants across all regions.</p>
        </div>
        <button 
          onClick={fetchUsers}
          disabled={loading}
          className="px-5 py-2.5 bg-primary-500 hover:bg-primary-600 rounded-xl text-sm font-bold text-white transition-all shadow-lg shadow-primary-500/20 flex items-center gap-2"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
          Sync Registry
        </button>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="flex items-center gap-4">
        <div className="flex-1 relative group">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-primary-400 transition-colors" />
          <input 
            type="text" 
            placeholder="Filter database by name, email or ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-12 glass border-0 rounded-2xl pl-12 pr-4 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20 transition-all placeholder:text-gray-600"
          />
        </div>
        <button 
          onClick={handleExport}
          className="h-12 w-12 glass flex items-center justify-center rounded-2xl text-gray-400 hover:text-white hover:bg-white/10 transition-all"
          title="Export Registry to CSV"
        >
          <ExternalLink className="w-5 h-5" />
        </button>
      </div>

      {/* Error handling */}
      {error && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-500 text-sm font-bold">
          {error}
        </div>
      )}

      {/* Table Section */}
      <div className="glass rounded-3xl overflow-hidden border-0">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/[0.03] border-b border-white/[0.05]">
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">User Identity</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Membership</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-center">Security Status</th>
              <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.04]">
            {loading ? (
              <tr>
                <td colSpan={4} className="px-6 py-12 text-center">
                  <div className="flex flex-col items-center gap-3">
                    <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
                    <p className="text-xs font-bold text-gray-500 uppercase tracking-widest">Querying database...</p>
                  </div>
                </td>
              </tr>
            ) : filteredUsers.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-6 py-12 text-center text-gray-500 text-sm italic">
                  No users found in the registry.
                </td>
              </tr>
            ) : filteredUsers.map((user) => (
              <tr key={user.id} className="group hover:bg-white/[0.02] transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 border border-white/5 flex items-center justify-center font-bold text-primary-400 group-hover:scale-110 transition-transform">
                      {user.name.charAt(0)}
                    </div>
                    <div>
                      <p className="text-sm font-bold text-white group-hover:text-primary-400 transition-colors font-sans">{user.name}</p>
                      <div className="flex items-center gap-1 mt-0.5">
                        <Mail className="w-3 h-3 text-gray-600" />
                        <span className="text-[11px] text-gray-500 font-medium lowercase leading-none">{user.email}</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-1.5">
                    <Calendar className="w-3.5 h-3.5 text-gray-600" />
                    <span className="text-xs text-gray-400 font-medium tracking-tight">
                      {new Date(user.joined).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex justify-center">
                    <span className={`px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest leading-none ${
                      user.status === 'active' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-red-500/10 text-red-500'
                    }`}>
                      {user.status}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 text-right">
                   <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Link 
                        href={`/users/${user.id}`} 
                        className="p-2 rounded-lg bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 transition-all"
                        title="View Full Profile"
                      >
                        <Eye className="w-4 h-4" />
                      </Link>
                      <button 
                        onClick={() => alert(`Operational details for ${user.name} are currently restricted to the profile view.`)}
                        className="p-2 rounded-lg bg-white/5 text-gray-600 hover:text-white hover:bg-white/10 transition-all cursor-not-allowed"
                      >
                        <MoreVertical className="w-4 h-4" />
                      </button>
                   </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
