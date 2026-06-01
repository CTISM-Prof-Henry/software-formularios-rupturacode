from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from riscos.models import Risco
from tratamentos.models import Tratamento


def _normalize(value):
    return str(value or "").strip().lower()


@require_GET
def dashboard_summary(request):
    riscos = Risco.objects.all()
    riscos_ativos = riscos.filter(ativo=True)
    tratamentos = Tratamento.objects.all()
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
    }

    return JsonResponse(data)
