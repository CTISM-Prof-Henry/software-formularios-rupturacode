export const fallbackSummary = {
  totalRiscos: 248,
  riscosAltoImpacto: 12,
  riscosComTratamento: 186,
  novosRiscos: 31,
}

export const dashboardMetricConfig = [
  { icon: 'shield', label: 'Total de riscos', tone: 'blue', valueKey: 'totalRiscos' },
  { icon: 'alert', label: 'Alto impacto', tone: 'red', valueKey: 'riscosAltoImpacto' },
  { icon: 'target', label: 'Com tratamento', tone: 'gray', valueKey: 'riscosComTratamento' },
  { icon: 'chart', label: 'Novos riscos', tone: 'blue', valueKey: 'novosRiscos' },
]

export const riskBars = [
  { label: 'Extremo', cases: '12 casos', width: 13, color: '#dc2626' },
  { label: 'Alto', cases: '42 casos', width: 38, color: '#f59e0b' },
  { label: 'Moderado', cases: '94 casos', width: 66, color: '#facc15' },
  { label: 'Baixo', cases: '100 casos', width: 74, color: '#86c66f' },
]
