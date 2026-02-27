"use client";

import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Upload, Send, FileText, ShoppingCart, Loader2 } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [messages, setMessages] = useState<{ role: "user" | "bot"; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [userId, setUserId] = useState("user_123"); // Default or fetched user id
  const [isQuerying, setIsQuerying] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isQuerying) return;

    const userMessage = input;
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsQuerying(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, { 
        text: userMessage,
        user_id: userId 
      });
      setMessages(prev => [...prev, { role: "bot", content: response.data.response }]);
    } catch (error) {
      console.error("Query failed", error);
      setMessages(prev => [...prev, { role: "bot", content: "Sorry, I encountered an error while processing your request." }]);
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <div className="logo">
          <ShoppingCart style={{ display: "inline", marginRight: "0.5rem" }} />
          Supermarket AI Assistant
        </div>
        <div className="status-badge">Gemini Powered</div>
      </header>

      <main className="main-content">


        <section className="card chat-section">
          <div className="chat-messages">
            {messages.length === 0 && (
              <div style={{ textAlign: "center", marginTop: "4rem", color: "var(--text-dim)" }}>
                <Send size={48} style={{ margin: "0 auto 1rem", opacity: 0.2 }} />
                <p>How can I help you with supermarket shopping today?</p>
                <p style={{ fontSize: "0.875rem" }}>Try asking "Where is the cheapest ice cream?"</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                {m.content}
              </div>
            ))}
            {isQuerying && (
              <div className="message bot">
                <Loader2 className="animate-spin" size={20} />
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <form className="chat-input-area" onSubmit={handleSendMessage}>
            <div className="user-id-wrapper" style={{ marginRight: "0.5rem", borderRight: "1px solid var(--border)", paddingRight: "0.5rem" }}>
              <input
                type="text"
                placeholder="User ID"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                style={{ width: "80px", border: "none", fontSize: "0.75rem", background: "transparent" }}
                title="LiteLLM User ID"
              />
            </div>
            <input
              type="text"
              placeholder="Ask a question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isQuerying}
            />
            <button type="submit" disabled={isQuerying || !input.trim()}>
              <Send size={20} />
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}
