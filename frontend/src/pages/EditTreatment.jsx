import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import TreatmentForm from '../components/TreatmentForm.jsx'
import { treatmentFormDefaults } from '../constants/treatmentForm.js'
import { getTratamento, updateTratamento } from '../lib/api.js'

function tratamentoToForm(tratamento) {
  return {
    ...treatmentFormDefaults,
    resposta: tratamento.resposta || treatmentFormDefaults.resposta,
    usuarioResponsavelId: tratamento.usuarioResponsavelId || '',
    acao: tratamento.acao || '',
    dataInicio: tratamento.dataInicio || '',
    dataFim: tratamento.dataFim || '',
    situacao: tratamento.situacao || treatmentFormDefaults.situacao,
  }
}

function EditTreatment() {
  const { tid } = useParams()
  const navigate = useNavigate()
  const [defaultValues, setDefaultValues] = useState(null)
  const [riscoId, setRiscoId] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let ignore = false
    getTratamento(tid)
      .then((tratamento) => {
        if (!ignore) {
          setDefaultValues(tratamentoToForm(tratamento))
          setRiscoId(tratamento.riscoId)
        }
      })
      .catch(() => {
        if (!ignore) {
          setError('Não foi possível carregar o tratamento.')
        }
      })
    return () => {
      ignore = true
    }
  }, [tid])

  async function handleSubmit(data) {
    await updateTratamento(tid, data)
    if (riscoId) {
      navigate(`/riscos/${riscoId}/tratamentos`)
    }
    return { text: 'Tratamento atualizado com sucesso.', type: 'success' }
  }

  if (error) {
    return <main className="new-risk-page"><p className="page-status">{error}</p></main>
  }

  if (!defaultValues) {
    return <main className="new-risk-page"><p>Carregando...</p></main>
  }

  return (
    <TreatmentForm
      defaultValues={defaultValues}
      description="Atualize a resposta, o responsável, os prazos e a situação do tratamento."
      kicker="Edição de tratamento"
      onCancel={() => navigate(riscoId ? `/riscos/${riscoId}/tratamentos` : '/riscos')}
      onSubmit={handleSubmit}
      submitLabel="Salvar tratamento"
      title="Editar Tratamento"
    />
  )
}

export default EditTreatment
