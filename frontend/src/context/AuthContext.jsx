import { useCallback, useEffect, useMemo, useState } from 'react'
import { login as loginRequest, logout as logoutRequest, me as fetchMe } from '../lib/api.js'
import { AuthContext } from './auth-context.js'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [status, setStatus] = useState('loading') // loading | authenticated | anonymous

  useEffect(() => {
    let ignore = false

    fetchMe()
      .then((data) => {
        if (!ignore) {
          setUser(data)
          setStatus('authenticated')
        }
      })
      .catch(() => {
        if (!ignore) {
          setUser(null)
          setStatus('anonymous')
        }
      })

    return () => {
      ignore = true
    }
  }, [])

  const login = useCallback(async (email, senha) => {
    const data = await loginRequest({ email, senha })
    setUser(data)
    setStatus('authenticated')
    return data
  }, [])

  const logout = useCallback(async () => {
    try {
      await logoutRequest()
    } finally {
      setUser(null)
      setStatus('anonymous')
    }
  }, [])

  const value = useMemo(() => ({ user, status, login, logout }), [user, status, login, logout])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
