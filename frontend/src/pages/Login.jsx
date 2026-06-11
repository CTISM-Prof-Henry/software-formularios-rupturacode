import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AuthCard from '../components/AuthCard.jsx'
import PasswordInput from '../components/PasswordInput.jsx'
import { useAuth } from '../hooks/useAuth.js'

function Login() {
  const navigate = useNavigate()
  const { login, status } = useAuth()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (status === 'authenticated') {
      navigate('/dashboard', { replace: true })
    }
  }, [status, navigate])

  async function handleSubmit(event) {
    event.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await login(email.trim().toLowerCase(), senha)
      navigate('/dashboard', { replace: true })
    } catch (err) {
      setError(err.data?.errors?.credenciais || 'Não foi possível entrar. Tente novamente.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthCard instruction="Digite seu email e senha para logar no sistema.">
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="form-alert error">{error}</div>}

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

        <label>
          <span>Senha</span>
          <PasswordInput
            autoComplete="current-password"
            onChange={(event) => setSenha(event.target.value)}
            required
            value={senha}
          />
        </label>

        <Link className="auth-link" to="/esqueceu-senha">
          Esqueci minha senha
        </Link>

        <button className="auth-submit" disabled={submitting} type="submit">
          {submitting ? 'Entrando...' : 'Confirmar'}
        </button>
      </form>
    </AuthCard>
  )
}

export default Login
