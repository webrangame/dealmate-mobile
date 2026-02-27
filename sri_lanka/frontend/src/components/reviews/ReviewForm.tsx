'use client';

import { useState, FormEvent } from 'react';
import { Star, Send } from 'lucide-react';

interface ReviewFormProps {
    onSubmit: (rating: number, comment: string) => Promise<void>;
    isLoading: boolean;
}

export default function ReviewForm({ onSubmit, isLoading }: ReviewFormProps) {
    const [rating, setRating] = useState(5);
    const [hoverRating, setHoverRating] = useState(0);
    const [comment, setComment] = useState('');

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (comment.trim() && !isLoading) {
            onSubmit(rating, comment.trim());
            setComment('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="glass rounded-xl p-6 shadow-lg space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 text-center">
                Leave a Review
            </h3>

            {/* Star Rating */}
            <div className="flex justify-center gap-1">
                {[...Array(5)].map((_, i) => {
                    const starValue = i + 1;
                    const isActive = (hoverRating || rating) >= starValue;
                    return (
                        <button
                            key={i}
                            type="button"
                            onClick={() => setRating(starValue)}
                            onMouseEnter={() => setHoverRating(starValue)}
                            onMouseLeave={() => setHoverRating(0)}
                            className="p-1 focus:outline-none transition-transform hover:scale-110"
                            disabled={isLoading}
                        >
                            <Star
                                className={`w-8 h-8 ${isActive ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300 dark:text-gray-600'
                                    }`}
                            />
                        </button>
                    );
                })}
            </div>

            {/* Comment Input */}
            <div>
                <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    placeholder="Tell us what you think..."
                    rows={3}
                    className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none transition-all"
                    disabled={isLoading}
                    required
                />
            </div>

            {/* Submit Button */}
            <button
                type="submit"
                disabled={isLoading || !comment.trim()}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-md hover:shadow-lg transform hover:scale-[1.01] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
                {isLoading ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                    <>
                        <Send className="w-5 h-5" />
                        Submit Review
                    </>
                )}
            </button>
        </form>
    );
}
