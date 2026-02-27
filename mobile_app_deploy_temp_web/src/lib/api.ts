import axios from 'axios';
import { ChatResponse, Review, ReviewsResponse } from '@/types';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://xfukqtd5pc.us-east-1.awsapprunner.com';
const MARKET_BASE_URL = 'https://market.niyogen.com';
const AGENT_ID = 'price-comparison-agent-australia';

class ApiService {
    private getUserId(): string {
        if (typeof window === 'undefined') return 'test_user_123';

        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                return user.email || user.id || 'test_user_123';
            } catch {
                return 'test_user_123';
            }
        }
        return 'test_user_123';
    }

    async sendMessage(text: string): Promise<ChatResponse> {
        const userId = this.getUserId();

        const response = await axios.post<ChatResponse>(`${BASE_URL}/chat`, {
            text,
            user_id: userId,
            stream: false,
        });

        return response.data;
    }

    async *sendMessageStream(text: string): AsyncGenerator<any> {
        const userId = this.getUserId();

        const response = await fetch(`${BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream',
            },
            body: JSON.stringify({
                text,
                user_id: userId,
                stream: true,
            }),
        });

        if (!response.ok) {
            throw new Error(`Streaming failed: ${response.statusText}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
            throw new Error('ReadableStream not supported');
        }

        let buffer = '';
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
                if (!line.trim()) continue;
                try {
                    const data = JSON.parse(line);
                    yield data;
                } catch (e) {
                    console.warn('Failed to parse stream line:', line, e);
                }
            }
        }
    }

    async fetchReviews(): Promise<Review[]> {
        try {
            const response = await axios.get<any>(
                `${MARKET_BASE_URL}/api/reviews?agentId=${AGENT_ID}&limit=50`,
                { withCredentials: true } // Send shared Niyogen cookies
            );

            const rawReviews = response.data.reviews || [];

            // Map snake_case API fields to camelCase Review interface
            return rawReviews.map((r: any) => ({
                id: r.id,
                userId: r.user_id,
                userName: r.user_name,
                rating: r.rating,
                comment: r.comment,
                createdAt: r.created_at
            }));
        } catch (error: any) {
            console.error('ApiService.fetchReviews error:', {
                message: error.message,
                status: error.response?.status,
                data: error.response?.data,
                url: error.config?.url
            });
            throw error;
        }
    }

    async submitReview(rating: number, comment: string): Promise<void> {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
            throw new Error('No user found. Please login.');
        }

        const user = JSON.parse(userStr);
        const userId = user.id || user.email;

        if (!userId) {
            throw new Error('User ID is required.');
        }

        await axios.post(`${MARKET_BASE_URL}/api/reviews`, {
            agentId: AGENT_ID,
            userId,
            rating,
            comment,
        }, { withCredentials: true }); // Send shared Niyogen cookies
    }
}

export const apiService = new ApiService();
