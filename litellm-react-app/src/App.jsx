import { useState, useEffect } from 'react'
import './App.css'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import ChatInterface from './components/ChatInterface'

const LITELLM_API_URL = 'https://swzissb82u.us-east-1.awsapprunner.com'
const LITELLM_UI_URL = 'https://swzissb82u.us-east-1.awsapprunner.com/ui/login/'
// Default virtual key for quick start
const DEFAULT_VIRTUAL_KEY = 'sk-N00S6nZMl_1xqzIZ13mdpw'
// Market API URL for authenticated user info
const MARKET_API_URL = 'https://market.niyogen.com'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userApiKey, setUserApiKey] = useState('')
  const [userInfo, setUserInfo] = useState(null)
  const [marketUserInfo, setMarketUserInfo] = useState(null) // User info from market.niyogen.com
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Fetch authenticated user info from market.niyogen.com
  const fetchMarketUserInfo = async () => {
    try {
      const response = await fetch(`${MARKET_API_URL}/api/auth/me`, {
        method: 'GET',
        credentials: 'include', // Include cookies for authentication
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (response.ok) {
        const data = await response.json()
        setMarketUserInfo(data)
        localStorage.setItem('market_user_info', JSON.stringify(data))
        return data
      } else {
        // If not authenticated, try to get from localStorage
        const savedMarketUserInfo = localStorage.getItem('market_user_info')
        if (savedMarketUserInfo) {
          setMarketUserInfo(JSON.parse(savedMarketUserInfo))
        }
        return null
      }
    } catch (err) {
      console.log('Could not fetch market user info:', err)
      // Try to get from localStorage as fallback
      const savedMarketUserInfo = localStorage.getItem('market_user_info')
      if (savedMarketUserInfo) {
        setMarketUserInfo(JSON.parse(savedMarketUserInfo))
      }
      return null
    }
  }

  // Check if user is already logged in
  useEffect(() => {
    const savedApiKey = localStorage.getItem('litellm_api_key')
    const savedUserInfo = localStorage.getItem('litellm_user_info')
    
    if (savedApiKey) {
      setUserApiKey(savedApiKey)
      setIsAuthenticated(true)
      if (savedUserInfo) {
        setUserInfo(JSON.parse(savedUserInfo))
      }
    }
    
    // Fetch market user info on mount
    fetchMarketUserInfo()
  }, [])

  // Quick start with default virtual key
  const handleQuickStart = async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Use the default virtual key directly
      setUserApiKey(DEFAULT_VIRTUAL_KEY)
      setIsAuthenticated(true)
      localStorage.setItem('litellm_api_key', DEFAULT_VIRTUAL_KEY)
      
      // Try to get user info (optional, won't fail if it doesn't work)
      try {
        const response = await fetch(`${LITELLM_API_URL}/user/info?user_id=admin`, {
          headers: {
            'x-litellm-api-key': 'sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642',
          },
        })
        if (response.ok) {
          const data = await response.json()
          setUserInfo(data)
          localStorage.setItem('litellm_user_info', JSON.stringify(data))
        }
      } catch (err) {
        // Ignore errors when fetching user info
        console.log('Could not fetch user info, continuing with key only')
      }
      
      // Fetch market user info
      await fetchMarketUserInfo()
    } catch (err) {
      setError(err.message || 'Quick start failed.')
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = async (username, password) => {
    setLoading(true)
    setError(null)
    
    try {
      // Password is the master key for LiteLLM UI login
      const masterKey = password
      
      // Try to get or create a user with the username
      // First, try to get existing user info
      let response = await fetch(`${LITELLM_API_URL}/user/info?user_id=${username}`, {
        headers: {
          'x-litellm-api-key': masterKey,
        },
      })
      
      let data
      let createdKey = null // Store key from user creation
      
      if (response.ok) {
        data = await response.json()
      } else {
        // User doesn't exist, create a new user
        response = await fetch(`${LITELLM_API_URL}/user/new`, {
          method: 'POST',
          headers: {
            'x-litellm-api-key': masterKey,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: username,
            user_email: `${username}@example.com`,
            user_alias: username,
            auto_create_key: true,
            tpm_limit: 100000,
            rpm_limit: 100,
          }),
        })
        
        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`Failed to create user: ${errorText}`)
        }
        
        const createData = await response.json()
        // Save the key from user creation (this is the virtual key)
        if (createData.key && createData.key.startsWith('sk-')) {
          createdKey = createData.key
        }
        
        // Wait a moment for user to be fully created, then fetch info
        await new Promise(resolve => setTimeout(resolve, 1000))
        response = await fetch(`${LITELLM_API_URL}/user/info?user_id=${username}`, {
          headers: {
            'x-litellm-api-key': masterKey,
          },
        })
        data = await response.json()
      }
      
      // Get the first API key from user
      let apiKey = null
      
      // First priority: use key from user creation
      if (createdKey && createdKey.startsWith('sk-')) {
        apiKey = createdKey
      }
      // Second priority: check if data has a key field (from creation response)
      else if (data.key && data.key.startsWith('sk-')) {
        apiKey = data.key
      }
      // Third priority: check if keys array has a virtual key (starts with 'sk-')
      else if (data.keys && data.keys.length > 0) {
        // Look for a key that starts with 'sk-' (virtual key)
        const virtualKey = data.keys.find((k) => {
          const keyValue = typeof k === 'string' ? k : (k.token || k.key || '')
          return keyValue && keyValue.startsWith('sk-')
        })
        
        if (virtualKey) {
          apiKey = typeof virtualKey === 'string' ? virtualKey : (virtualKey.token || virtualKey.key)
        }
      }
      
      // If we still don't have a virtual key, create a new one
      if (!apiKey || !apiKey.startsWith('sk-')) {
        console.log('No virtual key found, creating new key...')
        const keyResponse = await fetch(`${LITELLM_API_URL}/key/generate`, {
          method: 'POST',
          headers: {
            'x-litellm-api-key': masterKey,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: username,
            duration: null, // No expiration
          }),
        })
        
        if (keyResponse.ok) {
          const keyData = await keyResponse.json()
          apiKey = keyData.key || keyData.token
        } else {
          const errorText = await keyResponse.text()
          throw new Error(`Failed to create API key: ${errorText}`)
        }
      }
      
      // Final validation: ensure we have a valid virtual key
      if (!apiKey || !apiKey.startsWith('sk-')) {
        throw new Error('Failed to obtain valid API key. Expected key starting with "sk-".')
      }
      
      setUserApiKey(apiKey)
      setUserInfo(data)
      setIsAuthenticated(true)
      localStorage.setItem('litellm_api_key', apiKey)
      localStorage.setItem('litellm_user_info', JSON.stringify(data))
      
      // Fetch market user info
      await fetchMarketUserInfo()
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    setUserApiKey('')
    setUserInfo(null)
    setMarketUserInfo(null)
    localStorage.removeItem('litellm_api_key')
    localStorage.removeItem('litellm_user_info')
    localStorage.removeItem('market_user_info')
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} onQuickStart={handleQuickStart} loading={loading} error={error} />
  }

  return (
    <div className="app">
      <Dashboard 
        userInfo={userInfo} 
        marketUserInfo={marketUserInfo}
        apiKey={userApiKey}
        onLogout={handleLogout}
        apiUrl={LITELLM_API_URL}
      />
      <ChatInterface 
        apiKey={userApiKey}
        apiUrl={LITELLM_API_URL}
      />
    </div>
  )
}

export default App
