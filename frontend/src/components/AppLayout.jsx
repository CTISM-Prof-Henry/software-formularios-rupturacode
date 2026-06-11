import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar.jsx'

function AppLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <Outlet />
    </div>
  )
}

export default AppLayout
