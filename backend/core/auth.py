"""Autenticação baseada em sessão para a API (ver usuario/api_views.auth_*)."""

from functools import wraps

from django.http import JsonResponse


def login_required_session(view):
    """Bloqueia a view com 401 quando não há ``usuario_id`` na sessão."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("usuario_id"):
            return JsonResponse({"errors": {"auth": "Nao autenticado."}}, status=401)
        return view(request, *args, **kwargs)

    return wrapper
