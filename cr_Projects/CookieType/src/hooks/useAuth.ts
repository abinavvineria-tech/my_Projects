import { useState, useEffect, useCallback } from 'react'

export interface AuthState {
  isAuthenticated: boolean
  user: { username: string; passwordHash: string } | null
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    isAuthenticated: false,
    user: null
  })

  useEffect(() => {
    const saved = localStorage.getItem('cookietype-auth')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        setState({ isAuthenticated: true, user: parsed })
      } catch {}
    }
  }, [])

  const login = useCallback((username: string, password: string) => {
    const hash = btoa(password) // Simple demo - in production use proper hashing
    const user = { username, passwordHash: hash }
    localStorage.setItem('cookietype-auth', JSON.stringify(user))
    setState({ isAuthenticated: true, user })
    return true
  }, [])

  const register = useCallback((username: string, password: string) => {
    const hash = btoa(password)
    const user = { username, passwordHash: hash }
    localStorage.setItem('cookietype-auth', JSON.stringify(user))
    setState({ isAuthenticated: true, user })
    return true
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('cookietype-auth')
    setState({ isAuthenticated: false, user: null })
  }, [])

  const verifyPassword = useCallback((password: string) => {
    if (!state.user) return false
    return state.user.passwordHash === btoa(password)
  }, [state.user])

  return { ...state, login, register, logout, verifyPassword }
}