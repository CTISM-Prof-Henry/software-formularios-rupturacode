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

function buildQuery(params = {}) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && String(value).trim() !== '') {
      query.set(key, value)
    }
  })
  const serialized = query.toString()
  return serialized ? `?${serialized}` : ''
}

// Dashboard ------------------------------------------------------------------
export function getDashboardSummary() {
  return request('/api/dashboard/')
}

// Riscos ---------------------------------------------------------------------
export function getRiscos(params) {
  return request(`/api/riscos/${buildQuery(params)}`)
}

export function getRisco(id) {
  return request(`/api/riscos/${id}/`)
}

export function createRisk(payload) {
  return request('/api/riscos/', { body: JSON.stringify(payload), method: 'POST' })
}

export function updateRisco(id, payload) {
  return request(`/api/riscos/${id}/`, { body: JSON.stringify(payload), method: 'PUT' })
}

export function deleteRisco(id) {
  return request(`/api/riscos/${id}/`, { method: 'DELETE' })
}

// Usuarios -------------------------------------------------------------------
export function getUsuarios(params) {
  return request(`/api/usuarios/${buildQuery(params)}`)
}

export function getUsuario(id) {
  return request(`/api/usuarios/${id}/`)
}

export function createUsuario(payload) {
  return request('/api/usuarios/', { body: JSON.stringify(payload), method: 'POST' })
}

export function updateUsuario(id, payload) {
  return request(`/api/usuarios/${id}/`, { body: JSON.stringify(payload), method: 'PUT' })
}

// Subunidades (unidades UFSM) ------------------------------------------------
export function getCentros() {
  return request('/api/subunidades/centros/')
}

export function getUnidades(params) {
  return request(`/api/subunidades/${buildQuery(params)}`)
}

// Auth -----------------------------------------------------------------------
export function login(payload) {
  return request('/api/auth/login/', { body: JSON.stringify(payload), method: 'POST' })
}

export function logout() {
  return request('/api/auth/logout/', { method: 'POST' })
}

export function me() {
  return request('/api/auth/me/')
}

export function requestPasswordReset(email) {
  return request('/api/auth/password-reset/request/', {
    body: JSON.stringify({ email }),
    method: 'POST',
  })
}

export function verifyResetCode(email, codigo) {
  return request('/api/auth/password-reset/verify/', {
    body: JSON.stringify({ email, codigo }),
    method: 'POST',
  })
}

export function confirmPasswordReset(email, codigo, senha) {
  return request('/api/auth/password-reset/confirm/', {
    body: JSON.stringify({ email, codigo, senha }),
    method: 'POST',
  })
}
