import { useState } from 'react'
import Dashboard from './pages/Dashboard.jsx'
import NewRisk from './pages/NewRisk.jsx'
import Sidebar from './components/Sidebar.jsx'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState(() =>
    window.location.hash === '#dashboard' ? 'dashboard' : 'new-risk',
  )

  function handleNavigate(page) {
    const nextPage = page === 'risks' ? 'dashboard' : page
    window.location.hash = nextPage === 'dashboard' ? 'dashboard' : 'novo-risco'
    setCurrentPage(nextPage)
  }

  return (
    <div className="app-shell">
      <Sidebar activePage={currentPage} onNavigate={handleNavigate} />
      {currentPage === 'dashboard' ? (
        <Dashboard onNewRisk={() => handleNavigate('new-risk')} />
      ) : (
        <NewRisk />
      )}
    </div>
  )
}

export default App
