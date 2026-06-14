import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import RiskForm from '../components/RiskForm.jsx'
import { riskFormDefaults } from '../constants/riskForm.js'
import { getRisco, updateRisco } from '../lib/api.js'

function riscoToForm(risco) {
  return {
    ...riskFormDefaults,
    department: risco.departamento || '',
    riskType: risco.tipo || '',
    identifiedRisk: risco.descricao || '',
    probability: risco.probabilidade || riskFormDefaults.probability,
    impact: risco.impacto || riskFormDefaults.impact,
    riskLevel: risco.nivelDeRisco || riskFormDefaults.riskLevel,
    internalControls: risco.eficaciaDosControles || riskFormDefaults.internalControls,
    probabilityResidual: risco.probabilidadeResidual || '',
    impactResidual: risco.impactoResidual || '',
    residualLevel: risco.nivelResidual || riskFormDefaults.residualLevel,
  }
}

function EditRisk() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [defaultValues, setDefaultValues] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let ignore = false

    getRisco(id)
      .then((risco) => {
        if (!ignore) {
          setDefaultValues(riscoToForm(risco))
        }
      })
      .catch(() => {
        if (!ignore) {
          setError('Não foi possível carregar o risco.')
        }
      })

    return () => {
      ignore = true
    }
  }, [id])

  async function handleSubmit(data) {
    await updateRisco(id, data)
    return { text: 'Risco atualizado com sucesso.', type: 'success' }
  }

  if (error) {
    return <main className="new-risk-page"><p className="page-status">{error}</p></main>
  }

  if (!defaultValues) {
    return <main className="new-risk-page"><p>Carregando...</p></main>
  }

  return (
    <RiskForm
      defaultValues={defaultValues}
      description="Atualize as informações do risco institucional selecionado."
      kicker="Edição de risco"
      onCancel={() => navigate('/riscos')}
      onSubmit={handleSubmit}
      submitLabel="Salvar registro"
      title="Editar Risco"
    />
  )
}

export default EditRisk
