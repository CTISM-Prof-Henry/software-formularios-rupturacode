import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ClipboardList, FileCheck2, Save, ShieldCheck, X } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { buttonTap, itemVariants, pageVariants } from '../animations/pageAnimations.js'
import FormFeedback from './FormFeedback.jsx'
import FormField from './FormField.jsx'
import FormSection from './FormSection.jsx'
import LevelChip from './LevelChip.jsx'
import PageHeader from './PageHeader.jsx'
import RiskHeatmap from './RiskHeatmap.jsx'
import SearchableSelect from './SearchableSelect.jsx'
import { getUnidades } from '../lib/api.js'
import {
  controlOptions,
  impactOptions,
  probabilityOptions,
  riskFormDefaults,
  riskTypeOptions,
} from '../constants/riskForm.js'
import { levelFromPI, riskScore } from '../constants/riskScale.js'

function SelectOptions({ options }) {
  return options.map((option) => <option key={option}>{option}</option>)
}

// Garante que o valor salvo (ex.: vocabulário legado fora da escala atual) apareça
// como opção, senão o select cai no default e o campo fica "vazio" na edição.
function withCurrent(options, current) {
  return current && !options.includes(current) ? [current, ...options] : options
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
    setValue,
    watch,
  } = useForm({ defaultValues, mode: 'onBlur' })

  const probability = watch('probability')
  const impact = watch('impact')
  const department = watch('department')
  const computedScore = riskScore(probability, impact)
  const computedLevel = levelFromPI(probability, impact)

  const probabilityResidual = watch('probabilityResidual')
  const impactResidual = watch('impactResidual')
  const residualScore = riskScore(probabilityResidual, impactResidual)
  const residualLevel = levelFromPI(probabilityResidual, impactResidual)

  const heatmapMarkers = []
  if (computedScore) {
    heatmapMarkers.push({ probability, impact, label: 'Inerente', kind: 'inerente' })
  }
  if (residualScore) {
    heatmapMarkers.push({
      probability: probabilityResidual,
      impact: impactResidual,
      label: 'Residual',
      kind: 'residual',
    })
  }

  // Níveis são derivados de Probabilidade x Impacto; mantém os campos no payload
  // (o backend recalcula de qualquer forma).
  useEffect(() => {
    setValue('riskLevel', computedLevel)
  }, [computedLevel, setValue])

  useEffect(() => {
    setValue('residualLevel', residualLevel)
  }, [residualLevel, setValue])

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

  // Inclui o valor salvo como opção quando ele não está na lista padrão (dados legados).
  const riskTypeOpts = withCurrent(riskTypeOptions, defaultValues.riskType)
  const probabilityOpts = withCurrent(probabilityOptions, defaultValues.probability)
  const impactOpts = withCurrent(impactOptions, defaultValues.impact)
  const controlOpts = withCurrent(controlOptions, defaultValues.internalControls)
  const probabilityResidualOpts = withCurrent(probabilityOptions, defaultValues.probabilityResidual)
  const impactResidualOpts = withCurrent(impactOptions, defaultValues.impactResidual)

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
              <input
                type="hidden"
                {...register('department', { required: 'Informe o setor ou departamento.' })}
              />
              <SearchableSelect
                ariaInvalid={Boolean(errors.department)}
                options={departmentOptions.map((unidade) => ({
                  value: unidade.nome,
                  label: unidade.nome,
                }))}
                onChange={(value) =>
                  setValue('department', value, { shouldDirty: true, shouldValidate: true })
                }
                placeholder="Selecione a unidade"
                searchPlaceholder="Pesquisar unidade"
                value={department}
              />
            </FormField>

            <FormField error={errors.riskType?.message} label="Tipo de risco">
              <select
                aria-invalid={errors.riskType ? 'true' : 'false'}
                {...register('riskType', { required: 'Selecione o tipo de risco.' })}
              >
                <option disabled value="">
                  Selecione o tipo de risco
                </option>
                <SelectOptions options={riskTypeOpts} />
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
          <div className="form-grid four-columns">
            <FormField label="Probabilidade">
              <select {...register('probability')}>
                <SelectOptions options={probabilityOpts} />
              </select>
            </FormField>

            <FormField label="Impacto">
              <select {...register('impact')}>
                <SelectOptions options={impactOpts} />
              </select>
            </FormField>

            <FormField label="Nível de risco">
              <div className="computed-level">
                <LevelChip level={computedLevel} />
                {computedScore ? <span className="computed-level-score">{computedScore}</span> : null}
              </div>
              <input type="hidden" {...register('riskLevel')} />
            </FormField>

            <FormField label="Controles internos">
              <select {...register('internalControls')}>
                <SelectOptions options={controlOpts} />
              </select>
            </FormField>
          </div>
        </FormSection>

        <FormSection
          className="treatment-section"
          icon={ShieldCheck}
          step="Risco residual"
          title="Reavaliação pós-tratamento"
        >
          <p className="section-hint">
            Preencha após a conclusão do tratamento: o nível residual é recalculado a partir
            da nova probabilidade e impacto.
          </p>
          <div className="form-grid three-columns">
            <FormField label="Probabilidade residual">
              <select {...register('probabilityResidual')}>
                <option value="">—</option>
                <SelectOptions options={probabilityResidualOpts} />
              </select>
            </FormField>

            <FormField label="Impacto residual">
              <select {...register('impactResidual')}>
                <option value="">—</option>
                <SelectOptions options={impactResidualOpts} />
              </select>
            </FormField>

            <FormField label="Nível residual">
              <div className="computed-level">
                <LevelChip level={residualLevel} />
                {residualScore ? <span className="computed-level-score">{residualScore}</span> : null}
              </div>
              <input type="hidden" {...register('residualLevel')} />
            </FormField>
          </div>

          <div className="risk-form-matrix">
            <span className="section-hint">
              Posição na matriz — ▣ inerente · ◯ residual
            </span>
            <RiskHeatmap markers={heatmapMarkers} />
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
