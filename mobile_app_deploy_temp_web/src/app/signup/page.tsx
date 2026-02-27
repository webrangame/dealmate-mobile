'use client';

import { useRouter } from 'next/navigation';
import { UserPlus, ShieldCheck, ArrowRight, Zap } from 'lucide-react';

export default function SignupPage() {
    const router = useRouter();

    const handleAgentHubSignUp = () => {
        const origin = window.location.origin;
        // Redirect to centralized AgentHub (get-started or signin)
        window.location.href = `https://market.niyogen.com/signin?redirect=${encodeURIComponent(origin + '/auth/callback')}&origin=${encodeURIComponent(origin)}`;
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#020617] p-4 relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[128px] pointer-events-none" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[128px] pointer-events-none" />

            <div className="w-full max-w-md z-10">
                {/* Gateway Card */}
                <div className="bg-slate-900/40 border border-slate-800/50 backdrop-blur-xl rounded-[2.5rem] p-10 shadow-2xl relative overflow-hidden">
                    {/* Header Icon */}
                    <div className="flex justify-center mb-8">
                        <div className="p-4 bg-purple-500/10 rounded-3xl border border-purple-500/20 relative group">
                            <div className="absolute inset-0 bg-purple-500/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
                            <UserPlus className="w-10 h-10 text-purple-400 relative z-10" />
                        </div>
                    </div>

                    {/* Text */}
                    <div className="text-center space-y-3 mb-10">
                        <h1 className="text-3xl font-bold text-white tracking-tight">
                            FastGraph <span className="text-purple-400">Join</span>
                        </h1>
                        <p className="text-slate-400 text-sm leading-relaxed max-w-[240px] mx-auto">
                            Create an account to access the platform. You will be redirected to <span className="text-slate-200 font-semibold">AgentHub</span>.
                        </p>
                    </div>

                    {/* Action Button */}
                    <button
                        onClick={handleAgentHubSignUp}
                        className="group w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 px-6 rounded-2xl shadow-lg shadow-blue-500/25 transition-all flex items-center justify-between overflow-hidden relative"
                    >
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                        <span className="relative z-10">Sign Up with AgentHub</span>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform relative z-10" />
                    </button>

                    {/* Footer Info */}
                    <div className="mt-10 pt-8 border-t border-slate-800/50 flex flex-col items-center gap-4">
                        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] bg-slate-800/30 px-4 py-2 rounded-full border border-slate-700/50">
                            <ShieldCheck className="w-3 h-3 text-purple-400" />
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
                        Already have an account?{' '}
                        <a href="/login" className="text-blue-400/80 hover:text-blue-400 transition-colors underline decoration-blue-400/20 underline-offset-4">Sign in</a>
                    </p>
                </div>
            </div>
        </div>
    );
}
