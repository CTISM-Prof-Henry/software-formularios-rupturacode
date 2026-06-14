import json

from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.auth import login_required_session
from riscos.models import Risco
from usuario.models import Usuario

from .models import Tratamento

# Aceita tanto o codigo quanto o rotulo exibido (compatibilidade com o front).
_RESPOSTA_POR_ROTULO = {label: code for code, label in Tratamento.RESPOSTAS}
_SITUACAO_POR_ROTULO = {label: code for code, label in Tratamento.SITUACAO}
_RESPOSTA_CODES = {code for code, _ in Tratamento.RESPOSTAS}
_SITUACAO_CODES = {code for code, _ in Tratamento.SITUACAO}


def _normaliza(valor, por_rotulo, codigos):
    texto = str(valor or "").strip()
    if texto in codigos:
        return texto
    return por_rotulo.get(texto, texto)


def _parse_data(*valores):
    for valor in valores:
        if valor:
            return parse_date(valor) if isinstance(valor, str) else valor
    return None


def _esta_atrasado(tratamento):
    return bool(
        tratamento.data_fim
        and tratamento.situacao != "concluido"
        and tratamento.data_fim < timezone.localdate()
    )


def _treatment_to_dict(tratamento):
    return {
        "id": tratamento.id,
        "riscoId": tratamento.risco_id,
        "riscoNome": tratamento.risco.nome if tratamento.risco_id else None,
        "resposta": tratamento.resposta,
        "acao": tratamento.acao,
        "dataInicio": tratamento.data_inicio.isoformat() if tratamento.data_inicio else None,
        "dataFim": tratamento.data_fim.isoformat() if tratamento.data_fim else None,
        "situacao": tratamento.situacao,
        "atrasado": _esta_atrasado(tratamento),
        "ativo": tratamento.ativo,
        "usuarioResponsavelId": tratamento.usuario_responsavel_id,
        "usuarioResponsavelNome": (
            tratamento.usuario_responsavel.nome if tratamento.usuario_responsavel else None
        ),
        "dataCriacao": tratamento.data_criacao.isoformat(),
        "dataAtualizacao": tratamento.data_atualizacao.isoformat(),
    }


def _payload_to_treatment_fields(payload):
    return {
        "resposta": _normaliza(
            payload.get("resposta") or payload.get("riskResponse"),
            _RESPOSTA_POR_ROTULO,
            _RESPOSTA_CODES,
        ),
        "acao": payload.get("acao") or payload.get("actionPlan", ""),
        "data_inicio": _parse_data(
            payload.get("data_inicio"), payload.get("dataInicio"), payload.get("startDate")
        ),
        "data_fim": _parse_data(
            payload.get("data_fim"), payload.get("dataFim"), payload.get("dueDate")
        ),
        "situacao": _normaliza(
            payload.get("situacao") or payload.get("status"),
            _SITUACAO_POR_ROTULO,
            _SITUACAO_CODES,
        )
        or "nao_iniciado",
    }


def _resolve_fk(payload, *keys, model):
    for key in keys:
        if key in payload and payload[key] not in (None, ""):
            try:
                return model.objects.get(pk=payload[key]), None
            except (model.DoesNotExist, ValueError, TypeError):
                return None, f"{model.__name__} nao encontrado."
    return None, None


def _validate(fields):
    errors = {}
    if not fields.get("resposta") or fields["resposta"] not in _RESPOSTA_CODES:
        errors["resposta"] = "Resposta invalida."
    if fields.get("situacao") not in _SITUACAO_CODES:
        errors["situacao"] = "Situacao invalida."
    # Acao e prazos sao obrigatorios exceto quando a resposta e "Aceitar".
    if fields.get("resposta") != "aceitar":
        if not str(fields.get("acao", "")).strip():
            errors["acao"] = "Campo obrigatorio."
        if not fields.get("data_fim"):
            errors["dataFim"] = "Campo obrigatorio."
    return errors


@login_required_session
@csrf_exempt
@require_http_methods(["GET", "POST"])
def tratamentos_collection(request):
    if request.method == "GET":
        tratamentos = Tratamento.objects.filter(ativo=True).select_related(
            "usuario_responsavel", "risco"
        )
        risco_id = request.GET.get("risco", "").strip()
        if risco_id:
            tratamentos = tratamentos.filter(risco_id=risco_id)
        responsavel_id = request.GET.get("responsavel", "").strip()
        if responsavel_id:
            tratamentos = tratamentos.filter(usuario_responsavel_id=responsavel_id)
        tratamentos = tratamentos.order_by("-data_criacao")
        return JsonResponse(
            {"results": [_treatment_to_dict(t) for t in tratamentos]}
        )

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"errors": {"body": "JSON invalido."}}, status=400)

    risco, risco_error = _resolve_fk(payload, "riscoId", "risco", model=Risco)
    if risco_error or risco is None:
        return JsonResponse(
            {"errors": {"riscoId": risco_error or "Campo obrigatorio."}}, status=400
        )

    responsavel, resp_error = _resolve_fk(
        payload, "usuarioResponsavelId", "usuario_responsavel", model=Usuario
    )
    if resp_error:
        return JsonResponse({"errors": {"usuarioResponsavelId": resp_error}}, status=400)

    fields = _payload_to_treatment_fields(payload)
    errors = _validate(fields)
    if errors:
        return JsonResponse({"errors": errors}, status=400)

    tratamento = Tratamento.objects.create(
        risco=risco, usuario_responsavel=responsavel, **fields
    )
    return JsonResponse(_treatment_to_dict(tratamento), status=201)


@login_required_session
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def tratamentos_detail(request, tratamento_id):
    try:
        tratamento = Tratamento.objects.select_related(
            "usuario_responsavel", "risco"
        ).get(pk=tratamento_id)
    except Tratamento.DoesNotExist:
        return JsonResponse({"errors": {"id": "Tratamento nao encontrado."}}, status=404)

    if request.method == "GET":
        return JsonResponse(_treatment_to_dict(tratamento))

    if request.method == "DELETE":
        tratamento.ativo = False
        tratamento.save(update_fields=["ativo", "data_atualizacao"])
        return JsonResponse({"ok": True})

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"errors": {"body": "JSON invalido."}}, status=400)

    fields = _payload_to_treatment_fields(payload)
    errors = _validate(fields)
    if errors:
        return JsonResponse({"errors": errors}, status=400)

    responsavel, resp_error = _resolve_fk(
        payload, "usuarioResponsavelId", "usuario_responsavel", model=Usuario
    )
    if resp_error:
        return JsonResponse({"errors": {"usuarioResponsavelId": resp_error}}, status=400)
    if responsavel is not None or any(
        k in payload for k in ("usuarioResponsavelId", "usuario_responsavel")
    ):
        tratamento.usuario_responsavel = responsavel

    for key, value in fields.items():
        setattr(tratamento, key, value)
    tratamento.save()
    return JsonResponse(_treatment_to_dict(tratamento))
