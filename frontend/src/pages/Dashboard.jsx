import { useMemo } from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle, Eye, FileBarChart, Shield, Siren, Target } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { buttonTap, itemVariants, pageVariants } from '../animations/pageAnimations.js'
import MetricCard from '../components/MetricCard.jsx'
import PageHeader from '../components/PageHeader.jsx'
import RiskBars from '../components/RiskBars.jsx'
import RiskHeatmap from '../components/RiskHeatmap.jsx'
import { buildRiskBars, dashboardMetricConfig } from '../constants/dashboard.js'
import { useDashboardSummary } from '../hooks/useDashboardSummary.js'

const metricIcons = {
  alert: AlertTriangle,
  chart: FileBarChart,
  shield: Shield,
  target: Target,
}

function Dashboard({ onNewRisk }) {
  const navigate = useNavigate()
  const { status, summary } = useDashboardSummary()

  const metrics = useMemo(
    () =>
      dashboardMetricConfig.map((metric) => ({
        ...metric,
        icon: metricIcons[metric.icon],
        value: summary[metric.valueKey],
      })),
    [summary],
  )

  const riskBars = useMemo(
    () => buildRiskBars(summary.distribuicaoPorNivel),
    [summary],
  )

  return (
    <motion.main
      animate="visible"
      className="dashboard-page"
      initial="hidden"
      variants={pageVariants}
    >
      <PageHeader
        actions={
          <>
            <button className="secondary-button" onClick={() => navigate('/riscos')} type="button">
              <Eye size={16} />
              Veja os riscos
            </button>
            <motion.button
              className="primary-button"
              onClick={onNewRisk}
              type="button"
              whileTap={buttonTap}
            >
              <Siren size={16} />
              Reporte um risco
            </motion.button>
          </>
        }
        description="Resumo operacional dos riscos institucionais monitorados."
        kicker="Visão geral"
        statusMessage={status === 'offline' ? 'Backend indisponível. Exibindo dados de exemplo.' : null}
        title="Atlas - Gestão de Riscos"
      />

      <section className="metric-grid" aria-label="Indicadores de risco">
        {metrics.map((metric) => (
          <MetricCard
            icon={metric.icon}
            isLoading={status === 'loading'}
            key={metric.label}
            label={metric.label}
            tone={metric.tone}
            value={metric.value}
          />
        ))}
      </section>

      <section className="analysis-row">
        <motion.article className="risk-chart-card" variants={itemVariants}>
          <div className="panel-heading">
            <div>
              <h2>Gráfico de riscos</h2>
              <p>Riscos ativos por grau de impacto</p>
            </div>
            <span className="period-chip">Últimos 30 dias</span>
          </div>

          <RiskBars items={riskBars} />
        </motion.article>

        <motion.article className="risk-map-card" variants={itemVariants}>
          <div className="panel-heading">
            <div>
              <h2>Mapa de risco</h2>
              <p>Probabilidade cruzada com impacto</p>
            </div>
          </div>

          <RiskHeatmap />
        </motion.article>
      </section>
    </motion.main>
  )
}

export default Dashboard
