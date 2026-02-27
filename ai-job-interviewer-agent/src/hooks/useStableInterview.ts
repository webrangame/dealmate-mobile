'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

export function useStableInterview(jd: string, cv: string) {
    const [isConnected, setIsConnected] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [transcript, setTranscript] = useState<{ role: string; text: string }[]>([]);
    const [isListening, setIsListening] = useState(false);

    const messagesRef = useRef<{ role: string; content: string }[]>([]);
    const recognitionRef = useRef<any>(null);
    const synthRef = useRef<SpeechSynthesis | null>(null);

    // AI Call via LiteLLM Proxy
    const callLiteLLM = async (messages: { role: string; content: string }[]) => {
        const API_URL = process.env.NEXT_PUBLIC_LITELLM_API_URL;
        const API_KEY = process.env.NEXT_PUBLIC_LITELLM_API_KEY;

        if (!API_URL || !API_KEY) {
            throw new Error("LiteLLM configuration missing in .env.local");
        }

        const response = await fetch(`${API_URL}/v1/chat/completions`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: "gemini-2.0-flash",
                messages: messages
            })
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error?.message || `API Error: ${response.status}`);
        }

        const data = await response.json();
        return data.choices[0].message.content;
    };

    // Initialize Brain
    const initBrain = useCallback(async () => {
        try {
            const systemPrompt = `You are a professional Human Resources (HR) Interviewer. 
      Your goal is to conduct an HR interview for the following Job Description (JD) and Candidate CV.
      
      JOB DESCRIPTION:
      ${jd}
      
      CANDIDATE CV:
      ${cv}
      
      STRICT INSTRUCTIONS:
      - Assume the persona of a professional, empathetic, yet thorough HR manager.
      - Focus on HR-related topics: cultural fit, behavioral questions, soft skills, career aspirations, and compensation expectations.
      - Reference specific details from the Candidate CV and how they align (or don't align) with the JD.
      - Ask exactly ONE question at a time.
      - Wait for the candidate's response before proceeding.
      - Follow up naturally based on their answers.
      - Start by introducing yourself as Aoede from HR and asking the candidate to introduce themselves and explain why they are interested in this role.`;

            messagesRef.current = [
                { role: "system", content: systemPrompt }
            ];

            setIsConnected(true);

            // Get initial greeting from AI
            try {
                const responseText = await callLiteLLM([
                    ...messagesRef.current,
                    { role: "user", content: "Start the HR interview." }
                ]);

                messagesRef.current.push({ role: "assistant", content: responseText });
                handleAiResponse(responseText);
            } catch (e: any) {
                console.error("Initial message failed:", e);
                setError(`AI initialization failed: ${e?.message || "Connection Error"}`);
            }

        } catch (err) {
            console.error("Brain init error:", err);
            setError("Failed to initialize AI HR interviewer.");
        }
    }, [jd, cv]);

    // Handle AI Response (Text + TTS)
    const handleAiResponse = (text: string) => {
        setTranscript(prev => [...prev, { role: 'ai', text }]);
        speak(text);
    };

    // TTS Logic
    const speak = (text: string) => {
        if (!synthRef.current) return;
        synthRef.current.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        const voices = synthRef.current.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Google') || v.name.includes('Premium')) || voices[0];
        if (preferredVoice) utterance.voice = preferredVoice;

        utterance.rate = 1.0;
        utterance.onend = () => {
            startListening();
        };

        synthRef.current.speak(utterance);
    };

    const startListening = () => {
        if (recognitionRef.current && !isListening) {
            try {
                recognitionRef.current.start();
                setIsListening(true);
            } catch (e) {
                console.warn("Recognition start error:", e);
            }
        }
    };

    const stopListening = () => {
        if (recognitionRef.current && isListening) {
            recognitionRef.current.stop();
            setIsListening(false);
        }
    };

    useEffect(() => {
        if (typeof window !== 'undefined') {
            const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
            if (SpeechRecognition) {
                const recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onresult = async (event: any) => {
                    const speechToText = event.results[0][0].transcript;
                    setTranscript(prev => [...prev, { role: 'user', text: speechToText }]);
                    setIsListening(false);

                    try {
                        const newMessages = [
                            ...messagesRef.current,
                            { role: "user", content: speechToText }
                        ];
                        const responseText = await callLiteLLM(newMessages);

                        messagesRef.current.push({ role: "user", content: speechToText });
                        messagesRef.current.push({ role: "assistant", content: responseText });
                        handleAiResponse(responseText);
                    } catch (err) {
                        setError("AI connection lost. Please refresh.");
                    }
                };

                recognition.onerror = () => setIsListening(false);
                recognitionRef.current = recognition;
            } else {
                setError("Speech recognition unsupported in this browser.");
            }
            synthRef.current = window.speechSynthesis;
        }

        return () => {
            if (synthRef.current) synthRef.current.cancel();
            stopListening();
        };
    }, []);

    useEffect(() => {
        if (jd && cv && !isConnected) {
            initBrain();
        }
    }, [jd, cv, isConnected, initBrain]);

    return {
        isConnected,
        error,
        transcript,
        isListening,
        startListening,
        stopListening
    };
}
