from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .forms import RiscoForm
from .models import Risco


def criar_risco(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST para criar um risco."}, status=405)

    form = RiscoForm(request.POST)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    risco = form.save()
    return JsonResponse({"id": risco.id}, status=201)


def listar_riscos(request):
    riscos = Risco.objects.filter(ativo=True).values(
        "id",
        "nome",
        "descricao",
        "tipo",
        "departamento",
        "impacto",
        "probabilidade",
        "nivel_de_risco",
        "eficacia_dos_controles",
        "nivel_residual",
        "data_criacao",
        "data_atualizacao",
    )
    return JsonResponse({"results": list(riscos)})


def desativar_risco(request, risco_id):
    risco = get_object_or_404(Risco, id=risco_id)
    risco.ativo = False
    risco.save(update_fields=["ativo", "data_atualizacao"])
    return JsonResponse({"id": risco.id, "ativo": risco.ativo})


def editar_risco(request, risco_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST para editar um risco."}, status=405)

    risco = get_object_or_404(Risco, id=risco_id)
    form = RiscoForm(request.POST, instance=risco)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    risco = form.save()
    return JsonResponse({"id": risco.id})


def detalhes_risco(request, risco_id):
    risco = get_object_or_404(Risco, id=risco_id)
    return JsonResponse(
        {
            "id": risco.id,
            "nome": risco.nome,
            "descricao": risco.descricao,
            "tipo": risco.tipo,
            "departamento": risco.departamento,
            "impacto": risco.impacto,
            "probabilidade": risco.probabilidade,
            "nivel_de_risco": risco.nivel_de_risco,
            "eficacia_dos_controles": risco.eficacia_dos_controles,
            "nivel_residual": risco.nivel_residual,
            "ativo": risco.ativo,
            "data_criacao": risco.data_criacao,
            "data_atualizacao": risco.data_atualizacao,
        }
    )
