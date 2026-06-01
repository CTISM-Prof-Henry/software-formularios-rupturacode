const JSON_HEADERS = {
  'Content-Type': 'application/json',
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: JSON_HEADERS,
    ...options,
  })

  const contentType = response.headers.get('content-type') || ''
  const data = contentType.includes('application/json') ? await response.json() : null

  if (!response.ok) {
    const error = new Error('Falha ao comunicar com o backend.')
    error.status = response.status
    error.data = data
    throw error
  }

  return data
}

export function getDashboardSummary() {
  return request('/api/dashboard/')
}

export function createRisk(payload) {
  return request('/api/riscos/', {
    body: JSON.stringify(payload),
    method: 'POST',
  })
}
