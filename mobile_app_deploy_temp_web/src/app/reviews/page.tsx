'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { apiService } from '@/lib/api';
import { Review } from '@/types';
import Header from '@/components/layout/Header';
import ReviewsList from '@/components/reviews/ReviewsList';
import ReviewForm from '@/components/reviews/ReviewForm';
import { ChevronLeft, MessageSquare, AlertCircle } from 'lucide-react';
import Link from 'next/link';

export default function ReviewsPage() {
    const { user, isLoading: authLoading } = useAuth();
    const router = useRouter();
    const [reviews, setReviews] = useState<Review[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/login');
        }
    }, [user, authLoading, router]);

    useEffect(() => {
        fetchReviews();
    }, []);

    const fetchReviews = async () => {
        try {
            setIsLoading(true);
            const data = await apiService.fetchReviews();
            setReviews(data);
        } catch (err: any) {
            setError('Failed to load reviews. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleReviewSubmit = async (rating: number, comment: string) => {
        try {
            setIsSubmitting(true);
            setError('');
            await apiService.submitReview(rating, comment);
            await fetchReviews(); // Refresh list
        } catch (err: any) {
            setError(err.message || 'Failed to submit review. Are you logged in?');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (authLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!user) return null;

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
            <Header />

            <main className="flex-1 max-w-4xl mx-auto w-full p-4 md:p-8 space-y-8">
                {/* Back Link */}
                <Link
                    href="/chat"
                    className="inline-flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                >
                    <ChevronLeft className="w-5 h-5" />
                    Back to Chat
                </Link>

                {/* Hero Section */}
                <div className="text-center space-y-3">
                    <div className="inline-flex items-center justify-center p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-2">
                        <MessageSquare className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                    </div>
                    <h1 className="text-3xl font-bold font-outfit text-gray-900 dark:text-white">
                        Community Feedback
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400 max-w-lg mx-auto">
                        Your feedback helps us improve the Price Comparison Agent. Share your thoughts with the community!
                    </p>
                </div>

                {/* Error Alert */}
                {error && (
                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-center gap-3 text-red-800 dark:text-red-200">
                        <AlertCircle className="w-5 h-5 flex-shrink-0" />
                        <p className="text-sm font-medium">{error}</p>
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
                    {/* Review Form Area */}
                    <div className="md:col-span-2">
                        <div className="sticky top-8">
                            <ReviewForm onSubmit={handleReviewSubmit} isLoading={isSubmitting} />
                        </div>
                    </div>

                    {/* Reviews List Area */}
                    <div className="md:col-span-3">
                        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                            Recent Reviews
                            <span className="bg-gray-200 dark:bg-gray-800 text-sm font-medium px-2 py-0.5 rounded-full">
                                {reviews.length}
                            </span>
                        </h2>

                        {isLoading ? (
                            <div className="space-y-4">
                                {[...Array(3)].map((_, i) => (
                                    <div key={i} className="h-40 glass rounded-xl animate-pulse" />
                                ))}
                            </div>
                        ) : (
                            <ReviewsList reviews={reviews} />
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
