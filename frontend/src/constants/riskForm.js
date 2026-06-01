export const riskTypeOptions = [
  'Operacional',
  'Financeiro',
  'Estratégico',
  'Compliance',
  'Segurança da informação',
]

export const probabilityOptions = ['Muito Baixa', 'Baixa', 'Média', 'Alta', 'Muito Alta']
export const impactOptions = ['Insignificante', 'Pequeno', 'Moderado', 'Grande', 'Catastrófico']
export const riskLevelOptions = ['BAIXO', 'MODERADO', 'ALTO', 'CRÍTICO']
export const controlOptions = ['Eficaz', 'Parcialmente eficaz', 'Ineficaz']
export const residualOptions = ['BAIXO', 'MÉDIO', 'ALTO', 'CRÍTICO']
export const responseOptions = ['Mitigar / Reduzir', 'Aceitar', 'Transferir', 'Evitar']
export const statusOptions = ['Não Iniciado', 'Em andamento', 'Concluído', 'Suspenso']

export const riskFormDefaults = {
  actionPlan: '',
  department: '',
  dueDate: '',
  identifiedRisk: '',
  impact: 'Insignificante',
  internalControls: 'Ineficaz',
  probability: 'Muito Baixa',
  residualLevel: 'ALTO',
  riskLevel: 'CRÍTICO',
  riskResponse: 'Mitigar / Reduzir',
  riskType: '',
  startDate: '',
  status: 'Não Iniciado',
}
