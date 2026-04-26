from django.urls import path

from .views import (
    ativar_risco,
    criar_risco,
    desativar_risco,
    detalhes_risco,
    editar_risco,
    listar_riscos,
)

urlpatterns = [
    path("risco/criar/", criar_risco, name="criar_risco"),
    path("risco/listar/", listar_riscos, name="listar_riscos"),
    path("risco/<int:risco_id>/", detalhes_risco, name="detalhes_risco"),
    path("risco/<int:risco_id>/editar/", editar_risco, name="editar_risco"),
    path("risco/<int:risco_id>/desativar/", desativar_risco, name="desativar_risco"),
    path("risco/<int:risco_id>/ativar/", ativar_risco, name="ativar_risco"),
]
