import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext()

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1'

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
      setIsAuthenticated(true)
      axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
    }
    setLoading(false)
  }, [])

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API_BASE}/auth/login`, {
        username,
        password
      })
      
      const { access_token } = response.data
      const userData = { username }
      
      localStorage.setItem('authToken', access_token)
      localStorage.setItem('user', JSON.stringify(userData))
      
      setToken(access_token)
      setUser(userData)
      setIsAuthenticated(true)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const register = async (username, email, password) => {
    try {
      await axios.post(`${API_BASE}/auth/register`, {
        username,
        email,
        password
      })
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
    setIsAuthenticated(false)
    delete axios.defaults.headers.common['Authorization']
  }

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      user,
      token,
      loading,
      login,
      register,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
