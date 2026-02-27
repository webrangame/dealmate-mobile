import { useState, useRef, useEffect } from 'react'
import '../App.css'

function ChatInterface({ apiKey, apiUrl }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I\'m your LiteLLM assistant. How can I help you today?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedModel, setSelectedModel] = useState('gemini-2.5-pro')
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  const models = [
    'gemini-2.5-pro',
    'gemini-2.5-flash',
    'gemini-2.0-flash',
    'gemini-pro',
    'gemini-1.5-pro',
    'gemini-1.5-flash'
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading || !apiKey) return

    const userMessage = { role: 'user', content: input }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${apiUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: selectedModel,
          messages: newMessages.map(msg => ({
            role: msg.role,
            content: msg.content
          })),
          temperature: 0.7,
          max_tokens: 1000,
        }),
      })

      if (!response.ok) {
        let errorData
        try {
          errorData = await response.json()
        } catch {
          const errorText = await response.text()
          errorData = { error: { message: errorText } }
        }
        throw new Error(errorData.error?.message || errorData.message || `API Error: ${response.statusText}`)
      }

      const data = await response.json()
      const assistantMessage = {
        role: 'assistant',
        content: data.choices[0].message.content
      }
      
      setMessages([...newMessages, assistantMessage])
    } catch (err) {
      setError(err.message)
      setMessages([...newMessages, {
        role: 'assistant',
        content: `Error: ${err.message}`
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div style={{ 
      flex: 1, 
      display: 'flex', 
      flexDirection: 'column',
      background: '#f5f5f5',
      minHeight: 'calc(100vh - 300px)'
    }}>
      <div className="container" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Model Selector */}
        <div style={{ 
          marginBottom: '16px', 
          display: 'flex', 
          alignItems: 'center',
          gap: '12px'
        }}>
          <label style={{ fontWeight: '600', color: '#333' }}>Model:</label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="input"
            style={{ width: 'auto', minWidth: '200px' }}
            disabled={loading}
          >
            {models.map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>
        </div>

        {/* Messages */}
        <div style={{
          flex: 1,
          background: 'white',
          borderRadius: '12px',
          padding: '20px',
          overflowY: 'auto',
          marginBottom: '16px',
          minHeight: '400px',
          maxHeight: '600px'
        }}>
          {messages.map((message, index) => (
            <div
              key={index}
              style={{
                marginBottom: '16px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: message.role === 'user' ? 'flex-end' : 'flex-start'
              }}
            >
              <div style={{
                background: message.role === 'user' 
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
                  : '#f0f0f0',
                color: message.role === 'user' ? 'white' : '#333',
                padding: '12px 16px',
                borderRadius: '12px',
                maxWidth: '70%',
                wordWrap: 'break-word'
              }}>
                <div style={{ 
                  fontSize: '12px', 
                  opacity: 0.8, 
                  marginBottom: '4px',
                  fontWeight: '600'
                }}>
                  {message.role === 'user' ? 'You' : 'Assistant'}
                </div>
                <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '8px',
              color: '#666'
            }}>
              <div style={{
                width: '16px',
                height: '16px',
                border: '2px solid #667eea',
                borderTop: '2px solid transparent',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite'
              }}></div>
              <span>Thinking...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {error && (
          <div className="error" style={{ marginBottom: '16px' }}>
            {error}
          </div>
        )}

        {/* Input */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <input
            type="text"
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message... (Press Enter to send)"
            disabled={loading || !apiKey}
            style={{ flex: 1 }}
          />
          <button
            onClick={sendMessage}
            className="button"
            disabled={loading || !input.trim() || !apiKey}
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>

        {!apiKey && (
          <div className="error" style={{ marginTop: '16px' }}>
            No API key available. Please login first.
          </div>
        )}
      </div>

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default ChatInterface
