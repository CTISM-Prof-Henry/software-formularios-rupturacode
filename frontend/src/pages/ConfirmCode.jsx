import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AuthCard from '../components/AuthCard.jsx'
import { requestPasswordReset, verifyResetCode } from '../lib/api.js'

function ConfirmCode() {
  const navigate = useNavigate()
  const email = sessionStorage.getItem('reset_email') || ''
  const [codigo, setCodigo] = useState('')
  const [error, setError] = useState(null)
  const [info, setInfo] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await verifyResetCode(email, codigo.trim())
      sessionStorage.setItem('reset_codigo', codigo.trim())
      navigate('/alterar-senha')
    } catch (err) {
      setError(err.data?.errors?.codigo || 'Código inválido ou expirado.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleResend() {
    setInfo(null)
    setError(null)
    if (email) {
      await requestPasswordReset(email)
      setInfo('Novo código enviado.')
    }
  }

  return (
    <AuthCard instruction="Digite o código recebido no email.">
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="form-alert error">{error}</div>}
        {info && <div className="form-alert success">{info}</div>}

        <label>
          <span>Código</span>
          <input
            inputMode="numeric"
            onChange={(event) => setCodigo(event.target.value)}
            placeholder="123456"
            required
            type="text"
            value={codigo}
          />
        </label>

        <button className="auth-link as-button" onClick={handleResend} type="button">
          Reenviar código
        </button>

        <button className="auth-submit" disabled={submitting} type="submit">
          {submitting ? 'Verificando...' : 'Confirmar'}
        </button>
      </form>
    </AuthCard>
  )
}

export default ConfirmCode
