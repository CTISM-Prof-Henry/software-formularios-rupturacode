import { useEffect, useState } from 'react'
import { getCargos } from '../lib/api.js'

// Cargos canonicos (fonte da verdade no backend: core/permissions.CARGO_CHOICES).
// Cada item: { value, label, nivel }.
export function useCargos() {
  const [cargos, setCargos] = useState([])

  useEffect(() => {
    let ignore = false

    getCargos()
      .then((data) => {
        if (!ignore) {
          setCargos(data.results || [])
        }
      })
      .catch(() => {
        if (!ignore) {
          setCargos([])
        }
      })

    return () => {
      ignore = true
    }
  }, [])

  return cargos
}
