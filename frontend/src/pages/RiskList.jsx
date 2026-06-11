import { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { Check, Pencil, Plus, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { pageVariants } from '../animations/pageAnimations.js'
import FilterBar from '../components/FilterBar.jsx'
import LevelChip from '../components/LevelChip.jsx'
import PageHeader from '../components/PageHeader.jsx'
import { impactOptions, riskLevelOptions, riskTypeOptions } from '../constants/riskForm.js'
import { getRiscos } from '../lib/api.js'

function RiskList() {
  const navigate = useNavigate()
  const [riscos, setRiscos] = useState([])
  const [status, setStatus] = useState('loading')
  const [busca, setBusca] = useState('')
  const [tipo, setTipo] = useState('')
  const [nivel, setNivel] = useState('')
  const [impacto, setImpacto] = useState('')
  const [applied, setApplied] = useState({ busca: '', tipo: '', nivel: '', impacto: '' })

  useEffect(() => {
    let ignore = false

    getRiscos()
      .then((data) => {
        if (!ignore) {
          setRiscos(data.results || [])
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

  const filtered = useMemo(() => {
    return riscos.filter((risco) => {
      const matchBusca =
        !applied.busca ||
        (risco.descricao || '').toLowerCase().includes(applied.busca.toLowerCase()) ||
        (risco.nome || '').toLowerCase().includes(applied.busca.toLowerCase())
      const matchTipo = !applied.tipo || risco.tipo === applied.tipo
      const matchNivel = !applied.nivel || risco.nivelDeRisco === applied.nivel
      const matchImpacto = !applied.impacto || risco.impacto === applied.impacto
      return matchBusca && matchTipo && matchNivel && matchImpacto
    })
  }, [riscos, applied])

  function applyFilters() {
    setApplied({ busca, tipo, nivel, impacto })
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
          <button className="primary-button" onClick={() => navigate('/riscos/novo')} type="button">
            <Plus size={16} />
            Novo Risco
          </button>
        }
        description="Consulte, filtre e edite os riscos institucionais cadastrados."
        kicker="Gestão de riscos"
        statusMessage={status === 'offline' ? 'Backend indisponível.' : null}
        title="Riscos"
      />

      <section className="table-card">
        <FilterBar
          onFilter={applyFilters}
          onSearchChange={setBusca}
          searchPlaceholder="Buscar Risco..."
          searchValue={busca}
          selects={[
            { label: 'Tipos de risco', value: tipo, onChange: setTipo, options: riskTypeOptions },
            { label: 'Nível', value: nivel, onChange: setNivel, options: riskLevelOptions },
            { label: 'Impacto', value: impacto, onChange: setImpacto, options: impactOptions },
          ]}
        />

        <div className="data-table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Risco</th>
                <th>Tipo</th>
                <th>Probabilidade</th>
                <th>Impacto</th>
                <th>Nível</th>
                <th>Com Tratamento</th>
                <th className="col-action">Editar</th>
              </tr>
            </thead>
            <tbody>
              {status === 'loading' && (
                <tr>
                  <td colSpan={7} className="table-empty">Carregando...</td>
                </tr>
              )}
              {status !== 'loading' && filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="table-empty">Nenhum risco encontrado.</td>
                </tr>
              )}
              {filtered.map((risco) => (
                <tr key={risco.id}>
                  <td className="cell-strong">{risco.nome || risco.descricao}</td>
                  <td>{risco.tipo}</td>
                  <td>{risco.probabilidade}</td>
                  <td>{risco.impacto}</td>
                  <td><LevelChip level={risco.nivelDeRisco} /></td>
                  <td className="col-center">
                    {risco.comTratamento ? (
                      <Check size={16} className="icon-yes" />
                    ) : (
                      <X size={16} className="icon-no" />
                    )}
                  </td>
                  <td className="col-action">
                    <button
                      aria-label={`Editar ${risco.nome || risco.descricao}`}
                      className="icon-button"
                      onClick={() => navigate(`/riscos/${risco.id}/editar`)}
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

export default RiskList
