'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Lock, ShieldCheck, ArrowRight, Zap } from 'lucide-react';

export default function LoginPage() {
    const router = useRouter();

    const handleAgentHubSignIn = () => {
        const origin = window.location.origin;
        // The redirect parameter should be the final destination (/chat), not the callback page itself.
        // The marketplace sign-in logic already knows to send tokens to ${origin}/auth/callback 
        // based on the 'origin' parameter, and then redirect to the 'redirect' parameter.
        const finalRedirect = '/chat';
        window.location.href = `https://market.niyogen.com/signin?redirect=${encodeURIComponent(finalRedirect)}&origin=${encodeURIComponent(origin)}`;
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#020617] p-4 relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[128px] pointer-events-none" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[128px] pointer-events-none" />

            <div className="w-full max-w-md z-10">
                {/* Gateway Card */}
                <div className="bg-slate-900/40 border border-slate-800/50 backdrop-blur-xl rounded-[2.5rem] p-10 shadow-2xl relative overflow-hidden">
                    {/* Header Icon */}
                    <div className="flex justify-center mb-8">
                        <div className="p-4 bg-blue-500/10 rounded-3xl border border-blue-500/20 relative group">
                            <div className="absolute inset-0 bg-blue-500/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
                            <Lock className="w-10 h-10 text-blue-400 relative z-10" />
                        </div>
                    </div>

                    {/* Text */}
                    <div className="text-center space-y-3 mb-10">
                        <h1 className="text-3xl font-bold text-white tracking-tight">
                            FastGraph <span className="text-blue-400">Gateway</span>
                        </h1>
                        <p className="text-slate-400 text-sm leading-relaxed max-w-[240px] mx-auto">
                            Sign in to access the platform. You will be redirected to sign in on <span className="text-slate-200 font-semibold">AgentHub</span>.
                        </p>
                    </div>

                    {/* Action Button */}
                    <button
                        onClick={handleAgentHubSignIn}
                        className="group w-full bg-[#2563eb] hover:bg-[#1d4ed8] text-white font-bold py-5 px-6 rounded-2xl shadow-xl shadow-blue-500/20 transition-all flex items-center justify-between overflow-hidden relative"
                    >
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                        <div className="flex items-center gap-3 relative z-10">
                            <ShieldCheck className="w-5 h-5 text-blue-200" />
                            <span className="text-lg">Sign In with AgentHub</span>
                        </div>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-2 transition-transform relative z-10" />
                    </button>

                    {/* Footer Info */}
                    <div className="mt-10 pt-8 border-t border-slate-800/50 flex flex-col items-center gap-4">
                        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] bg-slate-800/30 px-4 py-2 rounded-full border border-slate-700/50">
                            <ShieldCheck className="w-3 h-3 text-blue-400" />
                            <span>Enterprise Secure Link</span>
                        </div>
                        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-400">
                            <Zap className="w-3 h-3 text-amber-400" />
                            <span>Powered by Niyogen AI</span>
                        </div>
                    </div>
                </div>

                {/* Bottom Link */}
                <div className="mt-8 text-center">
                    <p className="text-slate-500 text-xs">
                        By signing in, you agree to our{' '}
                        <a href="https://market.niyogen.com/terms" className="text-blue-400/80 hover:text-blue-400 transition-colors underline decoration-blue-400/20 underline-offset-4">Terms of Service</a>
                    </p>
                </div>
            </div>
        </div>
    );
}
