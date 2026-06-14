import { useCallback, useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Pencil, Plus, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { pageVariants } from '../animations/pageAnimations.js'
import FilterBar from '../components/FilterBar.jsx'
import PageHeader from '../components/PageHeader.jsx'
import StatusChip from '../components/StatusChip.jsx'
import { useCentros } from '../hooks/useCentros.js'
import { cargoOptions } from '../constants/userForm.js'
import { deleteUsuario, getUsuarios } from '../lib/api.js'

function UserList() {
  const navigate = useNavigate()
  const [usuarios, setUsuarios] = useState([])
  const [status, setStatus] = useState('loading')
  const centros = useCentros()
  const [busca, setBusca] = useState('')
  const [cargo, setCargo] = useState('')
  const [centro, setCentro] = useState('')

  const runFetch = useCallback((params) => {
    return getUsuarios(params)
      .then((data) => {
        setUsuarios(data.results || [])
        setStatus('loaded')
      })
      .catch(() => setStatus('offline'))
  }, [])

  useEffect(() => {
    let ignore = false
    getUsuarios()
      .then((data) => {
        if (!ignore) {
          setUsuarios(data.results || [])
          setStatus('loaded')
        }
      })
      .catch(() => {
        if (!ignore) {
          setStatus('offline')
        }
      })
    return () => {
      ignore = true
    }
  }, [])

  function applyFilters() {
    setStatus('loading')
    runFetch({ busca, cargo, centro })
  }

  function handleDelete(usuario) {
    if (!window.confirm(`Remover o usuário "${usuario.nome}"?`)) {
      return
    }
    deleteUsuario(usuario.id)
      .then(() => runFetch({ busca, cargo, centro }))
      .catch(() => setStatus('offline'))
  }

  return (
    <motion.main
      animate="visible"
      className="list-page"
      initial="hidden"
      variants={pageVariants}
    >
      <PageHeader
        actions={
          <button className="primary-button" onClick={() => navigate('/usuarios/novo')} type="button">
            <Plus size={16} />
            Novo Usuario
          </button>
        }
        description="Gerencie os usuários e funcionários cadastrados no sistema."
        kicker="Gestão de usuários"
        statusMessage={status === 'offline' ? 'Backend indisponível.' : null}
        title="Usuarios"
      />

      <section className="table-card">
        <FilterBar
          onFilter={applyFilters}
          onSearchChange={setBusca}
          searchPlaceholder="Buscar Usuario..."
          searchValue={busca}
          selects={[
            { label: 'Cargo do Usuario', value: cargo, onChange: setCargo, options: cargoOptions },
            {
              label: 'Centro',
              value: centro,
              onChange: setCentro,
              options: centros.map((c) => c.sigla),
            },
          ]}
        />

        <div className="data-table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Centro</th>
                <th>Departamento</th>
                <th>Cargo</th>
                <th>Status</th>
                <th className="col-action">Ações</th>
              </tr>
            </thead>
            <tbody>
              {status === 'loading' && (
                <tr>
                  <td colSpan={6} className="table-empty">Carregando...</td>
                </tr>
              )}
              {status !== 'loading' && usuarios.length === 0 && (
                <tr>
                  <td colSpan={6} className="table-empty">Nenhum usuário encontrado.</td>
                </tr>
              )}
              {usuarios.map((usuario) => (
                <tr key={usuario.id}>
                  <td className="cell-strong">{usuario.nome}</td>
                  <td>{usuario.centro || '—'}</td>
                  <td>{usuario.departamento}</td>
                  <td>{usuario.cargo}</td>
                  <td><StatusChip active={usuario.ativo} /></td>
                  <td className="col-action">
                    <button
                      aria-label={`Editar ${usuario.nome}`}
                      className="icon-button"
                      onClick={() => navigate(`/usuarios/${usuario.id}/editar`)}
                      type="button"
                    >
                      <Pencil size={16} />
                    </button>
                    <button
                      aria-label={`Remover ${usuario.nome}`}
                      className="icon-button"
                      onClick={() => handleDelete(usuario)}
                      type="button"
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </motion.main>
  )
}

export default UserList
