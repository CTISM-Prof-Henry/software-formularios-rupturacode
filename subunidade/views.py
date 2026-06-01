from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .forms import SubunidadeForm
from .models import Subunidade


def _subunidade_to_dict(subunidade):
    return {
        "id": subunidade.id,
        "nome": subunidade.nome,
        "descricao": subunidade.descricao,
        "sigla": subunidade.sigla,
        "ativo": subunidade.ativo,
    }


def criar_subunidade(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST para criar uma subunidade."}, status=405)

    form = SubunidadeForm(request.POST)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    subunidade = form.save()
    return JsonResponse(_subunidade_to_dict(subunidade), status=201)


def listar_subunidades(request):
    subunidades = Subunidade.objects.filter(ativo=True)
    return JsonResponse({"results": [_subunidade_to_dict(item) for item in subunidades]})


def detalhes_subunidade(request, subunidade_id):
    subunidade = get_object_or_404(Subunidade, id=subunidade_id)
    return JsonResponse(_subunidade_to_dict(subunidade))


def editar_subunidade(request, subunidade_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST para editar uma subunidade."}, status=405)

    subunidade = get_object_or_404(Subunidade, id=subunidade_id)
    form = SubunidadeForm(request.POST, instance=subunidade)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    subunidade = form.save()
    return JsonResponse(_subunidade_to_dict(subunidade))


def desativar_subunidade(request, subunidade_id):
    subunidade = get_object_or_404(Subunidade, id=subunidade_id)
    subunidade.ativo = False
    subunidade.save(update_fields=["ativo"])
    return JsonResponse(_subunidade_to_dict(subunidade))
