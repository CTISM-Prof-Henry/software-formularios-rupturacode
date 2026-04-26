from django.urls import path
from .views import (
    criar_tratamento,
    listar_tratamentos,
    ativar_tratamento,
    desativar_tratamento,
    editar_tratamento,
    detalhes_tratamento,
)

urlpatterns = [
    path("tratamento/criar/", criar_tratamento, name="criar_tratamento"),
    path("tratamento/listar/", listar_tratamentos, name="listar_tratamentos"),
    path(
        "tratamento/<int:pk>/editar/",
        editar_tratamento,
        name="editar_tratamento",
    ),
    path(
        "tratamento/<int:pk>/desativar/",
        desativar_tratamento,
        name="desativar_tratamento",
    ),
    path(
        "tratamento/<int:pk>/ativar/",
        ativar_tratamento,
        name="ativar_tratamento",
    ),
    path(
        "tratamento/<int:pk>/",
        detalhes_tratamento,
        name="detalhes_tratamento",
    ),
]
