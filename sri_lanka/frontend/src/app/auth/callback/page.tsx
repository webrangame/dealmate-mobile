'use client';

import { useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

function AuthCallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();

    useEffect(() => {
        const params = Object.fromEntries(searchParams.entries());
        console.log('[AuthCallback] Received params:', params);

        const accessToken = searchParams.get('accessToken');
        const refreshToken = searchParams.get('refreshToken');
        const email = searchParams.get('email');
        const name = searchParams.get('name');
        const userId = searchParams.get('userId');
        const redirect = searchParams.get('redirect') || '/chat';

        if (accessToken && userId && email) {
            console.log('[AuthCallback] Found all necessary auth data, establishing session...');
            // Construct user object
            const user = {
                id: userId,
                email: email,
                name: name || email.split('@')[0],
            };

            // Store in localStorage
            localStorage.setItem('user', JSON.stringify(user));
            // Store tokens if they exist
            if (accessToken) localStorage.setItem('accessToken', accessToken);
            if (refreshToken) localStorage.setItem('refreshToken', refreshToken);

            // Redirect to the intended page
            router.push(redirect);
        } else {
            // Handle error case
            console.error('[AuthCallback] Missing auth data in callback. Expected accessToken, userId, and email.', {
                hasAccessToken: !!accessToken,
                hasUserId: !!userId,
                hasEmail: !!email
            });
            router.push('/login?error=auth_failed');
        }
    }, [searchParams, router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
            <div className="text-center">
                <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Completing Sign In...</h2>
                <p className="text-gray-600 dark:text-gray-400 mt-2">Please wait while we set up your session.</p>
            </div>
        </div>
    );
}

export default function AuthCallbackPage() {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
                <div className="text-center">
                    <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Loading...</h2>
                </div>
            </div>
        }>
            <AuthCallbackContent />
        </Suspense>
    );
}
