import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Pencil } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { pageVariants } from '../animations/pageAnimations.js'
import PageHeader from '../components/PageHeader.jsx'
import TreatmentStatusBadge from '../components/TreatmentStatusBadge.jsx'
import { responseLabel } from '../constants/treatmentForm.js'
import { useAuth } from '../hooks/useAuth.js'
import { getTratamentos } from '../lib/api.js'

function formatDate(value) {
  if (!value) {
    return '—'
  }
  const [year, month, day] = value.split('-')
  return `${day}/${month}/${year}`
}

function MyTreatments() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [tratamentos, setTratamentos] = useState([])
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    if (!user?.id) {
      return undefined
    }
    let ignore = false
    getTratamentos({ responsavel: user.id })
      .then((data) => {
        if (!ignore) {
          setTratamentos(data.results || [])
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
  }, [user?.id])

  return (
    <motion.main
      animate="visible"
      className="list-page"
      initial="hidden"
      variants={pageVariants}
    >
      <PageHeader
        description="Tratamentos sob sua responsabilidade. Mantenha a situação atualizada."
        kicker="Minhas tarefas"
        statusMessage={status === 'offline' ? 'Backend indisponível.' : null}
        title="Meus Tratamentos"
      />

      <section className="table-card">
        <div className="data-table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Risco</th>
                <th>Resposta</th>
                <th>Ação</th>
                <th>Prazo</th>
                <th>Situação</th>
                <th className="col-action">Editar</th>
              </tr>
            </thead>
            <tbody>
              {status === 'loading' && (
                <tr>
                  <td colSpan={6} className="table-empty">Carregando...</td>
                </tr>
              )}
              {status !== 'loading' && tratamentos.length === 0 && (
                <tr>
                  <td colSpan={6} className="table-empty">Nenhum tratamento atribuído a você.</td>
                </tr>
              )}
              {tratamentos.map((tratamento) => (
                <tr key={tratamento.id}>
                  <td className="cell-strong">{tratamento.riscoNome || '—'}</td>
                  <td>{responseLabel(tratamento.resposta)}</td>
                  <td>{tratamento.acao || '—'}</td>
                  <td>{formatDate(tratamento.dataFim)}</td>
                  <td>
                    <TreatmentStatusBadge
                      atrasado={tratamento.atrasado}
                      situacao={tratamento.situacao}
                    />
                  </td>
                  <td className="col-action">
                    <button
                      aria-label="Editar tratamento"
                      className="icon-button"
                      onClick={() => navigate(`/tratamentos/${tratamento.id}/editar`)}
                      type="button"
                    >
                      <Pencil size={16} />
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

export default MyTreatments
