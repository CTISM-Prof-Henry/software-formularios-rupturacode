// Espelha as choices de tratamentos/models.py (value = código gravado no backend).

export const responseOptions = [
  { value: 'mitigar', label: 'Mitigar / Reduzir' },
  { value: 'evitar', label: 'Evitar' },
  { value: 'transferir', label: 'Transferir' },
  { value: 'aceitar', label: 'Aceitar' },
]

export const statusOptions = [
  { value: 'nao_iniciado', label: 'Não Iniciado' },
  { value: 'em_andamento', label: 'Em andamento' },
  { value: 'concluido', label: 'Concluído' },
  { value: 'suspenso', label: 'Suspenso' },
]

export const treatmentFormDefaults = {
  resposta: 'mitigar',
  usuarioResponsavelId: '',
  acao: '',
  dataInicio: '',
  dataFim: '',
  situacao: 'nao_iniciado',
}

function labelFrom(options, value) {
  const found = options.find((o) => o.value === value)
  return found ? found.label : value || '—'
}

export const responseLabel = (value) => labelFrom(responseOptions, value)
export const statusLabel = (value) => labelFrom(statusOptions, value)
