from django.http import JsonResponse
from django.views.decorators.http import require_GET

from core.auth import login_required_session

from .models import Subunidade


def _unidade_to_dict(unidade):
    return {
        "id": unidade.id,
        "cod": unidade.cod_estruturado,
        "nome": unidade.nome,
        "centroNome": unidade.centro_nome,
        "centroSigla": unidade.centro_sigla,
        "tipo": unidade.tipo,
        "situacao": unidade.situacao,
    }


@login_required_session
@require_GET
def subunidades_centros(request):
    centros = (
        Subunidade.objects.filter(ativo=True)
        .values("centro_sigla", "centro_nome")
        .distinct()
        .order_by("centro_nome")
    )
    # Dedupe por sigla (nomes divergentes na fonte): mantem o primeiro nome encontrado.
    vistos = {}
    for centro in centros:
        sigla = centro["centro_sigla"]
        if sigla and sigla not in vistos:
            vistos[sigla] = {"sigla": sigla, "nome": centro["centro_nome"]}

    return JsonResponse({"results": list(vistos.values())})


@login_required_session
@require_GET
def subunidades_collection(request):
    unidades = Subunidade.objects.filter(ativo=True)

    centro = request.GET.get("centro", "").strip()
    if centro:
        unidades = unidades.filter(centro_sigla__iexact=centro)

    tipo = request.GET.get("tipo", "").strip()
    if tipo:
        unidades = unidades.filter(tipo__iexact=tipo)

    busca = request.GET.get("busca", "").strip()
    if busca:
        unidades = unidades.filter(nome__icontains=busca)

    return JsonResponse({"results": [_unidade_to_dict(u) for u in unidades.order_by("nome")]})
