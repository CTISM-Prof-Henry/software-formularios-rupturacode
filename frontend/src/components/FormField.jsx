function FieldError({ message }) {
  if (!message) {
    return null
  }

  return <small className="field-error">{message}</small>
}

function FormField({ children, error, label }) {
  return (
    <div className="form-field">
      <span>{label}</span>
      {children}
      <FieldError message={error} />
    </div>
  )
}

export default FormField
