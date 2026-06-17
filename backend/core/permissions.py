"""Cargos canonicos e permissoes por nivel.

Fonte da verdade dos cargos (choices do model ``Usuario.cargo``) e do mapa
cargo -> nivel de acesso. O nivel efetivo de um usuario e ``admin`` quando
``is_admin`` (override manual) ou o nivel mapeado do seu cargo.

Niveis (do menor para o maior):
- ``leitor``: so leitura (GET).
- ``editor``: leitor + escrita de riscos e tratamentos.
- ``admin``: editor + gestao de usuarios.
"""

from functools import wraps

from django.http import JsonResponse

# (valor, rotulo) -- valor e o que vai no banco / API.
CARGO_CHOICES = [
    ("Diretor", "Diretor"),
    ("Coordenador", "Coordenador"),
    ("Analista", "Analista"),
    ("Técnico", "Técnico"),
    ("Professor", "Professor"),
    ("Servidor", "Servidor"),
]

CARGO_NIVEL = {
    "Diretor": "admin",
    "Coordenador": "admin",
    "Analista": "editor",
    "Técnico": "editor",
    "Professor": "leitor",
    "Servidor": "leitor",
}

NIVEL_ORDER = {"leitor": 0, "editor": 1, "admin": 2}

CARGOS_VALIDOS = {valor for valor, _ in CARGO_CHOICES}


def nivel_de(usuario):
    """Nivel efetivo do usuario (``is_admin`` sobrepoe o cargo)."""
    if getattr(usuario, "is_admin", False):
        return "admin"
    return CARGO_NIVEL.get(usuario.cargo, "leitor")


def tem_nivel(usuario, min_nivel):
    return NIVEL_ORDER.get(nivel_de(usuario), 0) >= NIVEL_ORDER[min_nivel]


def _usuario_da_sessao(request):
    from usuario.models import Usuario  # import tardio evita ciclo

    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return None
    return Usuario.objects.filter(pk=usuario_id, ativo=True).first()


def exige_nivel(request, min_nivel):
    """Checa o nivel inline (para views que multiplexam por metodo).

    Retorna ``JsonResponse`` de erro (401/403) quando barrado, ou ``None`` quando liberado.
    """
    usuario = _usuario_da_sessao(request)
    if usuario is None:
        return JsonResponse({"errors": {"auth": "Nao autenticado."}}, status=401)
    if not tem_nivel(usuario, min_nivel):
        return JsonResponse(
            {"errors": {"permissao": "Permissao insuficiente para esta acao."}}, status=403
        )
    return None


def nivel_required(min_nivel):
    """Decorator: bloqueia a view inteira a quem nao tem ``min_nivel``."""

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            barrado = exige_nivel(request, min_nivel)
            if barrado is not None:
                return barrado
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
