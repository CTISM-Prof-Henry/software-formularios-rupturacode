import { FileText, LayoutDashboard, PlusCircle, ShieldCheck } from 'lucide-react'

const navItems = [
  { label: 'Dashboard', page: 'dashboard', icon: LayoutDashboard },
  { label: 'Riscos', page: 'risks', icon: FileText },
  { label: 'Novo risco', page: 'new-risk', icon: PlusCircle },
]

function Sidebar({ activePage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark" aria-hidden="true">
          <ShieldCheck size={24} strokeWidth={2.2} />
        </div>
        <div>
          <strong>Atlas</strong>
          <span>Gestão de riscos institucionais</span>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Menu lateral">
        {navItems.map((item) => {
          const Icon = item.icon

          return (
            <a
              className={activePage === item.page ? 'active' : undefined}
              href="/"
              key={item.label}
              onClick={(event) => {
                event.preventDefault()
                onNavigate(item.page)
              }}
            >
              <Icon size={18} strokeWidth={2} />
              <span>{item.label}</span>
            </a>
          )
        })}
      </nav>

      <div className="sidebar-footer">
        <span>Status</span>
        <strong>Sistema em desenvolvimento</strong>
      </div>
    </aside>
  )
}

export default Sidebar
