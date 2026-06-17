from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from riscos.models import Risco
from riscos.scoring import IMPACTO_ESCALA, PROBABILIDADE_ESCALA, _to_valor
from tratamentos.models import Tratamento

from .auth import login_required_session


def _normalize(value):
    return str(value or "").strip().lower()


# Sinônimos legados -> nível canônico (mesma escala de riscos/scoring.py).
_NIVEL_CANONICO = {
    "baixo": "BAIXO",
    "moderado": "MODERADO",
    "médio": "MODERADO",
    "medio": "MODERADO",
    "alto": "ALTO",
    "extremo": "EXTREMO",
    "crítico": "EXTREMO",
    "critico": "EXTREMO",
}


def _distribuicao_por_nivel(riscos_ativos):
    distribuicao = {"BAIXO": 0, "MODERADO": 0, "ALTO": 0, "EXTREMO": 0}
    for nivel in riscos_ativos.values_list("nivel_de_risco", flat=True):
        canonico = _NIVEL_CANONICO.get(_normalize(nivel))
        if canonico:
            distribuicao[canonico] += 1
    return distribuicao


def _mapa_de_risco(riscos_ativos):
    """Contagem de riscos ativos por célula probabilidade x impacto (eixos 1-5)."""
    contagem = {}
    for prob, imp in riscos_ativos.values_list("probabilidade", "impacto"):
        p = _to_valor(prob, PROBABILIDADE_ESCALA)
        i = _to_valor(imp, IMPACTO_ESCALA)
        if p and i:
            contagem[(p, i)] = contagem.get((p, i), 0) + 1
    return [
        {"probabilidade": p, "impacto": i, "total": total}
        for (p, i), total in sorted(contagem.items())
    ]


@login_required_session
@require_GET
def dashboard_summary(request):
    riscos = Risco.objects.all()
    riscos_ativos = riscos.filter(ativo=True)
    tratamentos = Tratamento.objects.filter(ativo=True)
    recent_cutoff = timezone.now() - timedelta(days=30)

    riscos_alto_impacto = sum(
        1
        for risco in riscos_ativos
        if _normalize(risco.impacto) in {"alto", "grande", "catastrófico", "catastrofico"}
    )

    data = {
        "totalRiscos": riscos_ativos.count(),
        "riscosAltoImpacto": riscos_alto_impacto,
        "riscosComTratamento": tratamentos.values("risco_id").distinct().count(),
        "novosRiscos": riscos_ativos.filter(data_criacao__gte=recent_cutoff).count(),
        "distribuicaoPorNivel": _distribuicao_por_nivel(riscos_ativos),
        "mapaDeRisco": _mapa_de_risco(riscos_ativos),
    }

    return JsonResponse(data)
