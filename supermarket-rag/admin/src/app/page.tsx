'use client';

import { useState, useEffect } from 'react';
import { ShoppingBag, MessageSquare, ShieldCheck, Loader2 } from 'lucide-react';

export default function Dashboard() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/admin/dashboard')
            .then(res => res.json())
            .then(data => {
                if (data && !data.error) {
                    setStats(data);
                } else {
                    console.error('API Error:', data);
                    setStats({ totalProducts: 0, logsToday: 0, disabledProducts: 0, status: 'Error' });
                }
                setLoading(false);
            })
            .catch(e => {
                console.error(e);
                setStats({ totalProducts: 0, logsToday: 0, disabledProducts: 0, status: 'Offline' });
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <Loader2 className="animate-spin" size={32} />
            </div>
        );
    }

    return (
        <div className="animate-fade-in">
            <header style={{ marginBottom: '3rem' }}>
                <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>Dashboard</h1>
                <p style={{ color: 'var(--muted-foreground)' }}>Welcome back to your supermarket RAG management hub.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '2rem' }}>
                <div className="card">
                    <div style={{ color: 'var(--muted-foreground)', fontSize: '0.875rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <ShoppingBag size={14} /> Total Products
                    </div>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.totalProducts}</div>
                    <div style={{ color: 'var(--muted-foreground)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                        {stats.disabledProducts} disabled
                    </div>
                </div>
                <div className="card">
                    <div style={{ color: 'var(--muted-foreground)', fontSize: '0.875rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <MessageSquare size={14} /> Chat Logs Today
                    </div>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.logsToday}</div>
                    <div style={{ color: '#3b82f6', fontSize: '0.875rem', marginTop: '0.5rem' }}>Active monitoring</div>
                </div>
                <div className="card">
                    <div style={{ color: 'var(--muted-foreground)', fontSize: '0.875rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <ShieldCheck size={14} /> System Health
                    </div>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#10b981' }}></span>
                        {stats.status}
                    </div>
                    <div style={{ color: 'var(--muted-foreground)', fontSize: '0.875rem', marginTop: '0.5rem' }}>All services running</div>
                </div>
            </div>
        </div>
    );
}
