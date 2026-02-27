'use client';

import { Review } from '@/types';
import { Star } from 'lucide-react';

interface ReviewsListProps {
    reviews: Review[];
}

export default function ReviewsList({ reviews }: ReviewsListProps) {
    if (reviews.length === 0) {
        return (
            <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400">No reviews yet. Be the first to leave one!</p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {reviews.map((review) => (
                <div key={review.id} className="glass rounded-xl p-6 shadow-sm">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <h4 className="font-semibold text-gray-900 dark:text-white">
                                {review.userName || 'Anonymous User'}
                            </h4>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                {new Date(review.createdAt).toLocaleDateString()}
                            </p>
                        </div>
                        <div className="flex gap-0.5">
                            {[...Array(5)].map((_, i) => (
                                <Star
                                    key={i}
                                    className={`w-4 h-4 ${i < review.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300 dark:text-gray-600'
                                        }`}
                                />
                            ))}
                        </div>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
                        {review.comment}
                    </p>
                </div>
            ))}
        </div>
    );
}
