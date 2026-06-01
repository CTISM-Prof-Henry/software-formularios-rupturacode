import { motion } from 'framer-motion'
import { itemVariants } from '../animations/pageAnimations.js'

function FormSection({ children, className, icon: Icon, step, title }) {
  return (
    <motion.section className={`form-section ${className}`} variants={itemVariants}>
      <div className="section-heading">
        <div className="section-icon">
          <Icon size={17} />
        </div>
        <div>
          <span>{step}</span>
          <h2>{title}</h2>
        </div>
      </div>

      {children}
    </motion.section>
  )
}

export default FormSection
