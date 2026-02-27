'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { apiService } from '@/lib/api';
import { ChatMessage as ChatMessageType } from '@/types';
import Header from '@/components/layout/Header';
import AdsCarousel from '@/components/ads/AdsCarousel';
import ChatMessage from '@/components/chat/ChatMessage';
import ChatInput from '@/components/chat/ChatInput';
import TypingIndicator from '@/components/chat/TypingIndicator';

export default function ChatPage() {
    const router = useRouter();
    const { user, isLoading: authLoading } = useAuth();
    const [messages, setMessages] = useState<ChatMessageType[]>([
        {
            role: 'assistant',
            content: "Hello! I'm your Niyogen Assistant (Australia). I'm here to help you find the best prices and deals in Coles, Woolworths, and more. Ask me about any product!",
        },
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/login');
        }
    }, [user, authLoading, router]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    const handleSendMessage = async (text: string) => {
        const userMessage: ChatMessageType = {
            role: 'user',
            content: text,
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        try {
            const result = await apiService.sendMessage(text);
            const assistantMessage: ChatMessageType = {
                role: 'assistant',
                content: result.response,
                metadata: result.metadata
            };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error: any) {
            const errorMessage: ChatMessageType = {
                role: 'assistant',
                content: `Error: ${error.response?.data?.detail || error.message || 'Failed to send message'}`,
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    if (authLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!user) {
        return null;
    }

    return (
        <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
            <Header />

            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Ads Section */}
                <div className="p-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                    <div className="max-w-4xl mx-auto">
                        <AdsCarousel />
                    </div>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 overflow-y-auto p-4">
                    <div className="max-w-4xl mx-auto">
                        {messages.map((message, index) => (
                            <ChatMessage key={index} message={message} />
                        ))}
                        {isLoading && <TypingIndicator />}
                        <div ref={messagesEndRef} />
                    </div>
                </div>

                {/* Chat Input */}
                <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
            </div>
        </div>
    );
}
