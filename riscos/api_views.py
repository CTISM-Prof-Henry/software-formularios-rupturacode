import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Risco


def _risk_to_dict(risco):
    return {
        "id": risco.id,
        "nome": risco.nome,
        "descricao": risco.descricao,
        "tipo": risco.tipo,
        "departamento": risco.departamento,
        "impacto": risco.impacto,
        "probabilidade": risco.probabilidade,
        "nivelDeRisco": risco.nivel_de_risco,
        "eficaciaDosControles": risco.eficacia_dos_controles,
        "nivelResidual": risco.nivel_residual,
        "ativo": risco.ativo,
        "dataCriacao": risco.data_criacao.isoformat(),
        "dataAtualizacao": risco.data_atualizacao.isoformat(),
    }


def _payload_to_risk_fields(payload):
    return {
        "nome": payload.get("nome") or payload.get("identifiedRisk", "")[:100],
        "descricao": payload.get("descricao") or payload.get("identifiedRisk", ""),
        "tipo": payload.get("tipo") or payload.get("riskType", ""),
        "departamento": payload.get("departamento") or payload.get("department", ""),
        "impacto": payload.get("impacto") or payload.get("impact", ""),
        "probabilidade": payload.get("probabilidade") or payload.get("probability", ""),
        "nivel_de_risco": payload.get("nivel_de_risco") or payload.get("riskLevel", ""),
        "eficacia_dos_controles": payload.get("eficacia_dos_controles")
        or payload.get("internalControls", ""),
        "nivel_residual": payload.get("nivel_residual") or payload.get("residualLevel", ""),
    }


def _validate(fields):
    required_fields = [
        "nome",
        "descricao",
        "tipo",
        "departamento",
        "impacto",
        "probabilidade",
        "nivel_de_risco",
        "eficacia_dos_controles",
        "nivel_residual",
    ]

    return {
        field: "Campo obrigatorio."
        for field in required_fields
        if not str(fields.get(field, "")).strip()
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def riscos_collection(request):
    if request.method == "GET":
        riscos = Risco.objects.filter(ativo=True).order_by("-data_criacao")
        return JsonResponse({"results": [_risk_to_dict(risco) for risco in riscos]})

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"errors": {"body": "JSON invalido."}}, status=400)

    fields = _payload_to_risk_fields(payload)
    errors = _validate(fields)

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    risco = Risco.objects.create(**fields)
    return JsonResponse(_risk_to_dict(risco), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def riscos_detail(request, risco_id):
    try:
        risco = Risco.objects.get(pk=risco_id)
    except Risco.DoesNotExist:
        return JsonResponse({"errors": {"id": "Risco nao encontrado."}}, status=404)

    if request.method == "GET":
        return JsonResponse(_risk_to_dict(risco))

    if request.method == "DELETE":
        risco.ativo = False
        risco.save(update_fields=["ativo", "data_atualizacao"])
        return JsonResponse({"ok": True})

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"errors": {"body": "JSON invalido."}}, status=400)

    fields = _payload_to_risk_fields(payload)
    errors = _validate(fields)

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    for key, value in fields.items():
        setattr(risco, key, value)
    risco.save()
    return JsonResponse(_risk_to_dict(risco))
