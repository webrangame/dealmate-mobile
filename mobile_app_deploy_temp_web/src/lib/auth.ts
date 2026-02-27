import axios from 'axios';
import { User, AuthResponse } from '@/types';

const MARKET_BASE_URL = 'https://market.niyogen.com';

class AuthService {
    async login(email: string, password: string): Promise<User> {
        const response = await axios.post<AuthResponse>(`${MARKET_BASE_URL}/api/auth/login`, {
            email,
            password,
        });

        const user = response.data.user;
        localStorage.setItem('user', JSON.stringify(user));
        return user;
    }

    async signup(name: string, email: string, password: string): Promise<User> {
        const response = await axios.post<AuthResponse>(`${MARKET_BASE_URL}/api/auth/signup`, {
            name,
            email,
            password,
        });

        const user = response.data.user;
        localStorage.setItem('user', JSON.stringify(user));
        return user;
    }

    async logout(): Promise<void> {
        localStorage.removeItem('user');
    }

    getCurrentUser(): User | null {
        if (typeof window === 'undefined') return null;

        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                return JSON.parse(userStr);
            } catch {
                return null;
            }
        }
        return null;
    }

    isAuthenticated(): boolean {
        return this.getCurrentUser() !== null;
    }
}

export const authService = new AuthService();
