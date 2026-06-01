import { useEffect, useState } from 'react'
import { fallbackSummary } from '../constants/dashboard.js'
import { getDashboardSummary } from '../lib/api.js'

export function useDashboardSummary() {
  const [summary, setSummary] = useState(fallbackSummary)
  const [status, setStatus] = useState('idle')

  useEffect(() => {
    let ignore = false

    async function loadSummary() {
      setStatus('loading')

      try {
        const data = await getDashboardSummary()

        if (!ignore) {
          setSummary({
            novosRiscos: data.novosRiscos ?? 0,
            riscosAltoImpacto: data.riscosAltoImpacto ?? 0,
            riscosComTratamento: data.riscosComTratamento ?? 0,
            totalRiscos: data.totalRiscos ?? 0,
          })
          setStatus('loaded')
        }
      } catch {
        if (!ignore) {
          setStatus('offline')
        }
      }
    }

    loadSummary()

    return () => {
      ignore = true
    }
  }, [])

  return { status, summary }
}
