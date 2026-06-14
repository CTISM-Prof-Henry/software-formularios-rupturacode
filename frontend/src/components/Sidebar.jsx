import {
  FileText,
  LayoutDashboard,
  ListChecks,
  LogOut,
  PlusCircle,
  ShieldCheck,
  Users,
} from 'lucide-react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'

const navItems = [
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Riscos', to: '/riscos', icon: FileText },
  { label: 'Novo risco', to: '/riscos/novo', icon: PlusCircle },
  { label: 'Meus tratamentos', to: '/meus-tratamentos', icon: ListChecks },
  { label: 'Usuarios', to: '/usuarios', icon: Users },
]

function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    navigate('/login')
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark" aria-hidden="true">
          <ShieldCheck size={24} strokeWidth={2.2} />
        </div>
        <div>
          <strong>Atlas - Gestão de Riscos</strong>
          <span>Sistema de gerenciamento de risco</span>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Menu lateral">
        {navItems.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              className={({ isActive }) => (isActive ? 'active' : undefined)}
              end={item.to === '/dashboard' || item.to === '/riscos'}
              key={item.label}
              to={item.to}
            >
              <Icon size={18} strokeWidth={2} />
              <span>{item.label}</span>
            </NavLink>
          )
        })}
      </nav>

      <div className="sidebar-footer">
        <span>Sessão</span>
        <strong>{user?.nome || 'Usuário'}</strong>
        <button className="logout-button" onClick={handleLogout} type="button">
          <LogOut size={15} strokeWidth={2} />
          Sair
        </button>
      </div>
    </aside>
  )
}

export default Sidebar
