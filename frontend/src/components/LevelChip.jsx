function levelTone(level) {
  const value = (level || '').toString().trim().toUpperCase()
  if (['CRÍTICO', 'CRITICO', 'ALTO', 'EXTREMO'].includes(value)) {
    return value === 'CRÍTICO' || value === 'CRITICO' || value === 'EXTREMO' ? 'critical' : 'high'
  }
  if (['MODERADO', 'MÉDIO', 'MEDIO'].includes(value)) {
    return 'medium'
  }
  if (['BAIXO'].includes(value)) {
    return 'low'
  }
  return 'neutral'
}

function LevelChip({ level }) {
  if (!level) {
    return <span className="level-chip neutral">—</span>
  }
  return <span className={`level-chip ${levelTone(level)}`}>{level}</span>
}

export default LevelChip
