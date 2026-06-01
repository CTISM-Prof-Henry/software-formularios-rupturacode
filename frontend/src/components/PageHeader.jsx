import { motion } from 'framer-motion'
import { itemVariants } from '../animations/pageAnimations.js'

function PageHeader({ actions, description, kicker, statusMessage, title, variant = 'dashboard' }) {
  const className = variant === 'form' ? 'form-header' : 'dashboard-header'

  return (
    <motion.header className={className} variants={itemVariants}>
      <div>
        <span className="page-kicker">{kicker}</span>
        <h1>{title}</h1>
        <p>{description}</p>
        {statusMessage && <p className="page-status">{statusMessage}</p>}
      </div>

      {actions && <div className={variant === 'form' ? 'form-actions' : 'header-actions'}>{actions}</div>}
    </motion.header>
  )
}

export default PageHeader
