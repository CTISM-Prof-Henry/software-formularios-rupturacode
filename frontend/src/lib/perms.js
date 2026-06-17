// Helpers de permissao por nivel (espelham core/permissions do backend).
// O nivel efetivo vem da API em user.nivel ('leitor' | 'editor' | 'admin').
const ORDER = { leitor: 0, editor: 1, admin: 2 }

function nivelDe(user) {
  return user?.nivel || 'leitor'
}

export function podeEditarRiscos(user) {
  return ORDER[nivelDe(user)] >= ORDER.editor
}

export function podeGerirUsuarios(user) {
  return ORDER[nivelDe(user)] >= ORDER.admin
}
