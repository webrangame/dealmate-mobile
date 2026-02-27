'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Search, Bell, User, LogOut, Loader2 } from 'lucide-react';

interface AdminUser {
  id: number;
  email: string;
  name: string;
}

export default function Header() {
  const [admin, setAdmin] = useState<AdminUser | null>(null);
  const [loggingOut, setLoggingOut] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function fetchMe() {
      try {
        const res = await fetch('/api/auth/me');
        if (res.ok) {
          const data = await res.json();
          setAdmin(data.user);
        }
      } catch (err) {
        console.error('Failed to fetch admin');
      }
    }
    fetchMe();
  }, []);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
      router.push('/login');
      router.refresh();
    } catch (err) {
      console.error('Logout failed');
    } finally {
      setLoggingOut(false);
    }
  };

  return (
    <header className="h-20 glass border-b-0 sticky top-0 z-40 px-8 flex items-center justify-between">
      {/* Search Section */}
      <div className="flex-1 max-w-xl">
        <div className="relative group">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-primary-400 transition-colors" />
          <input 
            type="text" 
            placeholder="Search analytics, agents or participants..." 
            className="w-full h-11 bg-white/5 border border-white/5 rounded-2xl pl-12 pr-4 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500/30 transition-all placeholder:text-gray-600 font-medium"
          />
        </div>
      </div>

      {/* Actions Section */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-gray-400 hover:bg-white/10 hover:text-white transition-all relative group">
          <Bell className="w-5 h-5 group-hover:scale-110 transition-transform" />
          <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-primary-500 rounded-full border-2 border-admin-bg" />
        </button>

        <div className="w-[1px] h-6 bg-white/5 mx-2" />

        {/* User Profile */}
        <div className="flex items-center gap-3 pl-2 group relative">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-bold text-white tracking-tight leading-none">{admin?.name || 'Loading...'}</p>
            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest leading-none mt-1">Super Admin</p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 p-[2px] cursor-pointer">
            <div className="w-full h-full rounded-[9px] bg-admin-bg flex items-center justify-center overflow-hidden">
               <User className="text-white w-5 h-5" />
            </div>
          </div>
          
          {/* Logout Button */}
          <button 
            onClick={handleLogout}
            disabled={loggingOut}
            className="p-2 ml-2 rounded-xl bg-red-500/5 text-red-500/60 hover:text-red-500 hover:bg-red-500/10 transition-all group"
            title="Secure Logout"
          >
            {loggingOut ? <Loader2 className="w-5 h-5 animate-spin" /> : <LogOut className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />}
          </button>
        </div>
      </div>
    </header>
  );
}
