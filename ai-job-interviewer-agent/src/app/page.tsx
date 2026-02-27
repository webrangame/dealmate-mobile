'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Briefcase, Send, Sparkles, Wand2 } from 'lucide-react';

export default function Home() {
  const [jd, setJd] = useState('');
  const [cv, setCv] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const handleStartInterview = async () => {
    if (!jd.trim() || !cv.trim()) return;
    setIsSubmitting(true);

    // Save JD and CV to localStorage for use in the interview page
    localStorage.setItem('job_description', jd);
    localStorage.setItem('candidate_cv', cv);

    // Simulate a small delay for "AI preparation" effect
    setTimeout(() => {
      router.push('/interview');
    }, 1500);
  };

  return (
    <main className="flex flex-col items-center justify-center min-vh-100 p-6 md:p-24 relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[128px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-amber-600/10 rounded-full blur-[128px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="z-10 w-full max-w-4xl space-y-8"
      >
        <div className="text-center space-y-4">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, type: 'spring' }}
            className="flex justify-center"
          >
            <div className="p-3 bg-blue-600/10 rounded-2xl border border-blue-500/20">
              <Sparkles className="w-10 h-10 text-blue-400" />
            </div>
          </motion.div>

          <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-white">
            AI <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-amber-400">HR Interviewer</span>
          </h1>
          <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto">
            Professional HR agent that evaluates candidates based on their CV and specific job requirements.
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="glass rounded-3xl p-8 space-y-6 relative overflow-hidden"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <div className="flex items-center gap-3 text-blue-400 mb-2">
                <Briefcase className="w-5 h-5" />
                <span className="font-semibold uppercase tracking-wider text-sm">Job Description (JD)</span>
              </div>
              <div className="relative group">
                <textarea
                  value={jd}
                  onChange={(e) => setJd(e.target.value)}
                  placeholder="Paste the Job Description here..."
                  className="w-full h-64 bg-slate-900/50 border border-slate-700/50 rounded-2xl p-6 text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all resize-none"
                />
                <div className="absolute inset-0 bg-blue-500/5 opacity-0 group-focus-within:opacity-100 pointer-events-none transition-opacity rounded-2xl" />
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center gap-3 text-amber-400 mb-2">
                <Wand2 className="w-5 h-5" />
                <span className="font-semibold uppercase tracking-wider text-sm">Candidate CV / Resume</span>
              </div>
              <div className="relative group">
                <textarea
                  value={cv}
                  onChange={(e) => setCv(e.target.value)}
                  placeholder="Paste the Candidate's CV or Resume text here..."
                  className="w-full h-64 bg-slate-900/50 border border-slate-700/50 rounded-2xl p-6 text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 transition-all resize-none"
                />
                <div className="absolute inset-0 bg-amber-500/5 opacity-0 group-focus-within:opacity-100 pointer-events-none transition-opacity rounded-2xl" />
              </div>
            </div>
          </div>

          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="flex items-center gap-2 text-slate-500 text-sm">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <span>HR Agent will tailor behavioral questions based on these documents</span>
            </div>

            <button
              onClick={handleStartInterview}
              disabled={!jd.trim() || !cv.trim() || isSubmitting}
              className={`
                px-8 py-4 rounded-xl font-bold transition-all flex items-center gap-2
                ${jd.trim() && cv.trim() && !isSubmitting
                  ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/25 scale-100 hover:scale-105 active:scale-95'
                  : 'bg-slate-800 text-slate-500 cursor-not-allowed opacity-50'}
              `}
            >
              {isSubmitting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Preparing Agent...</span>
                </>
              ) : (
                <>
                  <span>Start Live Interview</span>
                  <Send className="w-5 h-5" />
                </>
              )}
            </button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8">
          {[
            { title: 'Real-time Voice', desc: 'Natural voice interaction with low latency' },
            { title: 'Dynamic Questions', desc: 'Questions tailored specifically to the JD provided' },
            { title: 'Performance Labs', desc: 'Get detailed feedback on your answers' }
          ].map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 + (i * 0.1) }}
              className="p-6 rounded-2xl border border-slate-800/50 bg-slate-900/20"
            >
              <h3 className="text-blue-400 font-semibold mb-1">{feature.title}</h3>
              <p className="text-slate-500 text-sm">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </main>
  );
}
