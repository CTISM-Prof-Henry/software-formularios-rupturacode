import { motion } from 'framer-motion'
import { itemVariants } from '../animations/pageAnimations.js'

function MetricCard({ icon: Icon, isLoading, label, tone, value }) {
  return (
    <motion.article className="metric-card" variants={itemVariants}>
      <div>
        <span>{label}</span>
        <strong>{isLoading ? '...' : value}</strong>
      </div>
      <span className={`metric-icon ${tone}`}>
        <Icon size={20} strokeWidth={1.9} />
      </span>
    </motion.article>
  )
}

export default MetricCard
