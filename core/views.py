from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from riscos.models import Risco
from tratamentos.models import Tratamento


def dashboard(request):
    riscos = Risco.objects.all()
    tratamentos = Tratamento.objects.all()

    contexto = {
        "total_riscos": riscos.count(),
        "riscos_alto_impacto": riscos.filter(impacto="Alto").count(),
        "riscos_com_tratamentos": tratamentos.count(),
        "riscos_recentes": riscos.filter(
            data_criacao__gte=timezone.now() - timedelta(days=30)
        ).count(),
    }

    return render(request, "dashboard.html", contexto)
