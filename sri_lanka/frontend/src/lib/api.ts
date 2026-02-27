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
        });

        return response.data;
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
