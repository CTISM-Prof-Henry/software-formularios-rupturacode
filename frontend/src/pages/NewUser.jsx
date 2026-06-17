import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ClipboardList, FileCheck2, Save, X } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { buttonTap, itemVariants, pageVariants } from '../animations/pageAnimations.js'
import FormFeedback from '../components/FormFeedback.jsx'
import FormField from '../components/FormField.jsx'
import FormSection from '../components/FormSection.jsx'
import PageHeader from '../components/PageHeader.jsx'
import SearchableSelect from '../components/SearchableSelect.jsx'
import { useCentros } from '../hooks/useCentros.js'
import { useCargos } from '../hooks/useCargos.js'
import { userFormDefaults } from '../constants/userForm.js'
import { createUsuario, getUnidades } from '../lib/api.js'

function NewUser() {
  const navigate = useNavigate()
  const [feedback, setFeedback] = useState(null)
  const centros = useCentros()
  const cargos = useCargos()
  const [unidades, setUnidades] = useState([])
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    reset,
    setValue,
    watch,
  } = useForm({ defaultValues: userFormDefaults, mode: 'onBlur' })

  const centroSelecionado = watch('centro')
  const departamentoSelecionado = watch('departamento')
  const cargoSelecionado = watch('cargo')

  useEffect(() => {
    let ignore = false

    setValue('departamento', '')

    if (!centroSelecionado) {
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
  }, [centroSelecionado, setValue])

  const unidadesDisponiveis = centroSelecionado ? unidades : []

  async function submitUser(data) {
    setFeedback(null)
    try {
      await createUsuario(data)
      reset()
      setFeedback({ text: 'Usuário cadastrado com sucesso.', type: 'success' })
    } catch (error) {
      const errs = error.data?.errors
      const text = errs
        ? Object.values(errs)[0]
        : 'Não foi possível cadastrar o usuário. Verifique se o backend está rodando.'
      setFeedback({ text, type: 'error' })
    }
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
              form="new-user-form"
              type="submit"
              whileTap={buttonTap}
            >
              <Save size={16} />
              {isSubmitting ? 'Salvando...' : 'Cadastrar novo usuario'}
            </motion.button>
          </>
        }
        description="Registrar um novo usuário/funcionário."
        kicker="Cadastro de usuário"
        title="Novo Usuario"
        variant="form"
      />

      <form className="risk-form" id="new-user-form" onSubmit={handleSubmit(submitUser)}>
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
              <input type="hidden" {...register('centro')} />
              <SearchableSelect
                options={centros.map((centro) => ({ value: centro.sigla, label: centro.nome }))}
                onChange={(value) => setValue('centro', value, { shouldDirty: true })}
                placeholder="Selecione um Centro"
                searchPlaceholder="Pesquisar centro"
                value={centroSelecionado}
              />
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
              <input
                type="hidden"
                disabled={!centroSelecionado}
                {...register('departamento', { required: 'Selecione o departamento.' })}
              />
              <SearchableSelect
                ariaInvalid={Boolean(errors.departamento)}
                disabled={!centroSelecionado}
                options={unidadesDisponiveis.map((unidade) => ({
                  value: unidade.nome,
                  label: unidade.nome,
                }))}
                onChange={(value) =>
                  setValue('departamento', value, { shouldDirty: true, shouldValidate: true })
                }
                placeholder={
                  centroSelecionado ? 'Selecione um departamento' : 'Selecione um centro primeiro'
                }
                searchPlaceholder="Pesquisar departamento"
                value={departamentoSelecionado}
              />
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
              <input type="hidden" {...register('cargo', { required: 'Informe o cargo.' })} />
              <SearchableSelect
                ariaInvalid={Boolean(errors.cargo)}
                options={cargos.map((cargo) => ({ value: cargo.value, label: cargo.label }))}
                onChange={(value) => setValue('cargo', value, { shouldDirty: true, shouldValidate: true })}
                placeholder="Selecione o cargo"
                searchPlaceholder="Pesquisar cargo"
                value={cargoSelecionado}
              />
            </FormField>

            <FormField error={errors.senha?.message} label="Senha inicial">
              <input
                aria-invalid={errors.senha ? 'true' : 'false'}
                placeholder="1234"
                type="text"
                {...register('senha', { required: 'Informe a senha inicial.' })}
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
            {isSubmitting ? 'Salvando...' : 'Cadastrar'}
          </motion.button>
        </motion.footer>
      </form>
    </motion.main>
  )
}

export default NewUser
