import { useState } from 'react'
import { Unlock } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import AuthCard from '../components/AuthCard.jsx'
import PasswordInput from '../components/PasswordInput.jsx'
import { confirmPasswordReset } from '../lib/api.js'

function ResetPassword() {
  const navigate = useNavigate()
  const email = sessionStorage.getItem('reset_email') || ''
  const codigo = sessionStorage.getItem('reset_codigo') || ''
  const [senha, setSenha] = useState('')
  const [confirmacao, setConfirmacao] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError(null)

    if (senha !== confirmacao) {
      setError('As senhas não coincidem.')
      return
    }

    setSubmitting(true)
    try {
      await confirmPasswordReset(email, codigo, senha)
      sessionStorage.removeItem('reset_email')
      sessionStorage.removeItem('reset_codigo')
      navigate('/login')
    } catch (err) {
      setError(err.data?.errors?.codigo || err.data?.errors?.senha || 'Não foi possível alterar a senha.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthCard icon={Unlock} instruction="Crie uma nova senha para acessar sua conta.">
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="form-alert error">{error}</div>}

        <label>
          <span>Nova senha</span>
          <PasswordInput
            autoComplete="new-password"
            onChange={(event) => setSenha(event.target.value)}
            required
            value={senha}
          />
        </label>

        <label>
          <span>Confirmar senha</span>
          <PasswordInput
            autoComplete="new-password"
            onChange={(event) => setConfirmacao(event.target.value)}
            required
            value={confirmacao}
          />
        </label>

        <button className="auth-submit" disabled={submitting} type="submit">
          {submitting ? 'Salvando...' : 'Confirmar'}
        </button>
      </form>
    </AuthCard>
  )
}

export default ResetPassword
