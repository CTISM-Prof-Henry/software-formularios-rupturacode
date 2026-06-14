import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { ClipboardList, FileCheck2, Save, X } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { useNavigate, useParams } from 'react-router-dom'
import { buttonTap, itemVariants, pageVariants } from '../animations/pageAnimations.js'
import FormFeedback from '../components/FormFeedback.jsx'
import FormField from '../components/FormField.jsx'
import FormSection from '../components/FormSection.jsx'
import PageHeader from '../components/PageHeader.jsx'
import { useCentros } from '../hooks/useCentros.js'
import { cargoOptions, userFormDefaults } from '../constants/userForm.js'
import { getUnidades, getUsuario, updateUsuario } from '../lib/api.js'

function usuarioToForm(usuario) {
  return {
    ...userFormDefaults,
    nome: usuario.nome || '',
    email: usuario.email || '',
    telefone: usuario.telefone || '',
    cpf: usuario.cpf || '',
    centro: usuario.centro || '',
    departamento: usuario.departamento || '',
    data_nascimento: usuario.dataNascimento || '',
    matricula: usuario.matricula || '',
    cargo: usuario.cargo || '',
    senha: '',
  }
}

function EditUser() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [feedback, setFeedback] = useState(null)
  const [loaded, setLoaded] = useState(false)
  const [loadError, setLoadError] = useState(null)
  const centros = useCentros()
  const [unidades, setUnidades] = useState([])
  // Departamento atual do usuário (garante que apareça no select mesmo sem recarregar).
  const departamentoAtual = useRef('')
  const firstCentroRun = useRef(true)

  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    reset,
    setValue,
    watch,
  } = useForm({ defaultValues: userFormDefaults, mode: 'onBlur' })

  const centroSelecionado = watch('centro')

  useEffect(() => {
    let ignore = false
    getUsuario(id)
      .then((usuario) => {
        if (!ignore) {
          departamentoAtual.current = usuario.departamento || ''
          reset(usuarioToForm(usuario))
          setLoaded(true)
        }
      })
      .catch(() => {
        if (!ignore) {
          setLoadError('Não foi possível carregar o usuário.')
        }
      })
    return () => {
      ignore = true
    }
  }, [id, reset])

  useEffect(() => {
    if (!loaded) {
      return undefined
    }
    let ignore = false

    // Não limpa o departamento no primeiro disparo (preserva o valor carregado).
    if (firstCentroRun.current) {
      firstCentroRun.current = false
    } else {
      setValue('departamento', '')
    }

    if (!centroSelecionado) {
      setUnidades([])
      return undefined
    }

    getUnidades({ centro: centroSelecionado })
      .then((data) => {
        if (!ignore) {
          setUnidades(data.results || [])
        }
      })
      .catch(() => {
        if (!ignore) {
          setUnidades([])
        }
      })

    return () => {
      ignore = true
    }
  }, [centroSelecionado, loaded, setValue])

  // Mantém o departamento atual disponível mesmo se ainda não veio na lista.
  const unidadesDisponiveis =
    centroSelecionado && departamentoAtual.current &&
    !unidades.some((u) => u.nome === departamentoAtual.current)
      ? [{ id: 'atual', nome: departamentoAtual.current }, ...unidades]
      : unidades

  async function submitUser(data) {
    setFeedback(null)
    try {
      const payload = { ...data }
      if (!payload.senha) {
        delete payload.senha
      }
      await updateUsuario(id, payload)
      navigate('/usuarios')
    } catch (error) {
      const errs = error.data?.errors
      const text = errs
        ? Object.values(errs)[0]
        : 'Não foi possível atualizar o usuário. Verifique se o backend está rodando.'
      setFeedback({ text, type: 'error' })
    }
  }

  if (loadError) {
    return <main className="new-risk-page"><p className="page-status">{loadError}</p></main>
  }

  if (!loaded) {
    return <main className="new-risk-page"><p>Carregando...</p></main>
  }

  return (
    <motion.main
      animate="visible"
      className="new-risk-page"
      initial="hidden"
      variants={pageVariants}
    >
      <PageHeader
        actions={
          <>
            <button className="link-button" onClick={() => navigate('/usuarios')} type="button">
              <X size={16} />
              Cancelar
            </button>
            <motion.button
              className="save-plan-button"
              disabled={isSubmitting}
              form="edit-user-form"
              type="submit"
              whileTap={buttonTap}
            >
              <Save size={16} />
              {isSubmitting ? 'Salvando...' : 'Salvar alterações'}
            </motion.button>
          </>
        }
        description="Atualize os dados do usuário/funcionário."
        kicker="Edição de usuário"
        title="Editar Usuario"
        variant="form"
      />

      <form className="risk-form" id="edit-user-form" onSubmit={handleSubmit(submitUser)}>
        <FormFeedback feedback={feedback} />

        <FormSection className="analysis-section" icon={FileCheck2} step="Etapa 1" title="Identificação">
          <div className="form-grid two-columns">
            <FormField error={errors.nome?.message} label="Nome completo">
              <input
                aria-invalid={errors.nome ? 'true' : 'false'}
                placeholder="fulano de tal"
                type="text"
                {...register('nome', { required: 'Informe o nome completo.' })}
              />
            </FormField>

            <FormField error={errors.centro?.message} label="Centro">
              <select {...register('centro')}>
                <option value="">Selecione um Centro</option>
                {centros.map((centro) => (
                  <option key={centro.sigla} value={centro.sigla}>
                    {centro.nome}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField error={errors.email?.message} label="Email">
              <input
                aria-invalid={errors.email ? 'true' : 'false'}
                placeholder="fulano@gmail.com"
                type="email"
                {...register('email', { required: 'Informe o e-mail.' })}
              />
            </FormField>

            <FormField error={errors.departamento?.message} label="Departamento">
              <select
                aria-invalid={errors.departamento ? 'true' : 'false'}
                disabled={!centroSelecionado}
                {...register('departamento', { required: 'Selecione o departamento.' })}
              >
                <option value="">
                  {centroSelecionado ? 'Selecione um departamento' : 'Selecione um centro primeiro'}
                </option>
                {unidadesDisponiveis.map((unidade) => (
                  <option key={unidade.id} value={unidade.nome}>
                    {unidade.nome}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Telefone">
              <input placeholder="(99)99999-9999" type="tel" {...register('telefone')} />
            </FormField>

            <FormField label="Nascimento">
              <input type="date" {...register('data_nascimento')} />
            </FormField>

            <FormField label="CPF">
              <input placeholder="000.000.000-00" type="text" {...register('cpf')} />
            </FormField>

            <FormField error={errors.matricula?.message} label="Matrícula">
              <input
                aria-invalid={errors.matricula ? 'true' : 'false'}
                placeholder="99999999"
                type="text"
                {...register('matricula', { required: 'Informe a matrícula.' })}
              />
            </FormField>
          </div>
        </FormSection>

        <FormSection
          className="evaluation-section"
          icon={ClipboardList}
          step="Etapa 2"
          title="Nível de acesso"
        >
          <div className="form-grid two-columns">
            <FormField error={errors.cargo?.message} label="Informe o cargo do usuário">
              <input
                aria-invalid={errors.cargo ? 'true' : 'false'}
                list="cargo-options"
                placeholder="coordenador"
                type="text"
                {...register('cargo', { required: 'Informe o cargo.' })}
              />
              <datalist id="cargo-options">
                {cargoOptions.map((option) => (
                  <option key={option} value={option} />
                ))}
              </datalist>
            </FormField>

            <FormField label="Nova senha (opcional)">
              <input
                placeholder="Deixe em branco para manter"
                type="text"
                {...register('senha')}
              />
            </FormField>
          </div>
        </FormSection>

        <motion.footer className="form-footer" variants={itemVariants}>
          <button className="link-button" onClick={() => navigate('/usuarios')} type="button">
            <X size={16} />
            Cancelar
          </button>
          <motion.button
            className="save-register-button"
            disabled={isSubmitting}
            type="submit"
            whileTap={buttonTap}
          >
            <Save size={16} />
            {isSubmitting ? 'Salvando...' : 'Salvar alterações'}
          </motion.button>
        </motion.footer>
      </form>
    </motion.main>
  )
}

export default EditUser
