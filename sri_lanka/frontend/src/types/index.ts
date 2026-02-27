// User types
export interface User {
    id: string;
    email: string;
    name: string;
    role?: string;
}

// Chat types
export interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: Date;
    metadata?: any[];
}

// Review types
export interface Review {
    id: string;
    userId: string;
    userName?: string;
    rating: number;
    comment: string;
    createdAt: string;
}

// Ad types
export interface VendorAd {
    store: string;
    offer: string;
    color: string;
    image?: string;
}

// API Response types
export interface ChatResponse {
    response: string;
    metadata?: any[];
}

export interface ReviewsResponse {
    reviews: Review[];
}

export interface AuthResponse {
    user: User;
    token?: string;
}
