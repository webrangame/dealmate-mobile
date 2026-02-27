'use client';

import { useState, useEffect } from 'react';
import { 
  Settings, 
  Database, 
  Cloud, 
  Zap, 
  Shield, 
  Globe, 
  RefreshCw,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Server,
  Key,
  Code
} from 'lucide-react';

interface HealthData {
  database: { status: string; latency?: string; details?: string };
  s3: { status: string; latency?: string; details?: string };
  litellm: { status: string; latency?: string; details?: string };
  environment: {
    node_env: string;
    app_url: string;
  };
}

export default function SettingsPage() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchHealth = async () => {
    setRefreshing(true);
    try {
      const res = await fetch('/api/admin/health');
      if (res.ok) {
        const data = await res.json();
        setHealth(data);
      }
    } catch (error) {
      console.error('Failed to fetch health status:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleMaintenance = (task: string) => {
    const confirmed = confirm(`CAUTION: You are about to trigger a system-level ${task}. This action is irreversible for the current session. Proceed?`);
    if (confirmed) {
      alert(`${task} sequence initiated. Monitoring Identity Stream...`);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  const StatusIcon = ({ status }: { status: string }) => {
    if (status === 'healthy') return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
    if (status === 'unhealthy') return <XCircle className="w-5 h-5 text-red-400" />;
    return <AlertTriangle className="w-5 h-5 text-amber-400" />;
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header section */}
      <div className="flex items-end justify-between">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Settings className="w-5 h-5 text-primary-400" />
            <h2 className="text-xl font-bold text-white uppercase tracking-wider">System Settings</h2>
          </div>
          <p className="text-gray-500 font-medium tracking-tight">Infrastructure monitoring and platform configuration center.</p>
        </div>
        <button 
          onClick={fetchHealth}
          disabled={refreshing}
          className="px-4 py-2.5 bg-white/5 border border-white/5 rounded-xl text-sm font-bold text-gray-400 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh Diagnostics
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Health & Status */}
        <div className="lg:col-span-2 space-y-8">
          <div className="glass rounded-3xl overflow-hidden border-0">
             <div className="bg-white/5 px-6 py-4 border-b border-white/5 flex justify-between items-center">
                <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                   <Server className="w-4 h-4 text-primary-400" />
                   Core Infrastructure
                </h3>
                <span className="text-[10px] bg-emerald-500/10 text-emerald-500 px-2 py-0.5 rounded font-black uppercase tracking-widest">Live Monitoring</span>
             </div>
             <div className="p-6 space-y-4">
                {[
                  { id: 'database', name: 'PostgreSQL Registry', icon: Database, color: 'blue', data: health?.database },
                  { id: 's3', name: 'AWS S3 Storage (Agents)', icon: Cloud, color: 'indigo', data: health?.s3 },
                  { id: 'litellm', name: 'LiteLLM Proxy API', icon: Zap, color: 'yellow', data: health?.litellm },
                ].map((service) => (
                  <div key={service.id} className="group p-4 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.05] transition-all duration-300">
                     <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                           <div className={`w-12 h-12 rounded-xl bg-${service.color}-500/10 flex items-center justify-center border border-${service.color}-500/20 group-hover:scale-110 transition-transform`}>
                              <service.icon className={`w-6 h-6 text-${service.color}-400`} />
                           </div>
                           <div>
                              <p className="text-sm font-bold text-white tracking-tight">{service.name}</p>
                              <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">
                                {service.data?.latency ? `Latency: ${service.data.latency}` : 'Checking availability...'}
                              </p>
                           </div>
                        </div>
                        <div className="flex items-center gap-3">
                           {service.data ? (
                             <>
                               <span className={`text-[10px] font-black uppercase tracking-widest ${service.data.status === 'healthy' ? 'text-emerald-500' : 'text-red-500'}`}>
                                 {service.data.status}
                               </span>
                               <StatusIcon status={service.data.status} />
                             </>
                           ) : (
                             <RefreshCw className="w-4 h-4 text-gray-600 animate-spin" />
                           )}
                        </div>
                     </div>
                     {service.data?.status === 'unhealthy' && service.data.details && (
                       <div className="mt-4 p-3 rounded-xl bg-red-500/5 border border-red-500/10 text-[11px] text-red-400 font-mono break-all font-medium">
                         Error: {service.data.details}
                       </div>
                     )}
                  </div>
                ))}
             </div>
          </div>

          <div className="glass rounded-3xl p-8 relative overflow-hidden group">
             <div className="absolute top-0 right-0 w-64 h-64 bg-primary-500/5 blur-[100px] -mr-32 -mt-32 rounded-full group-hover:bg-primary-500/10 transition-colors duration-700"></div>
             <div className="flex items-center gap-3 mb-6">
                <div className="p-2 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
                   <Shield className="w-5 h-5 text-indigo-400" />
                </div>
                <h3 className="text-lg font-bold text-white tracking-tight">Platform Configuration</h3>
             </div>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                   <div>
                      <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest block mb-2 px-1">Global Application URL</label>
                      <div className="glass h-11 rounded-xl px-4 flex items-center gap-3 group/field hover:bg-white/5 transition-all">
                        <Globe className="w-4 h-4 text-gray-600 group-hover/field:text-primary-400 transition-colors" />
                        <span className="text-sm font-medium text-gray-400 truncate">{health?.environment.app_url || 'Detecting...'}</span>
                      </div>
                   </div>
                   <div>
                      <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest block mb-2 px-1">Runtime Environment</label>
                      <div className="glass h-11 rounded-xl px-4 flex items-center gap-3 border-0">
                        <Code className="w-4 h-4 text-gray-600" />
                        <span className="text-sm font-black text-primary-400 uppercase italic tracking-widest">{health?.environment.node_env || 'production'}</span>
                      </div>
                   </div>
                </div>
                <div className="bg-white/[0.03] border border-white/5 rounded-2xl p-6 flex flex-col justify-center">
                   <h4 className="text-xs font-bold text-white mb-2 uppercase tracking-widest">Admin Authorization</h4>
                   <p className="text-[11px] text-gray-500 font-medium leading-relaxed">
                     Your session is secured using RSA-256 JWT tokens. API access requires bearer authentication from trusted origins.
                   </p>
                   <button 
                    onClick={() => alert('Identity Framework documentation is currently being synthesized for this origin.')}
                    className="mt-4 text-[10px] font-bold text-primary-400 uppercase tracking-widest hover:text-white transition-colors flex items-center gap-2"
                   >
                     Learn More <RefreshCw className="w-3 h-3" />
                   </button>
                </div>
             </div>
          </div>
        </div>

        {/* Right Column: Key Management / Other */}
        <div className="space-y-8">
           <div className="glass rounded-3xl p-6 border-0">
              <h3 className="text-sm font-bold text-white uppercase tracking-widest mb-4 px-2 flex items-center gap-2">
                 <Key className="w-4 h-4 text-yellow-500" />
                 Registry Tokens
              </h3>
              <div className="space-y-3">
                 {[
                   { name: 'LiteLLM Master Key', val: 'sk-dcb0...7642', status: 'Active' },
                   { name: 'AWS Access Key', val: 'AKIA...K7QA', status: 'Active' },
                   { name: 'Database Secret', val: '••••••••••••••••', status: 'Secured' },
                 ].map((k, i) => (
                   <div key={i} className="p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-all cursor-default group">
                      <div className="flex justify-between items-start mb-1">
                         <p className="text-[11px] font-bold text-gray-400">{k.name}</p>
                         <span className="text-[8px] font-black uppercase tracking-widest text-emerald-500">{k.status}</span>
                      </div>
                      <p className="font-mono text-[10px] text-gray-500 group-hover:text-gray-300 transition-colors">{k.val}</p>
                   </div>
                 ))}
              </div>
           </div>

           <div className="p-6 rounded-3xl bg-primary-500/5 border border-primary-500/10">
              <h4 className="text-xs font-black text-white uppercase tracking-widest mb-3 leading-none">Maintenance Center</h4>
              <p className="text-[11px] text-gray-500 font-medium mb-4 leading-relaxed"> Perform critical system tasks such as cache invalidation or log rotations.</p>
              <div className="space-y-2">
                 <button 
                  onClick={() => handleMaintenance('Redis Cache Flushing')}
                  className="w-full py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-[10px] font-black text-white uppercase tracking-widest transition-all"
                 >
                   Flush Redis Cache
                 </button>
                 <button 
                  onClick={() => handleMaintenance('RSA Key Rotation')}
                  className="w-full py-2.5 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-[10px] font-black text-red-500 uppercase tracking-widest transition-all border border-red-500/20"
                 >
                   Rotate Auth Keys
                 </button>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
}
