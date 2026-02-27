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
            let assistantMessage: ChatMessageType = {
                role: 'assistant',
                content: '',
            };

            // Temporary state to track the added assistant message index
            let messageIndex = -1;

            const stream = apiService.sendMessageStream(text);
            for await (const data of stream) {
                if (data.type === 'chunk') {
                    if (messageIndex === -1) {
                        setIsLoading(false); // Hide typing indicator once we have content
                        assistantMessage.content += data.content;
                        setMessages((prev) => {
                            messageIndex = prev.length;
                            return [...prev, { ...assistantMessage }];
                        });
                    } else {
                        assistantMessage.content += data.content;
                        setMessages((prev) => {
                            const newMessages = [...prev];
                            newMessages[messageIndex] = { ...assistantMessage };
                            return newMessages;
                        });
                    }
                } else if (data.type === 'done') {
                    assistantMessage = {
                        role: 'assistant',
                        content: data.response,
                        metadata: data.metadata
                    };
                    setMessages((prev) => {
                        const newMessages = [...prev];
                        if (messageIndex === -1) {
                            return [...prev, assistantMessage];
                        }
                        newMessages[messageIndex] = assistantMessage;
                        return newMessages;
                    });
                    setIsLoading(false);
                } else if (data.type === 'error') {
                    throw new Error(data.message);
                }
            }
        } catch (error: any) {
            console.error('Chat error:', error);
            const errorMessage: ChatMessageType = {
                role: 'assistant',
                content: `Error: ${error.message || 'Failed to send message'}`,
            };
            setMessages((prev) => [...prev, errorMessage]);
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
