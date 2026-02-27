'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '@/types';
import { authService } from '@/lib/auth';

interface AuthContextType {
    user: User | null;
    login: (email: string, password: string) => Promise<void>;
    signup: (name: string, email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const initAuth = async () => {
            // 1. Check for existing local session
            const currentUser = authService.getCurrentUser();
            if (currentUser) {
                setUser(currentUser);
                setIsLoading(false);
                return;
            }

            // 2. No local session, try Silent SSO with shared cookies
            try {
                console.log('[AuthContext] No local session, checking Niyogen SSO...');
                const response = await fetch('https://market.niyogen.com/api/auth/me', {
                    method: 'GET',
                    credentials: 'include',
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.user) {
                        console.log('[AuthContext] SSO session detected:', data.user.email);
                        const user = {
                            id: String(data.user.id),
                            email: data.user.email,
                            name: data.user.name || data.user.email.split('@')[0],
                        };
                        localStorage.setItem('user', JSON.stringify(user));
                        setUser(user);
                    }
                }
            } catch (err) {
                console.error('[AuthContext] SSO check failed:', err);
            } finally {
                setIsLoading(false);
            }
        };

        initAuth();
    }, []);

    const login = async (email: string, password: string) => {
        const user = await authService.login(email, password);
        setUser(user);
    };

    const signup = async (name: string, email: string, password: string) => {
        const user = await authService.signup(name, email, password);
        setUser(user);
    };

    const logout = async () => {
        await authService.logout();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, signup, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
