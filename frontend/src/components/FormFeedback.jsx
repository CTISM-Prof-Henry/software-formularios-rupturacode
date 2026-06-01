import { AnimatePresence, motion } from 'framer-motion'

function FormFeedback({ feedback }) {
  return (
    <AnimatePresence>
      {feedback && (
        <motion.div
          animate={{ opacity: 1, y: 0 }}
          className={`form-alert ${feedback.type}`}
          exit={{ opacity: 0, y: -6 }}
          initial={{ opacity: 0, y: -6 }}
          role="status"
        >
          {feedback.text}
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default FormFeedback
