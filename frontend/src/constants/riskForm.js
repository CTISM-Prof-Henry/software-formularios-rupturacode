import { impactScale, probabilityScale } from './riskScale.js'

export const riskTypeOptions = [
  'Operacional',
  'Financeiro',
  'Estratégico',
  'Compliance',
  'Segurança da informação',
]

export const probabilityOptions = probabilityScale.map((o) => o.label)
export const impactOptions = impactScale.map((o) => o.label)
export const riskLevelOptions = ['BAIXO', 'MODERADO', 'ALTO', 'EXTREMO']
export const controlOptions = ['Eficaz', 'Parcialmente eficaz', 'Ineficaz']

export const riskFormDefaults = {
  actionPlan: '',
  department: '',
  dueDate: '',
  identifiedRisk: '',
  impact: 'Insignificante',
  internalControls: 'Ineficaz',
  probability: 'Muito Baixa',
  // riskLevel/residualLevel são derivados de Probabilidade x Impacto (read-only).
  probabilityResidual: '',
  impactResidual: '',
  residualLevel: '',
  riskLevel: '',
  riskResponse: 'Mitigar / Reduzir',
  riskType: '',
  startDate: '',
  status: 'Não Iniciado',
}
