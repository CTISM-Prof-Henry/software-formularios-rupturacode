function StatusChip({ active }) {
  return (
    <span className={`status-chip ${active ? 'active' : 'inactive'}`}>
      <span className="status-dot" aria-hidden="true" />
      {active ? 'Ativo' : 'Inativo'}
    </span>
  )
}

export default StatusChip
