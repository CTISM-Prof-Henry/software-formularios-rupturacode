from django.contrib import admin
from django.urls import path, re_path

from core.api_views import dashboard_summary
from core.views import frontend_index
from riscos.api_views import riscos_collection, riscos_detail
from subunidade.api_views import subunidades_centros, subunidades_collection
from tratamentos.api_views import tratamentos_collection, tratamentos_detail
from usuario.api_views import (
    auth_login,
    auth_logout,
    auth_me,
    cargos_list,
    password_reset_confirm,
    password_reset_request,
    password_reset_verify,
    usuarios_collection,
    usuarios_detail,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/dashboard/", dashboard_summary, name="api_dashboard_summary"),
    path("api/riscos/", riscos_collection, name="api_riscos_collection"),
    path("api/riscos/<int:risco_id>/", riscos_detail, name="api_riscos_detail"),
    path("api/tratamentos/", tratamentos_collection, name="api_tratamentos_collection"),
    path("api/tratamentos/<int:tratamento_id>/", tratamentos_detail, name="api_tratamentos_detail"),
    path("api/usuarios/", usuarios_collection, name="api_usuarios_collection"),
    path("api/usuarios/<int:usuario_id>/", usuarios_detail, name="api_usuarios_detail"),
    path("api/cargos/", cargos_list, name="api_cargos_list"),
    path("api/subunidades/", subunidades_collection, name="api_subunidades_collection"),
    path("api/subunidades/centros/", subunidades_centros, name="api_subunidades_centros"),
    path("api/auth/login/", auth_login, name="api_auth_login"),
    path("api/auth/logout/", auth_logout, name="api_auth_logout"),
    path("api/auth/me/", auth_me, name="api_auth_me"),
    path("api/auth/password-reset/request/", password_reset_request, name="api_auth_reset_request"),
    path("api/auth/password-reset/verify/", password_reset_verify, name="api_auth_reset_verify"),
    path("api/auth/password-reset/confirm/", password_reset_confirm, name="api_auth_reset_confirm"),
    path("", frontend_index, name="frontend_index"),
    re_path(r"^(?!admin/|api/).*$", frontend_index),
]
