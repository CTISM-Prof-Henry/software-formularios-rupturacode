import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'

function ProtectedRoute() {
  const { status } = useAuth()

  if (status === 'loading') {
    return <div className="route-loading">Carregando...</div>
  }

  if (status !== 'authenticated') {
    return <Navigate replace to="/login" />
  }

  return <Outlet />
}

export default ProtectedRoute
