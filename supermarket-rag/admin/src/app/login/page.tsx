'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Lock, User, Loader2, ShieldCheck } from 'lucide-react';

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await res.json();

            if (res.ok) {
                router.push('/');
            } else {
                setError(data.error || 'Invalid credentials');
            }
        } catch (err) {
            setError('An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'radial-gradient(circle at top right, #111827, #000000)',
            padding: '1.5rem'
        }}>
            <div className="card animate-fade-in" style={{
                width: '100%',
                maxWidth: '420px',
                padding: '3rem',
                border: '1px solid rgba(255,255,255,0.1)',
                backdropFilter: 'blur(16px)',
                boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)'
            }}>
                <header style={{ textAlign: 'center', marginBottom: '3rem' }}>
                    <div style={{
                        width: '64px',
                        height: '64px',
                        background: 'linear-gradient(135deg, #3b82f6, #2563eb)',
                        borderRadius: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 1.5rem',
                        boxShadow: '0 0 20px rgba(37, 99, 235, 0.3)'
                    }}>
                        <ShieldCheck color="white" size={32} />
                    </div>
                    <h1 style={{
                        fontSize: '1.75rem',
                        fontWeight: '800',
                        letterSpacing: '-0.025em',
                        margin: '0',
                        color: '#ffffff'
                    }}>
                        RAG Admin
                    </h1>
                    <p style={{
                        color: 'var(--muted-foreground)',
                        fontSize: '0.925rem',
                        marginTop: '0.75rem',
                        fontWeight: '400'
                    }}>
                        Sign in to access the management portal
                    </p>
                </header>

                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
                        <label style={{
                            fontSize: '0.8125rem',
                            fontWeight: '600',
                            color: '#9ca3af',
                            textTransform: 'uppercase',
                            letterSpacing: '0.05em'
                        }}>
                            Username
                        </label>
                        <div style={{ position: 'relative' }}>
                            <User style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b7280' }} size={18} />
                            <input
                                type="text"
                                autoComplete="username"
                                className="card"
                                style={{
                                    width: '100%',
                                    paddingLeft: '3rem',
                                    background: 'rgba(255,255,255,0.03)',
                                    height: '48px',
                                    fontSize: '1rem',
                                    border: '1px solid rgba(255,255,255,0.05)',
                                    transition: 'all 0.2s ease'
                                }}
                                placeholder="Enter your username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
                        <label style={{
                            fontSize: '0.8125rem',
                            fontWeight: '600',
                            color: '#9ca3af',
                            textTransform: 'uppercase',
                            letterSpacing: '0.05em'
                        }}>
                            Password
                        </label>
                        <div style={{ position: 'relative' }}>
                            <Lock style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b7280' }} size={18} />
                            <input
                                type="password"
                                autoComplete="current-password"
                                className="card"
                                style={{
                                    width: '100%',
                                    paddingLeft: '3rem',
                                    background: 'rgba(255,255,255,0.03)',
                                    height: '48px',
                                    fontSize: '1rem',
                                    border: '1px solid rgba(255,255,255,0.05)'
                                }}
                                placeholder="••••••••"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    {error && (
                        <div style={{
                            color: '#f87171',
                            fontSize: '0.875rem',
                            textAlign: 'center',
                            padding: '0.75rem',
                            background: 'rgba(239, 68, 68, 0.1)',
                            borderRadius: '8px',
                            border: '1px solid rgba(239, 68, 68, 0.2)',
                            animation: 'shake 0.4s ease'
                        }}>
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{
                            height: '50px',
                            fontSize: '1rem',
                            fontWeight: '600',
                            marginTop: '0.5rem',
                            backgroundImage: 'linear-gradient(to right, #2563eb, #3b82f6)'
                        }}
                        disabled={loading}
                    >
                        {loading ? <Loader2 className="animate-spin" size={22} /> : 'Sign In to Portal'}
                    </button>
                </form>

                <footer style={{ marginTop: '3rem', textAlign: 'center', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '1.5rem' }}>
                    <p style={{ color: '#4b5563', fontSize: '0.75rem' }}>
                        &copy; 2026 Supermarket RAG System. All rights reserved.
                    </p>
                </footer>
            </div>

            <style jsx>{`
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
      `}</style>
        </div>
    );
}
