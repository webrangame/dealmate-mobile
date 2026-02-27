'use client';

import { useState, useEffect } from 'react';
import { VendorAd } from '@/types';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const ads: VendorAd[] = [
    {
        store: 'Pizza Hut',
        offer: 'Buy 1 Get 1 Free',
        color: '#E31837',
        image: '/images/pizza_hut_ad.png',
    },
    {
        store: 'Coca-Cola',
        offer: 'Refresh Your Day',
        color: '#F40009',
        image: '/images/coca_cola_ad.png',
    },
    {
        store: 'Coles',
        offer: 'Super Offer',
        color: '#EF4444',
    },
    {
        store: 'Woolworths',
        offer: 'Fresh Deals',
        color: '#10B981',
    },
    {
        store: 'Aldi',
        offer: 'Special Buys',
        color: '#3B82F6',
    },
    {
        store: 'IGA',
        offer: 'Local Low Prices',
        color: '#F97316',
    },
];

export default function AdsCarousel() {
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentIndex((prev) => (prev + 1) % ads.length);
        }, 4000);

        return () => clearInterval(interval);
    }, []);

    const goToPrevious = () => {
        setCurrentIndex((prev) => (prev - 1 + ads.length) % ads.length);
    };

    const goToNext = () => {
        setCurrentIndex((prev) => (prev + 1) % ads.length);
    };

    const currentAd = ads[currentIndex];

    return (
        <div className="relative h-24 rounded-xl overflow-hidden group">
            {/* Ad Card */}
            <div
                className="absolute inset-0 transition-all duration-500"
                style={{
                    background: `linear-gradient(135deg, ${currentAd.color}dd, ${currentAd.color})`,
                }}
            >
                <div className="relative h-full p-4 flex items-center justify-between">
                    <div className="flex-1">
                        <h3 className="text-white font-bold text-lg drop-shadow-lg">
                            {currentAd.store}
                        </h3>
                        <p className="text-white/90 text-sm drop-shadow">{currentAd.offer}</p>
                    </div>
                    <div className="bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-white/30">
                        <span className="text-white text-xs font-semibold drop-shadow">
                            View Catalogue
                        </span>
                    </div>
                </div>
            </div>

            {/* Navigation Buttons */}
            <button
                onClick={goToPrevious}
                className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
            >
                <ChevronLeft className="w-5 h-5 text-white" />
            </button>
            <button
                onClick={goToNext}
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
            >
                <ChevronRight className="w-5 h-5 text-white" />
            </button>

            {/* Indicators */}
            <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-1.5">
                {ads.map((_, index) => (
                    <button
                        key={index}
                        onClick={() => setCurrentIndex(index)}
                        className={`w-1.5 h-1.5 rounded-full transition-all ${index === currentIndex
                                ? 'bg-white w-4'
                                : 'bg-white/50 hover:bg-white/75'
                            }`}
                    />
                ))}
            </div>
        </div>
    );
}
