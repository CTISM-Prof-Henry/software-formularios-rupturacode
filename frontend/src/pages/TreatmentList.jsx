import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowLeft, Pencil, Plus, Trash2 } from 'lucide-react'
import { useNavigate, useParams } from 'react-router-dom'
import { pageVariants } from '../animations/pageAnimations.js'
import PageHeader from '../components/PageHeader.jsx'
import TreatmentStatusBadge from '../components/TreatmentStatusBadge.jsx'
import { responseLabel } from '../constants/treatmentForm.js'
import { useAuth } from '../hooks/useAuth.js'
import { podeEditarRiscos } from '../lib/perms.js'
import { deleteTratamento, getRisco, getTratamentos } from '../lib/api.js'

function formatDate(value) {
  if (!value) {
    return '—'
  }
  const [year, month, day] = value.split('-')
  return `${day}/${month}/${year}`
}

function TreatmentList() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const podeEditar = podeEditarRiscos(user)
  const [risco, setRisco] = useState(null)
  const [tratamentos, setTratamentos] = useState([])
  const [status, setStatus] = useState('loading')

  function carregar() {
    setStatus('loading')
    Promise.all([getRisco(id), getTratamentos({ risco: id })])
      .then(([riscoData, tratamentosData]) => {
        setRisco(riscoData)
        setTratamentos(tratamentosData.results || [])
        setStatus('loaded')
      })
      .catch(() => setStatus('offline'))
  }

  useEffect(() => {
    let ignore = false
    Promise.all([getRisco(id), getTratamentos({ risco: id })])
      .then(([riscoData, tratamentosData]) => {
        if (!ignore) {
          setRisco(riscoData)
          setTratamentos(tratamentosData.results || [])
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
  }, [id])

  function handleDelete(tratamentoId) {
    if (!window.confirm('Remover este tratamento?')) {
      return
    }
    deleteTratamento(tratamentoId).then(carregar).catch(() => setStatus('offline'))
  }

  const tituloRisco = risco ? risco.nome || risco.descricao : ''

  return (
    <motion.main
      animate="visible"
      className="list-page"
      initial="hidden"
      variants={pageVariants}
    >
      <PageHeader
        actions={
          <>
            <button className="link-button" onClick={() => navigate('/riscos')} type="button">
              <ArrowLeft size={16} />
              Voltar
            </button>
            {podeEditar && (
              <button
                className="primary-button"
                onClick={() => navigate(`/riscos/${id}/tratamentos/novo`)}
                type="button"
              >
                <Plus size={16} />
                Novo Tratamento
              </button>
            )}
          </>
        }
        description={tituloRisco ? `Tratamentos do risco: ${tituloRisco}` : 'Tratamentos do risco.'}
        kicker="Gestão de tratamentos"
        statusMessage={status === 'offline' ? 'Backend indisponível.' : null}
        title="Tratamentos"
      />

      <section className="table-card">
        <div className="data-table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Resposta</th>
                <th>Responsável</th>
                <th>Ação</th>
                <th>Prazo</th>
                <th>Situação</th>
                <th className="col-action">Ações</th>
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
                  <td colSpan={6} className="table-empty">Nenhum tratamento cadastrado.</td>
                </tr>
              )}
              {tratamentos.map((tratamento) => (
                <tr key={tratamento.id}>
                  <td className="cell-strong">{responseLabel(tratamento.resposta)}</td>
                  <td>{tratamento.usuarioResponsavelNome || '—'}</td>
                  <td>{tratamento.acao || '—'}</td>
                  <td>{formatDate(tratamento.dataFim)}</td>
                  <td>
                    <TreatmentStatusBadge
                      atrasado={tratamento.atrasado}
                      situacao={tratamento.situacao}
                    />
                  </td>
                  <td className="col-action">
                    {podeEditar ? (
                      <>
                        <button
                          aria-label="Editar tratamento"
                          className="icon-button"
                          onClick={() => navigate(`/tratamentos/${tratamento.id}/editar`)}
                          type="button"
                        >
                          <Pencil size={16} />
                        </button>
                        <button
                          aria-label="Remover tratamento"
                          className="icon-button"
                          onClick={() => handleDelete(tratamento.id)}
                          type="button"
                        >
                          <Trash2 size={16} />
                        </button>
                      </>
                    ) : (
                      '—'
                    )}
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

export default TreatmentList
