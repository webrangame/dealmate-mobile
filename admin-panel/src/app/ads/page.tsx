'use client';

import { useState, useEffect } from 'react';
import {
    Megaphone,
    Plus,
    Search,
    Filter,
    Eye,
    EyeOff,
    Trash2,
    DollarSign,
    Link as LinkIcon,
    Loader2,
    X,
    Upload,
    Image as ImageIcon,
    ExternalLink,
    ShieldAlert,
    Layout,
    Maximize
} from 'lucide-react';
import Image from 'next/image';

interface Ad {
    id: number;
    agent_slug: string;
    agent_name?: string;
    image_url: string;
    target_url: string;
    is_paid: boolean;
    is_enabled: boolean;
    ad_type: 'Hero' | 'Square' | 'Billboard';
    created_at: string;
}

interface Agent {
    slug: string;
    name: string;
}

const AD_TYPES = [
    { id: 'Hero', name: 'Premium Hero', ratio: '16:9', size: '1920 x 1080', icon: Maximize },
    { id: 'Square', name: 'Feed Square', ratio: '1:1', size: '1080 x 1080', icon: Layout },
    { id: 'Billboard', name: 'Slim Billboard', ratio: '4:1', size: '1600 x 400', icon: Megaphone },
] as const;

export default function AdsPage() {
    const [ads, setAds] = useState<Ad[]>([]);
    const [agents, setAgents] = useState<Agent[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [search, setSearch] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Form State
    const [formData, setFormData] = useState({
        agentSlug: '',
        adType: 'Hero' as Ad['ad_type'],
        targetUrl: '',
        isPaid: false,
        isEnabled: true,
        file: null as File | null
    });
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [adsRes, agentsRes] = await Promise.all([
                fetch('/api/admin/ads'),
                fetch('/api/admin/agents')
            ]);

            const adsData = await adsRes.json();
            const agentsData = await agentsRes.json();

            if (!adsRes.ok) throw new Error(adsData.error || 'Failed to fetch ads');
            if (!agentsRes.ok) throw new Error(agentsData.error || 'Failed to fetch agents');

            setAds(adsData.ads || []);
            setAgents(agentsData.agents || []);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async (ad: Ad, field: 'is_enabled' | 'is_paid') => {
        try {
            const res = await fetch(`/api/admin/ads/${ad.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ [field]: !ad[field] })
            });
            if (!res.ok) throw new Error('Update failed');

            setAds(prev => prev.map(a => a.id === ad.id ? { ...a, [field]: !ad[field] } : a));
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm('Are you sure you want to delete this ad?')) return;
        try {
            const res = await fetch(`/api/admin/ads/${id}`, { method: 'DELETE' });
            if (!res.ok) throw new Error('Delete failed');
            setAds(prev => prev.filter(a => a.id !== id));
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!formData.file || !formData.agentSlug) {
            alert('Please select an image and an agent');
            return;
        }

        setSubmitting(true);
        try {
            const data = new FormData();
            data.append('file', formData.file);
            data.append('agentSlug', formData.agentSlug);
            data.append('adType', formData.adType);
            data.append('targetUrl', formData.targetUrl);
            data.append('isPaid', String(formData.isPaid));
            data.append('isEnabled', String(formData.isEnabled));

            const res = await fetch('/api/admin/ads', {
                method: 'POST',
                body: data
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.error || 'Upload failed');
            }

            setIsModalOpen(false);
            setFormData({ agentSlug: '', adType: 'Hero', targetUrl: '', isPaid: false, isEnabled: true, file: null });
            fetchData();
        } catch (err: any) {
            alert(err.message);
        } finally {
            setSubmitting(false);
        }
    };

    const filteredAds = ads.filter(ad =>
        ad.agent_slug.toLowerCase().includes(search.toLowerCase()) ||
        (ad.agent_name && ad.agent_name.toLowerCase().includes(search.toLowerCase()))
    );

    const selectedTypeInfo = AD_TYPES.find(t => t.id === formData.adType);

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="flex items-end justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white tracking-tight">Promotional Ads</h2>
                    <p className="text-gray-500 font-medium tracking-tight mt-1">Manage AI Agent placements and specialized banners for web and mobile.</p>
                </div>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="px-4 py-2.5 bg-primary-500 text-white rounded-xl text-sm font-bold hover:bg-primary-600 transition-all flex items-center gap-2 shadow-lg shadow-primary-500/20"
                >
                    <Plus className="w-4 h-4" />
                    Create New Ad
                </button>
            </div>

            <div className="flex items-center gap-4">
                <div className="flex-1 relative group">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 group-focus-within:text-primary-400 transition-colors" />
                    <input
                        type="text"
                        placeholder="Search ads by agent slug or name..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full h-12 glass border-0 rounded-2xl pl-12 pr-4 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20 transition-all placeholder:text-gray-600 font-medium"
                    />
                </div>
            </div>

            {error && (
                <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-500 text-sm font-bold flex items-center gap-2">
                    <ShieldAlert className="w-4 h-4" />
                    {error}
                </div>
            )}

            <div className="glass rounded-3xl overflow-hidden border-0">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-white/[0.03] border-b border-white/[0.05]">
                            <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Promotion</th>
                            <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Type / Placement</th>
                            <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none">Target Agent</th>
                            <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-center">Economics</th>
                            <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-right">Visibility</th>
                            <th className="px-6 py-5 text-[10px] font-bold text-gray-500 uppercase tracking-widest leading-none text-right"></th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/[0.04]">
                        {loading ? (
                            <tr>
                                <td colSpan={6} className="px-6 py-12 text-center">
                                    <Loader2 className="w-8 h-8 text-primary-500 animate-spin mx-auto" />
                                </td>
                            </tr>
                        ) : filteredAds.length === 0 ? (
                            <tr>
                                <td colSpan={6} className="px-6 py-12 text-center text-gray-500 text-sm italic">
                                    No promotional ads found.
                                </td>
                            </tr>
                        ) : filteredAds.map((ad) => (
                            <tr key={ad.id} className="group hover:bg-white/[0.02] transition-colors">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-4">
                                        <div className="relative w-24 h-14 rounded-lg overflow-hidden border border-white/10 bg-black/40">
                                            <Image
                                                src={ad.image_url}
                                                alt="Ad"
                                                fill
                                                className="object-cover group-hover:scale-105 transition-transform duration-500"
                                                unoptimized
                                            />
                                        </div>
                                        <div>
                                            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-tighter">Created</p>
                                            <p className="text-xs text-gray-300 font-medium">{new Date(ad.created_at).toLocaleDateString()}</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                        <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                                            {ad.ad_type === 'Hero' && <Maximize className="w-3.5 h-3.5" />}
                                            {ad.ad_type === 'Square' && <Layout className="w-3.5 h-3.5" />}
                                            {ad.ad_type === 'Billboard' && <Megaphone className="w-3.5 h-3.5" />}
                                        </div>
                                        <div>
                                            <p className="text-xs font-bold text-white leading-none">{ad.ad_type}</p>
                                            <p className="text-[9px] text-gray-600 font-bold uppercase mt-1">
                                                {AD_TYPES.find(t => t.id === ad.ad_type)?.ratio}
                                            </p>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex flex-col">
                                        <span className="text-sm font-bold text-white group-hover:text-primary-400 transition-colors uppercase tracking-tight italic">
                                            {ad.agent_name || ad.agent_slug}
                                        </span>
                                        <a href={ad.target_url} target="_blank" className="text-[10px] text-gray-500 hover:text-indigo-400 flex items-center gap-1 mt-1 truncate max-w-[200px]">
                                            <LinkIcon className="w-3 h-3" />
                                            {ad.target_url || 'No redirect URL'}
                                        </a>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <button
                                        onClick={() => handleToggle(ad, 'is_paid')}
                                        className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest border transition-all ${ad.is_paid
                                            ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20 shadow-lg shadow-emerald-500/5'
                                            : 'bg-white/5 text-gray-500 border-white/5'}`}
                                    >
                                        <DollarSign className="w-3 h-3" />
                                        {ad.is_paid ? 'Paid' : 'Free'}
                                    </button>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <button
                                        onClick={() => handleToggle(ad, 'is_enabled')}
                                        className={`p-2.5 rounded-xl border transition-all ${ad.is_enabled
                                            ? 'bg-primary-500/5 border-primary-500/10 text-primary-400 hover:bg-primary-500/10'
                                            : 'bg-white/5 border-white/5 text-gray-600 hover:bg-white/10'}`}
                                    >
                                        {ad.is_enabled ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
                                    </button>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <button
                                        onClick={() => handleDelete(ad.id)}
                                        className="p-2.5 text-gray-600 hover:text-red-400 hover:bg-red-400/5 rounded-xl transition-all"
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Modal - Create Ad */}
            {isModalOpen && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300">
                    <div className="w-full max-w-2xl glass-dark border border-white/10 rounded-[2.5rem] overflow-hidden shadow-2xl p-8 space-y-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <h3 className="text-xl font-black text-white tracking-tight uppercase italic">Publish Promotion</h3>
                                <p className="text-xs text-gray-500 font-bold tracking-widest uppercase mt-1">Direct Marketplace Injection</p>
                            </div>
                            <button
                                onClick={() => setIsModalOpen(false)}
                                className="p-3 bg-white/5 rounded-full text-gray-400 hover:text-white hover:bg-white/10 transition-all shadow-inner"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        <form onSubmit={handleUpload} className="space-y-6">
                            {/* Placement Type Picker */}
                            <div className="space-y-3">
                                <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Placement Strategy</label>
                                <div className="grid grid-cols-3 gap-3">
                                    {AD_TYPES.map((type) => (
                                        <button
                                            key={type.id}
                                            type="button"
                                            onClick={() => setFormData({ ...formData, adType: type.id as Ad['ad_type'] })}
                                            className={`flex flex-col items-center justify-center gap-2 p-4 rounded-2xl border transition-all ${formData.adType === type.id
                                                ? 'bg-primary-500/10 border-primary-500/30 text-white'
                                                : 'bg-white/5 border-white/5 text-gray-500 hover:bg-white/[0.08]'}`}
                                        >
                                            <type.icon className={`w-5 h-5 ${formData.adType === type.id ? 'text-primary-400' : ''}`} />
                                            <div className="text-center">
                                                <p className="text-[10px] font-black uppercase tracking-tighter leading-none">{type.name}</p>
                                                <p className="text-[8px] font-bold text-gray-500 mt-1 uppercase">{type.ratio}</p>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-8">
                                {/* Image Upload Area */}
                                <div className="space-y-2">
                                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Promotional Asset</label>
                                    <div
                                        className={`relative h-44 rounded-3xl border-2 border-dashed flex flex-col items-center justify-center gap-3 transition-all cursor-pointer overflow-hidden ${formData.file
                                            ? 'border-primary-500/50 bg-primary-500/5'
                                            : 'border-white/10 bg-white/5 hover:bg-white/[0.08] hover:border-white/20'}`}
                                        onClick={() => document.getElementById('ad-file')?.click()}
                                    >
                                        {formData.file ? (
                                            <div className="absolute inset-0 p-2">
                                                <img
                                                    src={URL.createObjectURL(formData.file)}
                                                    alt="Preview"
                                                    className="w-full h-full object-cover rounded-[1.25rem] shadow-2xl"
                                                />
                                                <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-md text-white px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border border-white/10 shadow-lg">
                                                    Asset Ready
                                                </div>
                                            </div>
                                        ) : (
                                            <>
                                                <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                                                    <Upload className="w-5 h-5 text-gray-400" />
                                                </div>
                                                <div className="text-center">
                                                    <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest">Recommended</p>
                                                    <p className="text-sm font-black text-white mt-1">{selectedTypeInfo?.size} px</p>
                                                </div>
                                            </>
                                        )}
                                        <input
                                            id="ad-file"
                                            type="file"
                                            className="hidden"
                                            accept="image/*"
                                            onChange={(e) => setFormData({ ...formData, file: e.target.files?.[0] || null })}
                                        />
                                    </div>
                                </div>

                                {/* Data Fields */}
                                <div className="space-y-4">
                                    <div className="space-y-1.5">
                                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1 leading-none">Primary Agent Link</label>
                                        <select
                                            value={formData.agentSlug}
                                            onChange={(e) => setFormData({ ...formData, agentSlug: e.target.value })}
                                            className="w-full h-12 bg-white/5 border border-white/5 rounded-2xl px-4 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20 transition-all font-bold tracking-tight appearance-none italic uppercase"
                                            required
                                        >
                                            <option value="" className="bg-neutral-900">-- Choose Agent --</option>
                                            {agents.map(agent => (
                                                <option key={agent.slug} value={agent.slug} className="bg-neutral-900">{agent.name}</option>
                                            ))}
                                        </select>
                                    </div>

                                    <div className="space-y-1.5">
                                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1 leading-none">Deep Link URL (Optional)</label>
                                        <input
                                            type="text"
                                            placeholder="https://app.agent.com/landing"
                                            value={formData.targetUrl}
                                            onChange={(e) => setFormData({ ...formData, targetUrl: e.target.value })}
                                            className="w-full h-12 bg-white/5 border border-white/5 rounded-2xl px-4 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20 transition-all font-medium placeholder:text-gray-600"
                                        />
                                    </div>

                                    <div className="flex gap-4">
                                        <button
                                            type="button"
                                            onClick={() => setFormData({ ...formData, isPaid: !formData.isPaid })}
                                            className={`flex-1 flex items-center justify-center gap-2 h-12 rounded-2xl border transition-all text-[10px] font-black uppercase tracking-widest ${formData.isPaid
                                                ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                                                : 'bg-white/5 border-white/5 text-gray-500'}`}
                                        >
                                            <DollarSign className="w-3.5 h-3.5" />
                                            {formData.isPaid ? 'Commercial' : 'Community'}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={submitting}
                                className="w-full h-14 bg-gradient-to-r from-primary-500 to-indigo-600 rounded-[1.25rem] text-sm font-black text-white uppercase tracking-widest shadow-2xl shadow-primary-500/30 hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-3 disabled:opacity-50"
                            >
                                {submitting ? (
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                ) : (
                                    <>
                                        <ImageIcon className="w-5 h-5" />
                                        Inject {selectedTypeInfo?.name} into Marketplace
                                    </>
                                )}
                            </button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
