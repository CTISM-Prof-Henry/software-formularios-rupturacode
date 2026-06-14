import { levels } from './riskScale.js'

export const fallbackSummary = {
  totalRiscos: 0,
  riscosAltoImpacto: 0,
  riscosComTratamento: 0,
  novosRiscos: 0,
  distribuicaoPorNivel: { BAIXO: 0, MODERADO: 0, ALTO: 0, EXTREMO: 0 },
}

export const dashboardMetricConfig = [
  { icon: 'shield', label: 'Total de riscos', tone: 'blue', valueKey: 'totalRiscos' },
  { icon: 'alert', label: 'Alto impacto', tone: 'red', valueKey: 'riscosAltoImpacto' },
  { icon: 'target', label: 'Com tratamento', tone: 'gray', valueKey: 'riscosComTratamento' },
  { icon: 'chart', label: 'Novos riscos', tone: 'blue', valueKey: 'novosRiscos' },
]

// Ordem de exibição das barras por nível (cor vem da escala única).
const barConfig = [
  { key: 'EXTREMO', label: 'Extremo' },
  { key: 'ALTO', label: 'Alto' },
  { key: 'MODERADO', label: 'Moderado' },
  { key: 'BAIXO', label: 'Baixo' },
]

// Monta os itens do RiskBars a partir da distribuição por nível vinda da API.
export function buildRiskBars(distribuicao = {}) {
  const valores = barConfig.map(({ key }) => distribuicao[key] || 0)
  const maximo = Math.max(1, ...valores)
  return barConfig.map(({ key, label }) => {
    const total = distribuicao[key] || 0
    return {
      label,
      cases: `${total} ${total === 1 ? 'caso' : 'casos'}`,
      width: Math.round((total / maximo) * 100),
      color: levels[key].color,
    }
  })
}
