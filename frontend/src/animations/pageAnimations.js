export const pageVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: {
    opacity: 1,
    transition: { duration: 0.28, ease: 'easeOut', staggerChildren: 0.06 },
    y: 0,
  },
}

export const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, transition: { duration: 0.24, ease: 'easeOut' }, y: 0 },
}

export const buttonTap = {
  scale: 0.98,
}
