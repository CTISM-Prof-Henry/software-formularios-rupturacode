import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AuthCard from '../components/AuthCard.jsx'
import { requestPasswordReset } from '../lib/api.js'

function ForgotPassword() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    try {
      await requestPasswordReset(email.trim().toLowerCase())
      sessionStorage.setItem('reset_email', email.trim().toLowerCase())
      navigate('/codigo')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthCard instruction="Digite seu email para receber o código de verificação.">
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          <span>Email</span>
          <input
            autoComplete="email"
            onChange={(event) => setEmail(event.target.value)}
            placeholder="exemplo@exemplo.com"
            required
            type="email"
            value={email}
          />
        </label>

        <Link className="auth-link" to="/login">
          Voltar ao login
        </Link>

        <button className="auth-submit" disabled={submitting} type="submit">
          {submitting ? 'Enviando...' : 'Continuar'}
        </button>
      </form>
    </AuthCard>
  )
}

export default ForgotPassword
