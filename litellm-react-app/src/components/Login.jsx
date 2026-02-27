import { useState } from 'react'
import '../App.css'

function Login({ onLogin, onQuickStart, loading, error }) {
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    onLogin(username, password)
  }

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div className="card" style={{ maxWidth: '400px', width: '100%' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '24px' }}>
          🚅 LiteLLM Login
        </h2>
        
        <p style={{ 
          textAlign: 'center', 
          color: '#666', 
          marginBottom: '24px',
          fontSize: '14px'
        }}>
          Connect to LiteLLM Proxy
        </p>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '8px', 
              fontWeight: '600',
              color: '#333'
            }}>
              Username
            </label>
            <input
              type="text"
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
              disabled={loading}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '8px', 
              fontWeight: '600',
              color: '#333'
            }}>
              Password / Master Key
            </label>
            <input
              type="password"
              className="input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password or master key"
              required
              disabled={loading}
            />
            <p style={{ 
              fontSize: '12px', 
              color: '#999', 
              marginTop: '4px' 
            }}>
              Enter your LiteLLM master key (starts with 'sk-')
            </p>
            <p style={{ 
              fontSize: '11px', 
              color: '#999', 
              marginTop: '4px',
              fontStyle: 'italic'
            }}>
              Example: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
            </p>
          </div>

          <button 
            type="submit" 
            className="button"
            style={{ width: '100%' }}
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div style={{ marginTop: '16px', textAlign: 'center' }}>
          <div style={{ 
            marginBottom: '12px', 
            color: '#666', 
            fontSize: '14px',
            position: 'relative'
          }}>
            <span style={{ 
              display: 'block', 
              width: '100%', 
              height: '1px', 
              background: '#e0e0e0',
              marginBottom: '12px'
            }}></span>
            <span style={{ background: 'white', padding: '0 8px', position: 'relative', top: '-10px' }}>OR</span>
          </div>
          
          <button 
            type="button"
            onClick={onQuickStart}
            className="button"
            style={{ 
              width: '100%',
              background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
              opacity: loading ? 0.6 : 1
            }}
            disabled={loading}
          >
            {loading ? 'Starting...' : '🚀 Quick Start (Use Default Key)'}
          </button>
          <p style={{ 
            fontSize: '11px', 
            color: '#999', 
            marginTop: '8px',
            fontStyle: 'italic'
          }}>
            Uses pre-configured virtual key for immediate access
          </p>
        </div>

        <div style={{ 
          marginTop: '24px', 
          padding: '16px', 
          background: '#f9f9f9', 
          borderRadius: '8px',
          fontSize: '14px',
          color: '#666'
        }}>
          <strong>Note:</strong> This app connects to:
          <br />
          <code style={{ fontSize: '12px', color: '#667eea' }}>
            https://swzissb82u.us-east-1.awsapprunner.com
          </code>
        </div>
      </div>
    </div>
  )
}

export default Login
