import { statusLabel } from '../constants/treatmentForm.js'

const toneBySituacao = {
  concluido: 'low',
  em_andamento: 'high',
  nao_iniciado: 'neutral',
  suspenso: 'neutral',
}

// Atrasado tem prioridade visual sobre a situação.
function TreatmentStatusBadge({ situacao, atrasado }) {
  if (atrasado) {
    return <span className="level-chip critical">Atrasado</span>
  }
  const tone = toneBySituacao[situacao] || 'neutral'
  return <span className={`level-chip ${tone}`}>{statusLabel(situacao)}</span>
}

export default TreatmentStatusBadge
