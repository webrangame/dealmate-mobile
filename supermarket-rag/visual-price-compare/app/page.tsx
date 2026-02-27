'use client';

import { useState } from 'react';

interface Match {
  product_name: string;
  coles_price: string;
  ww_price: string;
  unit: string;
}

interface Results {
  matches: Match[];
  summary: string;
  screenshots: {
    coles: string | null;
    woolworths: string | null;
  };
}

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Results | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showVisuals, setShowVisuals] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt) return;

    setLoading(true);
    setResults(null);
    setError(null);

    try {
      const response = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data);
      }
    } catch (err: any) {
      setError('An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0b] text-white p-8 font-[family-name:var(--font-geist-sans)]">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-5xl font-extrabold mb-4 bg-gradient-to-r from-red-500 via-white to-green-500 bg-clip-text text-transparent">
            Supermarket Visual Compare
          </h1>
          <p className="text-gray-400 text-lg">Compare prices visually across Coles and Woolworths using AI</p>
        </header>

        <form onSubmit={handleSearch} className="mb-12 flex flex-col items-center gap-6">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. Compare the prices of ice cream at Coles and Woolworths..."
            className="w-full max-w-2xl px-6 py-4 h-32 rounded-2xl bg-[#161617] border border-gray-800 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all text-lg resize-none"
          />
          <button
            type="submit"
            disabled={loading}
            className={`px-8 py-4 rounded-xl font-bold text-lg transition-all ${loading
              ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
              : 'bg-white text-black hover:bg-red-500 hover:text-white transform hover:scale-105 active:scale-95'
              }`}
          >
            {loading ? 'Analyzing...' : 'Compare'}
          </button>
        </form>

        {loading && (
          <div className="flex flex-col items-center justify-center space-y-4 py-20">
            <div className="w-16 h-16 border-4 border-red-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-gray-400 animate-pulse">Launching browsers and analyzing screenshots...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-900/20 border border-red-500/50 p-6 rounded-2xl mb-8 text-center text-red-200">
            <p className="font-bold mb-1">Comparison Failed</p>
            <p className="text-sm opacity-80">{error}</p>
          </div>
        )}

        {results && (
          <div className="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Summary Banner */}
            <div className="bg-[#161617] p-8 rounded-3xl border border-gray-800">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <span className="text-red-500">AI Summary</span>
              </h2>
              <p className="text-gray-300 text-lg leading-relaxed">{results.summary}</p>
            </div>

            {/* Comparison Table */}
            <div className="overflow-hidden rounded-3xl border border-gray-800 bg-[#161617]">
              <table className="w-full text-left">
                <thead className="bg-[#1c1c1d] text-gray-400 uppercase text-xs font-bold tracking-wider">
                  <tr>
                    <th className="px-8 py-4">Product Name</th>
                    <th className="px-8 py-4 text-red-400">Coles</th>
                    <th className="px-8 py-4 text-green-400">Woolworths</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800">
                  {results.matches.map((item, i) => (
                    <tr key={i} className="hover:bg-[#1c1c1d] transition-colors group">
                      <td className="px-8 py-6 font-medium text-gray-200">{item.product_name}</td>
                      <td className="px-8 py-6 text-red-400 font-bold">{item.coles_price}</td>
                      <td className="px-8 py-6 text-green-400 font-bold">{item.ww_price}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Visual Evidence Toggle */}
            <div className="flex justify-center">
              <button
                onClick={() => setShowVisuals(!showVisuals)}
                className="text-gray-500 hover:text-white transition-colors text-sm font-medium flex items-center gap-2"
              >
                {showVisuals ? 'Hide Visual Evidence' : 'Show Visual Evidence'}
              </button>
            </div>

            {/* Visual Evidence */}
            {showVisuals && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-in fade-in zoom-in-95 duration-300">
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-center text-red-500 uppercase tracking-widest text-sm">Coles Evidence</h3>
                  <div className="aspect-video bg-[#161617] rounded-3xl border border-gray-800 overflow-hidden flex items-center justify-center text-gray-500 relative">
                    {results.screenshots.coles ? (
                      <img
                        src={results.screenshots.coles}
                        alt="Coles search results"
                        className="w-full h-full object-cover object-top hover:scale-110 transition-transform duration-500 cursor-zoom-in"
                        onClick={() => window.open(results.screenshots.coles!, '_blank')}
                      />
                    ) : (
                      <p className="p-4 text-center text-xs">Snapshot unavailable</p>
                    )}
                  </div>
                </div>
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-center text-green-500 uppercase tracking-widest text-sm">Woolworths Evidence</h3>
                  <div className="aspect-video bg-[#161617] rounded-3xl border border-gray-800 overflow-hidden flex items-center justify-center text-gray-500 relative">
                    {results.screenshots.woolworths ? (
                      <img
                        src={results.screenshots.woolworths}
                        alt="Woolworths search results"
                        className="w-full h-full object-cover object-top hover:scale-110 transition-transform duration-500 cursor-zoom-in"
                        onClick={() => window.open(results.screenshots.woolworths!, '_blank')}
                      />
                    ) : (
                      <p className="p-4 text-center text-xs">Snapshot unavailable</p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
