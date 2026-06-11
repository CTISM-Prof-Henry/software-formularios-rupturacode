import { useEffect, useState } from 'react'
import { getCentros } from '../lib/api.js'

export function useCentros() {
  const [centros, setCentros] = useState([])

  useEffect(() => {
    let ignore = false

    getCentros()
      .then((data) => {
        if (!ignore) {
          setCentros(data.results || [])
        }
      })
      .catch(() => {
        if (!ignore) {
          setCentros([])
        }
      })

    return () => {
      ignore = true
    }
  }, [])

  return centros
}
