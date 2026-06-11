import RiskForm from '../components/RiskForm.jsx'
import { createRisk } from '../lib/api.js'

function NewRisk() {
  async function handleSubmit(data, reset) {
    await createRisk(data)
    reset()
    return { text: 'Risco cadastrado com sucesso.', type: 'success' }
  }

  return (
    <RiskForm
      description="Registre uma nova ameaça ou oportunidade institucional no sistema centralizado."
      kicker="Cadastro de risco"
      onSubmit={handleSubmit}
      submitLabel="Salvar registro"
      title="Identificação de Novo Risco"
    />
  )
}

export default NewRisk
