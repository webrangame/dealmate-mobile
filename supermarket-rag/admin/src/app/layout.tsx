'use client';

import './globals.css';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { LayoutDashboard, ShoppingBag, MessageSquare, LogOut } from 'lucide-react';

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();
    const router = useRouter();
    const isLoginPage = pathname === '/login';

    const handleLogout = async () => {
        try {
            const res = await fetch('/api/auth/logout', { method: 'POST' });
            if (res.ok) {
                router.push('/login');
            }
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    if (isLoginPage) {
        return (
            <html lang="en" data-theme="dark">
                <body>{children}</body>
            </html>
        );
    }

    const navItems = [
        { name: 'Dashboard', href: '/', icon: <LayoutDashboard size={18} /> },
        { name: 'Products', href: '/products', icon: <ShoppingBag size={18} /> },
        { name: 'Chat Logs', href: '/logs', icon: <MessageSquare size={18} /> },
    ];

    return (
        <html lang="en" data-theme="dark">
            <body>
                <div style={{ display: 'flex', minHeight: '100vh' }}>
                    <aside className="glass" style={{
                        width: '260px',
                        borderRight: '1px solid var(--border)',
                        padding: '2.5rem 1.5rem',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '2.5rem',
                        position: 'fixed',
                        height: '100vh',
                        zIndex: 40
                    }}>
                        <div style={{
                            fontSize: '1.25rem',
                            fontWeight: '800',
                            color: 'var(--primary)',
                            letterSpacing: '-0.025em',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.75rem'
                        }}>
                            <div style={{ width: '8px', height: '8px', background: 'var(--primary)', borderRadius: '50%' }}></div>
                            RAG Admin
                        </div>

                        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
                            {navItems.map((item) => {
                                const isActive = pathname === item.href;
                                return (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        className={`btn ${isActive ? 'btn-primary' : 'btn-secondary'}`}
                                        style={{
                                            justifyContent: 'flex-start',
                                            gap: '0.75rem',
                                            border: 'none',
                                            background: isActive ? 'var(--primary)' : 'transparent',
                                            color: isActive ? 'white' : 'var(--muted-foreground)',
                                            fontWeight: isActive ? 600 : 500
                                        }}
                                    >
                                        {item.icon}
                                        {item.name}
                                    </Link>
                                );
                            })}
                        </nav>

                        <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1.5rem' }}>
                            <button
                                onClick={handleLogout}
                                className="btn btn-secondary"
                                style={{
                                    width: '100%',
                                    justifyContent: 'flex-start',
                                    gap: '0.75rem',
                                    border: 'none',
                                    background: 'transparent',
                                    color: '#f87171' // Soft red
                                }}
                            >
                                <LogOut size={18} />
                                Sign Out
                            </button>
                        </div>
                    </aside>

                    <main style={{
                        flex: 1,
                        marginLeft: '260px',
                        padding: '3rem 4rem',
                        overflowY: 'auto'
                    }}>
                        {children}
                    </main>
                </div>
            </body>
        </html>
    );
}
