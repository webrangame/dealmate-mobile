import { useState, useEffect } from 'react'
import '../App.css'

function Dashboard({ userInfo, marketUserInfo, apiKey, onLogout, apiUrl }) {
  const [tokenUsage, setTokenUsage] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (userInfo) {
      // Extract token usage from user info
      const usage = {
        spend: userInfo.user_info?.spend || 0,
        total_tokens: userInfo.user_info?.total_tokens || 0,
        prompt_tokens: userInfo.user_info?.prompt_tokens || 0,
        completion_tokens: userInfo.user_info?.completion_tokens || 0,
        tpm_limit: userInfo.user_info?.tpm_limit || 0,
        rpm_limit: userInfo.user_info?.rpm_limit || 0,
      }
      setTokenUsage(usage)
      setLoading(false)
    }
  }, [userInfo])

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  return (
    <div style={{ 
      background: 'white', 
      padding: '20px', 
      borderBottom: '2px solid #e0e0e0',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <div className="container">
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '20px'
        }}>
          <div>
            <h1 style={{ color: '#333', fontSize: '28px', marginBottom: '8px' }}>
              🚅 LiteLLM Dashboard
            </h1>
            {marketUserInfo && (
              <div style={{ 
                fontSize: '14px', 
                color: '#666',
                display: 'flex',
                alignItems: 'center',
                gap: '12px'
              }}>
                <span>👤 Signed in as:</span>
                <strong style={{ color: '#667eea' }}>
                  {marketUserInfo.name || marketUserInfo.email || 'User'}
                </strong>
                {marketUserInfo.email && (
                  <span style={{ color: '#999' }}>({marketUserInfo.email})</span>
                )}
              </div>
            )}
          </div>
          <button onClick={onLogout} className="button">
            Logout
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          {/* API Key Section */}
          <div className="card">
            <h3>Your API Key</h3>
            <div className="info-box">
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center' 
              }}>
                <code className="code-block" style={{ flex: 1, marginRight: '12px' }}>
                  {apiKey ? `${apiKey.substring(0, 20)}...` : 'Not available'}
                </code>
                <button 
                  onClick={() => copyToClipboard(apiKey)}
                  className="button"
                  style={{ padding: '8px 16px', fontSize: '14px' }}
                >
                  Copy
                </button>
              </div>
            </div>
            <p style={{ fontSize: '14px', color: '#666', marginTop: '12px' }}>
              Use this key to make API requests to LiteLLM
            </p>
          </div>

          {/* Token Usage Section */}
          <div className="card">
            <h3>Token Usage</h3>
            {loading ? (
              <p>Loading...</p>
            ) : tokenUsage ? (
              <div>
                <div className="info-box">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Total Spend:</span>
                    <strong>${tokenUsage.spend.toFixed(4)}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Total Tokens:</span>
                    <strong>{tokenUsage.total_tokens.toLocaleString()}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Prompt Tokens:</span>
                    <strong>{tokenUsage.prompt_tokens.toLocaleString()}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Completion Tokens:</span>
                    <strong>{tokenUsage.completion_tokens.toLocaleString()}</strong>
                  </div>
                </div>
                <div style={{ marginTop: '12px', fontSize: '14px', color: '#666' }}>
                  <div>TPM Limit: {tokenUsage.tpm_limit.toLocaleString()}</div>
                  <div>RPM Limit: {tokenUsage.rpm_limit.toLocaleString()}</div>
                </div>
              </div>
            ) : (
              <p style={{ color: '#999' }}>No usage data available</p>
            )}
          </div>
        </div>

        {/* User Info */}
        <div className="card" style={{ marginTop: '20px' }}>
          <h3>User Information</h3>
          
          {/* Market User Info (from market.niyogen.com) */}
          {marketUserInfo && (
            <div className="info-box" style={{ marginBottom: '16px', borderLeft: '4px solid #667eea' }}>
              <div style={{ marginBottom: '8px' }}>
                <strong>Name:</strong> {marketUserInfo.name || 'N/A'}
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Email:</strong> {marketUserInfo.email || 'N/A'}
              </div>
              {marketUserInfo.id && (
                <div style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
                  User ID: {marketUserInfo.id}
                </div>
              )}
            </div>
          )}
          
          {/* LiteLLM User Info */}
          {userInfo && (
            <div className="info-box">
              <div style={{ marginBottom: '8px', fontWeight: '600', color: '#667eea' }}>
                LiteLLM Account
              </div>
              <div><strong>User ID:</strong> {userInfo.user_id || 'N/A'}</div>
              <div style={{ marginTop: '8px' }}>
                <strong>Email:</strong> {userInfo.user_info?.user_email || 'N/A'}
              </div>
              <div style={{ marginTop: '8px' }}>
                <strong>Alias:</strong> {userInfo.user_info?.user_alias || 'N/A'}
              </div>
              <div style={{ marginTop: '8px' }}>
                <strong>Role:</strong> {userInfo.user_info?.user_role || 'N/A'}
              </div>
            </div>
          )}
          
          {!marketUserInfo && !userInfo && (
            <p style={{ color: '#999' }}>No user information available</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
