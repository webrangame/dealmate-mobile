'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, PhoneOff, MessageSquare, Volume2, ShieldCheck, AlertCircle, Wand2 } from 'lucide-react';
import { useStableInterview } from '@/hooks/useStableInterview';

export default function InterviewPage() {
    const router = useRouter();
    const [jd, setJd] = useState('');
    const [cv, setCv] = useState('');
    const [showTranscript, setShowTranscript] = useState(false);
    const transcriptEndRef = useRef<HTMLDivElement>(null);

    // Initialize JD and CV from localStorage
    useEffect(() => {
        const savedJd = localStorage.getItem('job_description');
        const savedCv = localStorage.getItem('candidate_cv');
        if (!savedJd || !savedCv) {
            router.push('/');
            return;
        }
        setJd(savedJd);
        setCv(savedCv);
    }, [router]);

    const { isConnected, error, transcript, isListening, startListening, stopListening } = useStableInterview(jd, cv);

    useEffect(() => {
        transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [transcript]);

    const handleEndInterview = () => {
        router.push('/');
    };

    return (
        <main className="flex flex-col h-screen bg-[#020617] text-slate-200 overflow-hidden">
            {/* Header */}
            <header className="flex items-center justify-between p-6 border-b border-slate-800/50 bg-slate-900/20 backdrop-blur-md">
                <div className="flex items-center gap-4">
                    <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-amber-500'}`} />
                    <div>
                        <h2 className="font-bold text-lg text-white">Interview Session</h2>
                        <p className="text-xs text-slate-500 uppercase tracking-widest font-semibold">
                            {isConnected ? 'Agent Aoede Active' : 'Initializing Agent...'}
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs text-nowrap">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        <span>Secure Voice Link</span>
                    </div>
                    <button
                        onClick={handleEndInterview}
                        className="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-600/10 hover:bg-red-600 text-red-500 hover:text-white border border-red-500/20 transition-all font-semibold text-sm"
                    >
                        <PhoneOff className="w-4 h-4" />
                        <span>Quit</span>
                    </button>
                </div>
            </header>

            {/* Main Content */}
            <div className="flex-1 flex flex-col md:flex-row overflow-hidden relative">

                {/* Visualizer Area */}
                <div className={`flex-1 flex flex-col items-center justify-center p-8 transition-all ${showTranscript ? 'md:w-2/3' : 'w-full'}`}>
                    <div className="relative w-64 h-64 flex items-center justify-center">
                        {/* Animated Rings - Pulse when AI speaks or user speaks */}
                        {[...Array(3)].map((_, i) => (
                            <motion.div
                                key={i}
                                initial={{ scale: 1, opacity: 0.5 }}
                                animate={{
                                    scale: (isListening || (transcript.length > 0 && transcript[transcript.length - 1].role === 'ai')) ? [1, 1.3, 1] : 1,
                                    opacity: (isListening || (transcript.length > 0 && transcript[transcript.length - 1].role === 'ai')) ? [0.5, 0.1, 0.5] : 0.2
                                }}
                                transition={{ duration: 2, repeat: Infinity, delay: i * 0.4 }}
                                className="absolute inset-0 border-2 border-blue-500/30 rounded-full"
                            />
                        ))}

                        <motion.div
                            animate={{ scale: isListening ? [1, 1.1, 1] : 1 }}
                            transition={{ duration: 1, repeat: Infinity }}
                            className={`w-48 h-48 rounded-full shadow-2xl flex items-center justify-center text-white transition-all duration-500 ${isListening ? 'bg-gradient-to-tr from-green-600 to-emerald-600' : 'bg-gradient-to-tr from-blue-600 to-indigo-600'
                                }`}
                        >
                            {isListening ? (
                                <Mic className="w-16 h-16 animate-pulse" />
                            ) : (
                                <Volume2 className="w-16 h-16 opacity-80" />
                            )}
                        </motion.div>
                    </div>

                    <div className="mt-12 text-center space-y-2">
                        <h3 className="text-xl font-medium text-white italic min-h-[1.75rem]">
                            {isListening ? "Listening to you..." :
                                isConnected ? (transcript.length > 0 && transcript[transcript.length - 1].role === 'ai' ? "Aoede is speaking..." : "Waiting to start...") :
                                    "Connecting to Brain..."}
                        </h3>
                        <p className="text-slate-500 text-sm max-w-md mx-auto">
                            {isListening
                                ? "Speak your answer clearly. Aoede will listen until you stop talking."
                                : "Aoede will ask a question. Listen carefully and click the mic to answer if it doesn't auto-start."}
                        </p>
                    </div>

                    {error && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="mt-8 flex items-center gap-3 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400"
                        >
                            <AlertCircle className="w-5 h-5" />
                            <span>{error}</span>
                        </motion.div>
                    )}

                    {!isListening && isConnected && (
                        <motion.button
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            onClick={startListening}
                            className="mt-8 flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 rounded-full font-bold text-white shadow-lg shadow-blue-500/20 transition-all scale-100 hover:scale-105 active:scale-95"
                        >
                            <Mic className="w-5 h-5" />
                            <span>Answer Now</span>
                        </motion.button>
                    )}
                </div>

                {/* Transcript Panel */}
                <AnimatePresence>
                    {showTranscript && (
                        <motion.div
                            initial={{ x: 300, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            exit={{ x: 300, opacity: 0 }}
                            className="w-full md:w-1/3 bg-slate-900/30 border-l border-slate-800/50 backdrop-blur-xl flex flex-col"
                        >
                            <div className="p-4 border-b border-slate-800/50 flex items-center justify-between">
                                <span className="font-semibold text-sm uppercase tracking-wider text-slate-400">Interview Log</span>
                                <button onClick={() => setShowTranscript(false)} className="text-slate-500 hover:text-white text-2xl">
                                    &times;
                                </button>
                            </div>
                            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                                {transcript.map((item, i) => (
                                    <div key={i} className={`flex flex-col ${item.role === 'ai' ? 'items-start' : 'items-end'}`}>
                                        <span className="text-[10px] uppercase font-bold text-slate-600 mb-1">{item.role === 'ai' ? 'Aoede' : 'You'}</span>
                                        <div className={`max-w-[85%] p-3 rounded-2xl text-sm ${item.role === 'ai' ? 'bg-slate-800 text-slate-200 rounded-tl-none' : 'bg-blue-600 text-white rounded-tr-none shadow-md shadow-blue-900/20'
                                            }`}>
                                            {item.text}
                                        </div>
                                    </div>
                                ))}
                                <div ref={transcriptEndRef} />
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Controls */}
            <footer className="p-8 flex items-center justify-center gap-6 bg-slate-900/40 backdrop-blur-xl border-t border-slate-800/50">
                <div className="flex items-center gap-4 bg-slate-800/30 p-2 rounded-2xl border border-slate-700/50">
                    <button
                        onClick={() => isListening ? stopListening() : startListening()}
                        className={`p-4 rounded-xl transition-all ${isListening
                            ? 'bg-red-500/20 border border-red-500/30 text-red-400 shadow-[0_0_15px_rgba(239,68,68,0.2)]'
                            : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
                            }`}
                        title={isListening ? "Stop Listening" : "Start Listening"}
                    >
                        {isListening ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
                    </button>

                    <button
                        onClick={() => setShowTranscript(!showTranscript)}
                        className={`p-4 rounded-xl transition-all ${showTranscript
                            ? 'bg-blue-500/20 border border-blue-500/30 text-blue-400'
                            : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
                            }`}
                        title="Toggle Transcript"
                    >
                        <MessageSquare className="w-6 h-6" />
                    </button>
                </div>

                <div className="hidden sm:flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] ml-4 bg-slate-900/50 px-4 py-2 rounded-full border border-slate-800/50">
                    <Wand2 className="w-3 h-3 text-blue-400" />
                    Gemini Stable AI
                </div>
            </footer>
        </main>
    );
}
