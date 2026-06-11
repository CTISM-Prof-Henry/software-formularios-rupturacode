import json
import random

from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .models import Usuario

RESET_CODE_TTL = 600  # 10 minutos
RESET_CACHE_PREFIX = "password_reset_code:"


def _user_to_dict(usuario):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "telefone": usuario.telefone,
        "cpf": usuario.cpf,
        "matricula": usuario.matricula,
        "centro": usuario.centro,
        "departamento": usuario.departamento,
        "cargo": usuario.cargo,
        "dataNascimento": usuario.data_nascimento.isoformat() if usuario.data_nascimento else None,
        "isAdmin": usuario.is_admin,
        "ativo": usuario.ativo,
        "dataCriacao": usuario.data_criacao.isoformat(),
        "dataAtualizacao": usuario.data_atualizacao.isoformat(),
    }


def _payload_to_user_fields(payload):
    return {
        "nome": payload.get("nome") or payload.get("name", ""),
        "email": (payload.get("email") or "").strip().lower(),
        "telefone": payload.get("telefone") or payload.get("phone", ""),
        "cpf": payload.get("cpf", ""),
        "matricula": payload.get("matricula") or payload.get("registration", ""),
        "centro": payload.get("centro") or payload.get("center", ""),
        "departamento": payload.get("departamento") or payload.get("department", ""),
        "cargo": payload.get("cargo") or payload.get("role", ""),
        "data_nascimento": payload.get("data_nascimento") or payload.get("birthDate") or None,
    }


def _validate_user(fields):
    required_fields = ["nome", "email", "matricula", "departamento", "cargo"]
    return {
        field: "Campo obrigatorio."
        for field in required_fields
        if not str(fields.get(field, "")).strip()
    }


def _parse_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}"), None
    except json.JSONDecodeError:
        return None, JsonResponse({"errors": {"body": "JSON invalido."}}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def usuarios_collection(request):
    if request.method == "GET":
        usuarios = Usuario.objects.filter(ativo=True).order_by("nome")

        busca = request.GET.get("busca", "").strip()
        if busca:
            usuarios = usuarios.filter(nome__icontains=busca)
        for param, field in (("cargo", "cargo"), ("centro", "centro"), ("departamento", "departamento")):
            value = request.GET.get(param, "").strip()
            if value:
                usuarios = usuarios.filter(**{f"{field}__iexact": value})

        return JsonResponse({"results": [_user_to_dict(usuario) for usuario in usuarios]})

    payload, error = _parse_body(request)
    if error:
        return error

    fields = _payload_to_user_fields(payload)
    errors = _validate_user(fields)

    senha = payload.get("senha") or payload.get("password", "")
    if not str(senha).strip():
        errors["senha"] = "Campo obrigatorio."

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    if Usuario.objects.filter(email=fields["email"]).exists():
        return JsonResponse({"errors": {"email": "E-mail ja cadastrado."}}, status=400)
    if Usuario.objects.filter(matricula=fields["matricula"]).exists():
        return JsonResponse({"errors": {"matricula": "Matricula ja cadastrada."}}, status=400)

    usuario = Usuario.objects.create(
        **fields,
        senha=make_password(senha),
        is_admin=bool(payload.get("isAdmin") or payload.get("is_admin")),
    )
    return JsonResponse(_user_to_dict(usuario), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def usuarios_detail(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return JsonResponse({"errors": {"id": "Usuario nao encontrado."}}, status=404)

    if request.method == "GET":
        return JsonResponse(_user_to_dict(usuario))

    if request.method == "DELETE":
        usuario.ativo = False
        usuario.save(update_fields=["ativo", "data_atualizacao"])
        return JsonResponse({"ok": True})

    payload, error = _parse_body(request)
    if error:
        return error

    fields = _payload_to_user_fields(payload)
    errors = _validate_user(fields)
    if errors:
        return JsonResponse({"errors": errors}, status=400)

    for key, value in fields.items():
        setattr(usuario, key, value)

    senha = payload.get("senha") or payload.get("password")
    if senha and str(senha).strip():
        usuario.senha = make_password(senha)
    if "ativo" in payload:
        usuario.ativo = bool(payload["ativo"])

    usuario.save()
    return JsonResponse(_user_to_dict(usuario))


# ---------------------------------------------------------------------------
# Autenticacao (baseada em sessao)
# ---------------------------------------------------------------------------


@csrf_exempt
@require_POST
def auth_login(request):
    payload, error = _parse_body(request)
    if error:
        return error

    email = (payload.get("email") or "").strip().lower()
    senha = payload.get("senha") or payload.get("password", "")

    usuario = Usuario.objects.filter(email=email, ativo=True).first()
    if not usuario or not check_password(senha, usuario.senha):
        return JsonResponse({"errors": {"credenciais": "E-mail ou senha invalidos."}}, status=401)

    request.session["usuario_id"] = usuario.id
    return JsonResponse(_user_to_dict(usuario))


@csrf_exempt
@require_POST
def auth_logout(request):
    request.session.flush()
    return JsonResponse({"ok": True})


@require_GET
def auth_me(request):
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.filter(pk=usuario_id, ativo=True).first() if usuario_id else None
    if not usuario:
        return JsonResponse({"errors": {"auth": "Nao autenticado."}}, status=401)
    return JsonResponse(_user_to_dict(usuario))


@csrf_exempt
@require_POST
def password_reset_request(request):
    payload, error = _parse_body(request)
    if error:
        return error

    email = (payload.get("email") or "").strip().lower()
    usuario = Usuario.objects.filter(email=email, ativo=True).first()

    # Resposta generica (nao revela se o e-mail existe), mas so envia se existir.
    if usuario:
        codigo = f"{random.randint(0, 999999):06d}"
        cache.set(f"{RESET_CACHE_PREFIX}{email}", codigo, RESET_CODE_TTL)
        send_mail(
            subject="Atlas - Codigo de recuperacao de senha",
            message=f"Seu codigo de recuperacao e: {codigo} (valido por 10 minutos).",
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )

    return JsonResponse({"ok": True})


def _check_reset_code(email, codigo):
    stored = cache.get(f"{RESET_CACHE_PREFIX}{email}")
    return bool(stored) and stored == str(codigo).strip()


@csrf_exempt
@require_POST
def password_reset_verify(request):
    payload, error = _parse_body(request)
    if error:
        return error

    email = (payload.get("email") or "").strip().lower()
    codigo = payload.get("codigo") or payload.get("code", "")

    if not _check_reset_code(email, codigo):
        return JsonResponse({"errors": {"codigo": "Codigo invalido ou expirado."}}, status=400)
    return JsonResponse({"ok": True})


@csrf_exempt
@require_POST
def password_reset_confirm(request):
    payload, error = _parse_body(request)
    if error:
        return error

    email = (payload.get("email") or "").strip().lower()
    codigo = payload.get("codigo") or payload.get("code", "")
    senha = payload.get("senha") or payload.get("password", "")

    if not _check_reset_code(email, codigo):
        return JsonResponse({"errors": {"codigo": "Codigo invalido ou expirado."}}, status=400)
    if not str(senha).strip():
        return JsonResponse({"errors": {"senha": "Informe a nova senha."}}, status=400)

    usuario = Usuario.objects.filter(email=email, ativo=True).first()
    if not usuario:
        return JsonResponse({"errors": {"email": "Usuario nao encontrado."}}, status=404)

    usuario.senha = make_password(senha)
    usuario.save(update_fields=["senha", "data_atualizacao"])
    cache.delete(f"{RESET_CACHE_PREFIX}{email}")
    return JsonResponse({"ok": True})
