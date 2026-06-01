function FieldError({ message }) {
  if (!message) {
    return null
  }

  return <small className="field-error">{message}</small>
}

function FormField({ children, error, label }) {
  return (
    <label>
      <span>{label}</span>
      {children}
      <FieldError message={error} />
    </label>
  )
}

export default FormField
