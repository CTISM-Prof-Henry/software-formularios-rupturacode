// Escala métrica de risco (1-5 por eixo) — espelha riscos/scoring.py no backend.
// Fonte única usada por RiskForm, RiskHeatmap e LevelChip.

export const probabilityScale = [
  { value: 1, label: 'Muito Baixa' },
  { value: 2, label: 'Baixa' },
  { value: 3, label: 'Média' },
  { value: 4, label: 'Alta' },
  { value: 5, label: 'Muito Alta' },
]

export const impactScale = [
  { value: 1, label: 'Insignificante' },
  { value: 2, label: 'Pequeno' },
  { value: 3, label: 'Moderado' },
  { value: 4, label: 'Grande' },
  { value: 5, label: 'Catastrófico' },
]

// Níveis por faixa de score (1-25). tone alimenta as classes .level-chip do CSS.
export const levels = {
  BAIXO: { label: 'BAIXO', tone: 'low', color: '#86c66f' },
  MODERADO: { label: 'MODERADO', tone: 'medium', color: '#facc15' },
  ALTO: { label: 'ALTO', tone: 'high', color: '#f59e0b' },
  EXTREMO: { label: 'EXTREMO', tone: 'critical', color: '#dc2626' },
}

export function scaleValue(scale, raw) {
  if (raw === undefined || raw === null || raw === '') {
    return null
  }
  const found = scale.find((o) => o.label === raw || String(o.value) === String(raw))
  return found ? found.value : null
}

export function riskScore(probability, impact) {
  const p = scaleValue(probabilityScale, probability)
  const i = scaleValue(impactScale, impact)
  if (!p || !i) {
    return null
  }
  return p * i
}

function levelFromScore(score) {
  if (!score) {
    return ''
  }
  if (score <= 4) {
    return 'BAIXO'
  }
  if (score <= 9) {
    return 'MODERADO'
  }
  if (score <= 16) {
    return 'ALTO'
  }
  return 'EXTREMO'
}

export function levelFromPI(probability, impact) {
  return levelFromScore(riskScore(probability, impact))
}
