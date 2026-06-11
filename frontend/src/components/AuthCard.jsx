import { motion } from 'framer-motion'
import { ShieldCheck } from 'lucide-react'
import { pageVariants } from '../animations/pageAnimations.js'

function AuthCard({ children, icon: Icon = ShieldCheck, instruction }) {
  return (
    <div className="auth-screen">
      <div className="auth-brand">
        <div className="brand-mark" aria-hidden="true">
          <ShieldCheck size={22} strokeWidth={2.2} />
        </div>
        <div>
          <strong>Atlas - Gestão de Riscos</strong>
          <span>Sistema de gerenciamento de risco</span>
        </div>
      </div>

      <motion.div
        animate="visible"
        className="auth-card"
        initial="hidden"
        variants={pageVariants}
      >
        <div className="auth-card-icon" aria-hidden="true">
          <Icon size={28} strokeWidth={2} />
        </div>
        {instruction && <p className="auth-instruction">{instruction}</p>}
        {children}
      </motion.div>
    </div>
  )
}

export default AuthCard
