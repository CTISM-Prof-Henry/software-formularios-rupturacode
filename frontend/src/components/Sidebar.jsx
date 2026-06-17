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
import { podeEditarRiscos, podeGerirUsuarios } from '../lib/perms.js'

// requer: nivel minimo p/ ver o item (undefined = qualquer logado).
const navItems = [
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Riscos', to: '/riscos', icon: FileText },
  { label: 'Novo risco', to: '/riscos/novo', icon: PlusCircle, requer: 'editor' },
  { label: 'Meus tratamentos', to: '/meus-tratamentos', icon: ListChecks },
  { label: 'Usuarios', to: '/usuarios', icon: Users, requer: 'admin' },
]

function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const itensVisiveis = navItems.filter((item) => {
    if (item.requer === 'admin') return podeGerirUsuarios(user)
    if (item.requer === 'editor') return podeEditarRiscos(user)
    return true
  })

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
        {itensVisiveis.map((item) => {
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
