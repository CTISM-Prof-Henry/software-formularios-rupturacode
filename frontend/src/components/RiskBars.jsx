function RiskBars({ items }) {
  return (
    <div className="risk-bars">
      {items.map((bar) => (
        <div className="risk-bar-item" key={bar.label}>
          <div className="bar-heading">
            <strong>{bar.label}</strong>
            <span>{bar.cases}</span>
          </div>
          <div className="bar-track">
            <span style={{ '--bar-width': `${bar.width}%`, '--bar-color': bar.color }} />
          </div>
        </div>
      ))}
    </div>
  )
}

export default RiskBars
