from django.urls import path
from .views import (
    criar_subunidade,
    listar_subunidades,
    detalhes_subunidade,
    editar_subunidade,
    desativar_subunidade,
    ativar_subunidade,
)

urlpatterns = [
    path("subunidade/criar/", criar_subunidade, name="criar_subunidade"),
    path("subunidade/listar/", listar_subunidades, name="listar_subunidades"),
    path(
        "subunidade/<int:subunidade_id>/",
        detalhes_subunidade,
        name="detalhes_subunidade",
    ),
    path(
        "subunidade/<int:subunidade_id>/editar/",
        editar_subunidade,
        name="editar_subunidade",
    ),
    path(
        "subunidade/<int:subunidade_id>/desativar/",
        desativar_subunidade,
        name="desativar_subunidade",
    ),
    path(
        "subunidade/<int:subunidade_id>/ativar/",
        ativar_subunidade,
        name="ativar_subunidade",
    ),
]
