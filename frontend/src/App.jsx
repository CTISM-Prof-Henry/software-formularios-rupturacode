import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import AppLayout from './components/AppLayout.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Dashboard from './pages/Dashboard.jsx'
import NewRisk from './pages/NewRisk.jsx'
import EditRisk from './pages/EditRisk.jsx'
import RiskList from './pages/RiskList.jsx'
import UserList from './pages/UserList.jsx'
import NewUser from './pages/NewUser.jsx'
import Login from './pages/Login.jsx'
import ForgotPassword from './pages/ForgotPassword.jsx'
import ConfirmCode from './pages/ConfirmCode.jsx'
import ResetPassword from './pages/ResetPassword.jsx'
import './App.css'

function DashboardRoute() {
  const navigate = useNavigate()
  return <Dashboard onNewRisk={() => navigate('/riscos/novo')} />
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/esqueceu-senha" element={<ForgotPassword />} />
      <Route path="/codigo" element={<ConfirmCode />} />
      <Route path="/alterar-senha" element={<ResetPassword />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/" element={<DashboardRoute />} />
          <Route path="/dashboard" element={<DashboardRoute />} />
          <Route path="/riscos" element={<RiskList />} />
          <Route path="/riscos/novo" element={<NewRisk />} />
          <Route path="/riscos/:id/editar" element={<EditRisk />} />
          <Route path="/usuarios" element={<UserList />} />
          <Route path="/usuarios/novo" element={<NewUser />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate replace to="/" />} />
    </Routes>
  )
}

export default App
