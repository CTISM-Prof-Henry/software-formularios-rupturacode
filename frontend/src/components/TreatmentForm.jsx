import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ShieldCheck, Save, X } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { buttonTap, itemVariants, pageVariants } from '../animations/pageAnimations.js'
import FormFeedback from './FormFeedback.jsx'
import FormField from './FormField.jsx'
import FormSection from './FormSection.jsx'
import PageHeader from './PageHeader.jsx'
import SearchableSelect from './SearchableSelect.jsx'
import { getUsuarios } from '../lib/api.js'
import {
  responseOptions,
  statusOptions,
  treatmentFormDefaults,
} from '../constants/treatmentForm.js'

function TreatmentForm({
  defaultValues = treatmentFormDefaults,
  description,
  kicker,
  onCancel,
  onSubmit,
  submitLabel = 'Salvar tratamento',
  title,
}) {
  const [submitFeedback, setSubmitFeedback] = useState(null)
  const [usuarios, setUsuarios] = useState([])
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    reset,
    setValue,
    watch,
  } = useForm({ defaultValues, mode: 'onBlur' })

  const resposta = watch('resposta')
  const usuarioResponsavelId = watch('usuarioResponsavelId')
  const isAceitar = resposta === 'aceitar'

  useEffect(() => {
    let ignore = false
    getUsuarios()
      .then((data) => {
        if (!ignore) {
          setUsuarios(data.results || [])
        }
      })
      .catch(() => {
        if (!ignore) {
          setUsuarios([])
        }
      })
    return () => {
      ignore = true
    }
  }, [])

  // Responsável é um select de opções assíncronas: re-aplica o valor salvo quando
  // a lista de usuários chega (senão o campo aparece vazio na edição).
  useEffect(() => {
    if (usuarios.length && defaultValues.usuarioResponsavelId) {
      setValue('usuarioResponsavelId', defaultValues.usuarioResponsavelId)
    }
  }, [usuarios, defaultValues.usuarioResponsavelId, setValue])

  async function handleFormSubmit(data) {
    setSubmitFeedback(null)
    try {
      const feedback = await onSubmit(data, reset)
      if (feedback) {
        setSubmitFeedback(feedback)
      }
    } catch (error) {
      setSubmitFeedback({
        text:
          error.data?.errors?.body ||
          'Não foi possível salvar o tratamento. Verifique se o backend está rodando.',
        type: 'error',
      })
    }
  }

  function handleCancel() {
    if (onCancel) {
      onCancel()
      return
    }
    reset()
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
            <button className="link-button" type="button" onClick={handleCancel}>
              <X size={16} />
              Cancelar
            </button>
            <motion.button
              className="save-plan-button"
              disabled={isSubmitting}
              form="treatment-form"
              type="submit"
              whileTap={buttonTap}
            >
              <Save size={16} />
              {isSubmitting ? 'Salvando...' : submitLabel}
            </motion.button>
          </>
        }
        description={description}
        kicker={kicker}
        title={title}
        variant="form"
      />

      <form
        className="risk-form"
        id="treatment-form"
        onSubmit={handleSubmit(handleFormSubmit)}
      >
        <FormFeedback feedback={submitFeedback} />

        <FormSection
          className="treatment-section"
          icon={ShieldCheck}
          step="Resposta"
          title="Plano de tratamento"
        >
          <div className="form-grid two-columns">
            <FormField label="Resposta ao risco">
              <select {...register('resposta')}>
                {responseOptions.map((o) => (
                  <option key={o.value} value={o.value}>
                    {o.label}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField label="Responsável">
              <input type="hidden" {...register('usuarioResponsavelId')} />
              <SearchableSelect
                options={usuarios.map((u) => ({ value: String(u.id), label: u.nome }))}
                onChange={(value) => setValue('usuarioResponsavelId', value, { shouldDirty: true })}
                placeholder="Selecione o responsável"
                searchPlaceholder="Pesquisar responsável"
                value={usuarioResponsavelId}
              />
            </FormField>
          </div>

          <FormField error={errors.acao?.message} label="Ação (detalhamento)">
            <input
              aria-invalid={errors.acao ? 'true' : 'false'}
              placeholder="O que exatamente será feito..."
              type="text"
              {...register('acao', {
                validate: (value) =>
                  isAceitar || value.trim() !== '' || 'Informe a ação do tratamento.',
              })}
            />
          </FormField>

          <div className="form-grid two-columns">
            <FormField label="Data início">
              <input type="date" {...register('dataInicio')} />
            </FormField>

            <FormField error={errors.dataFim?.message} label="Data fim (prazo)">
              <input
                aria-invalid={errors.dataFim ? 'true' : 'false'}
                type="date"
                {...register('dataFim', {
                  validate: (value) =>
                    isAceitar || value !== '' || 'Informe o prazo do tratamento.',
                })}
              />
            </FormField>
          </div>

          <FormField label="Situação atual">
            <select {...register('situacao')}>
              {statusOptions.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
          </FormField>
        </FormSection>

        <motion.footer className="form-footer" variants={itemVariants}>
          <button className="link-button" type="button" onClick={handleCancel}>
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
            {isSubmitting ? 'Salvando...' : submitLabel}
          </motion.button>
        </motion.footer>
      </form>
    </motion.main>
  )
}

export default TreatmentForm
