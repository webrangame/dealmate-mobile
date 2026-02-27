'use client';

import { useState, useEffect } from 'react';
import { Calendar, User, MessageSquare, Globe, Loader2, ChevronLeft, ChevronRight } from 'lucide-react';

interface ChatLog {
    id: number;
    timestamp: string;
    user_id: string;
    user_query: string;
    ai_response: string;
    ip_address: string;
    metadata: any;
}

export default function LogsPage() {
    const [logs, setLogs] = useState<ChatLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [total, setTotal] = useState(0);
    const [offset, setOffset] = useState(0);
    const limit = 20;

    useEffect(() => {
        fetchLogs();
    }, [offset]);

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const res = await fetch(`/api/admin/logs?limit=${limit}&offset=${offset}`);
            const data = await res.json();
            if (data && Array.isArray(data.logs)) {
                setLogs(data.logs);
                setTotal(data.total || 0);
            } else {
                console.error('Invalid logs data:', data);
                setLogs([]);
                setTotal(0);
            }
        } catch (e) {
            console.error(e);
            setLogs([]);
            setTotal(0);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleString();
    };

    return (
        <div className="animate-fade-in">
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
                <div>
                    <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>Chat Logs</h1>
                    <p style={{ color: 'var(--muted-foreground)' }}>Monitor real-time customer interactions and RAG performance.</p>
                </div>
                <div className="card" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ fontSize: '0.875rem' }}>
                        {offset + 1} - {Math.min(offset + limit, total)} of {total}
                    </div>
                    <div style={{ display: 'flex', gap: '0.25rem' }}>
                        <button
                            className="btn btn-secondary"
                            style={{ padding: '0.25rem' }}
                            disabled={offset === 0}
                            onClick={() => setOffset(Math.max(0, offset - limit))}
                        >
                            <ChevronLeft size={16} />
                        </button>
                        <button
                            className="btn btn-secondary"
                            style={{ padding: '0.25rem' }}
                            disabled={offset + limit >= total}
                            onClick={() => setOffset(offset + limit)}
                        >
                            <ChevronRight size={16} />
                        </button>
                    </div>
                </div>
            </header>

            {loading ? (
                <div style={{ padding: '5rem', textAlign: 'center' }}>
                    <Loader2 className="animate-spin" style={{ margin: '0 auto' }} />
                </div>
            ) : logs.length === 0 ? (
                <div className="card" style={{ padding: '5rem', textAlign: 'center', color: 'var(--muted-foreground)' }}>
                    No chat logs recorded yet.
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {logs.map((log) => (
                        <div key={log.id} className="card" style={{ padding: '1.5rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
                                <div style={{ display: 'flex', gap: '1.5rem' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', color: 'var(--muted-foreground)' }}>
                                        <Calendar size={14} /> {formatDate(log.timestamp)}
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', color: 'var(--muted-foreground)' }}>
                                        <User size={14} /> {log.user_id}
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', color: 'var(--muted-foreground)' }}>
                                        <Globe size={14} /> {log.ip_address || 'Unknown'}
                                    </div>
                                </div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--muted-foreground)' }}>ID: #{log.id}</div>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                                <div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem', fontWeight: 600, fontSize: '0.875rem' }}>
                                        <MessageSquare size={16} color="var(--primary)" /> User Query
                                    </div>
                                    <div style={{ background: 'var(--background)', padding: '1rem', borderRadius: 'var(--radius)', fontSize: '0.925rem', lineHeight: 1.5 }}>
                                        {log.user_query}
                                    </div>
                                </div>
                                <div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem', fontWeight: 600, fontSize: '0.875rem' }}>
                                        <Loader2 size={16} color="#10b981" /> Assistant Response
                                    </div>
                                    <div style={{ background: 'var(--background)', padding: '1rem', borderRadius: 'var(--radius)', fontSize: '0.925rem', lineHeight: 1.5, maxHeight: '200px', overflowY: 'auto' }}>
                                        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                                            {typeof log.ai_response === 'string' ? log.ai_response : JSON.stringify(log.ai_response, null, 2)}
                                        </pre>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center', gap: '1rem', paddingBottom: '4rem' }}>
                <button
                    className="btn btn-secondary"
                    disabled={offset === 0}
                    onClick={() => setOffset(Math.max(0, offset - limit))}
                >
                    Previous Page
                </button>
                <button
                    className="btn btn-secondary"
                    disabled={offset + limit >= total}
                    onClick={() => setOffset(offset + limit)}
                >
                    Next Page
                </button>
            </div>
        </div>
    );
}
