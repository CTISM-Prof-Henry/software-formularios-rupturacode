import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ClipboardList, FileCheck2, Save, ShieldCheck, X } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { buttonTap, itemVariants, pageVariants } from '../animations/pageAnimations.js'
import FormFeedback from './FormFeedback.jsx'
import FormField from './FormField.jsx'
import FormSection from './FormSection.jsx'
import PageHeader from './PageHeader.jsx'
import { getUnidades } from '../lib/api.js'
import {
  controlOptions,
  impactOptions,
  probabilityOptions,
  residualOptions,
  responseOptions,
  riskFormDefaults,
  riskLevelOptions,
  riskTypeOptions,
  statusOptions,
} from '../constants/riskForm.js'

function SelectOptions({ options }) {
  return options.map((option) => <option key={option}>{option}</option>)
}

function RiskForm({
  defaultValues = riskFormDefaults,
  description,
  kicker,
  onCancel,
  onSubmit,
  submitLabel = 'Salvar registro',
  title,
}) {
  const [submitFeedback, setSubmitFeedback] = useState(null)
  const [unidades, setUnidades] = useState([])
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    reset,
  } = useForm({ defaultValues, mode: 'onBlur' })

  useEffect(() => {
    let ignore = false
    getUnidades()
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
  }, [])

  // Garante que o valor atual (ex.: ao editar) apareça mesmo se não estiver na lista.
  const currentDepartment = defaultValues.department
  const departmentOptions =
    currentDepartment && !unidades.some((u) => u.nome === currentDepartment)
      ? [{ id: 'atual', nome: currentDepartment }, ...unidades]
      : unidades

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
          'Não foi possível salvar o risco. Verifique se o backend está rodando.',
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
              form="risk-form"
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

      <form className="risk-form" id="risk-form" onSubmit={handleSubmit(handleFormSubmit)}>
        <FormFeedback feedback={submitFeedback} />

        <FormSection
          className="analysis-section"
          icon={FileCheck2}
          step="Etapa 1"
          title="Identificação e análise"
        >
          <div className="form-grid two-columns">
            <FormField error={errors.department?.message} label="Setor/Departamento">
              <select
                aria-invalid={errors.department ? 'true' : 'false'}
                {...register('department', { required: 'Informe o setor ou departamento.' })}
              >
                <option value="">Selecione a unidade</option>
                {departmentOptions.map((unidade) => (
                  <option key={unidade.id} value={unidade.nome}>
                    {unidade.nome}
                  </option>
                ))}
              </select>
            </FormField>

            <FormField error={errors.riskType?.message} label="Tipo de risco">
              <select
                aria-invalid={errors.riskType ? 'true' : 'false'}
                {...register('riskType', { required: 'Selecione o tipo de risco.' })}
              >
                <option disabled value="">
                  Selecione o tipo de risco
                </option>
                <SelectOptions options={riskTypeOptions} />
              </select>
            </FormField>
          </div>

          <FormField error={errors.identifiedRisk?.message} label="Risco identificado">
            <textarea
              aria-invalid={errors.identifiedRisk ? 'true' : 'false'}
              placeholder="Descreva detalhadamente o evento de risco identificado..."
              {...register('identifiedRisk', {
                minLength: { message: 'Descreva o risco com mais detalhes.', value: 12 },
                required: 'Descreva o risco identificado.',
              })}
            />
          </FormField>
        </FormSection>

        <FormSection
          className="evaluation-section"
          icon={ClipboardList}
          step="Etapa 2"
          title="Avaliação"
        >
          <div className="form-grid five-columns">
            <FormField label="Probabilidade">
              <select {...register('probability')}>
                <SelectOptions options={probabilityOptions} />
              </select>
            </FormField>

            <FormField label="Impacto">
              <select {...register('impact')}>
                <SelectOptions options={impactOptions} />
              </select>
            </FormField>

            <FormField label="Nível de risco">
              <select className="critical-select" {...register('riskLevel')}>
                <SelectOptions options={riskLevelOptions} />
              </select>
            </FormField>

            <FormField label="Controles internos">
              <select {...register('internalControls')}>
                <SelectOptions options={controlOptions} />
              </select>
            </FormField>

            <FormField label="Nível residual">
              <select className="residual-select" {...register('residualLevel')}>
                <SelectOptions options={residualOptions} />
              </select>
            </FormField>
          </div>
        </FormSection>

        <FormSection
          className="treatment-section"
          icon={ShieldCheck}
          step="Etapa 3"
          title="Tratamento"
        >
          <div className="form-grid treatment-grid">
            <FormField label="Resposta ao risco">
              <select {...register('riskResponse')}>
                <SelectOptions options={responseOptions} />
              </select>
            </FormField>

            <FormField error={errors.actionPlan?.message} label="Plano de ação">
              <input
                aria-invalid={errors.actionPlan ? 'true' : 'false'}
                placeholder="Ação imediata para contenção do risco..."
                type="text"
                {...register('actionPlan', { required: 'Informe o plano de ação.' })}
              />
            </FormField>

            <FormField label="Data início">
              <input type="date" {...register('startDate')} />
            </FormField>

            <FormField label="Data fim (previsão)">
              <input type="date" {...register('dueDate')} />
            </FormField>

            <FormField label="Situação atual">
              <select {...register('status')}>
                <SelectOptions options={statusOptions} />
              </select>
            </FormField>
          </div>
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

export default RiskForm
