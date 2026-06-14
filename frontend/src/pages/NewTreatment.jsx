import { useNavigate, useParams } from 'react-router-dom'
import TreatmentForm from '../components/TreatmentForm.jsx'
import { createTratamento } from '../lib/api.js'

function NewTreatment() {
  const { id } = useParams()
  const navigate = useNavigate()

  async function handleSubmit(data) {
    await createTratamento({ ...data, riscoId: id })
    navigate(`/riscos/${id}/tratamentos`)
    return { text: 'Tratamento cadastrado com sucesso.', type: 'success' }
  }

  return (
    <TreatmentForm
      description="Defina a resposta ao risco, o responsável e os prazos do tratamento."
      kicker="Novo tratamento"
      onCancel={() => navigate(`/riscos/${id}/tratamentos`)}
      onSubmit={handleSubmit}
      submitLabel="Salvar tratamento"
      title="Novo Tratamento"
    />
  )
}

export default NewTreatment
