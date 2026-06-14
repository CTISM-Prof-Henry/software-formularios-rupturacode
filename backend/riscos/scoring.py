"""Risk level scoring from Probability x Impact.

Metric 1-5 scale on each axis; level derived from the score band (1-25).
This is the single source of truth on the backend; the frontend mirrors it in
``frontend/src/constants/riskScale.js``.
"""

# Label -> metric value (1-5). Lower-cased keys, accent-tolerant.
PROBABILIDADE_ESCALA = {
    "muito baixa": 1,
    "baixa": 2,
    "média": 3,
    "media": 3,
    "alta": 4,
    "muito alta": 5,
}

IMPACTO_ESCALA = {
    "insignificante": 1,
    "pequeno": 2,
    "moderado": 3,
    "grande": 4,
    "catastrófico": 5,
    "catastrofico": 5,
}

NIVEL_BAIXO = "BAIXO"
NIVEL_MODERADO = "MODERADO"
NIVEL_ALTO = "ALTO"
NIVEL_EXTREMO = "EXTREMO"


def _to_valor(raw, escala):
    """Map a label or a 1-5 number to its metric value, or None if unmappable."""
    if raw is None:
        return None
    texto = str(raw).strip().lower()
    if texto in escala:
        return escala[texto]
    if texto.isdigit():
        numero = int(texto)
        return numero if 1 <= numero <= 5 else None
    return None


def score(probabilidade, impacto):
    """Return Probability x Impact (1-25), or None if either axis is unmappable."""
    prob = _to_valor(probabilidade, PROBABILIDADE_ESCALA)
    imp = _to_valor(impacto, IMPACTO_ESCALA)
    if prob is None or imp is None:
        return None
    return prob * imp


def nivel_por_score(valor):
    """Map a 1-25 score to a level. Empty string for None (unmappable input)."""
    if valor is None:
        return ""
    if valor <= 4:
        return NIVEL_BAIXO
    if valor <= 9:
        return NIVEL_MODERADO
    if valor <= 16:
        return NIVEL_ALTO
    return NIVEL_EXTREMO


def nivel_de_risco(probabilidade, impacto):
    """Compute the risk level directly from probability and impact."""
    return nivel_por_score(score(probabilidade, impacto))
