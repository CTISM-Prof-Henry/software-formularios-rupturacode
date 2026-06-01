from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from riscos.models import Risco
from usuario.models import Usuario

from .forms import TratamentoForm
from .models import Tratamento


def _tratamento_to_dict(tratamento):
    return {
        "id": tratamento.id,
        "resposta": tratamento.resposta,
        "acao": tratamento.acao,
        "data_inicio": tratamento.data_inicio,
        "data_fim": tratamento.data_fim,
        "situacao": tratamento.situacao,
        "risco_id": tratamento.risco_id,
        "usuario_responsavel_id": tratamento.usuario_responsavel_id,
    }


def criar_tratamento(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST para criar um tratamento."}, status=405)

    usuario = Usuario.objects.first()
    risco = Risco.objects.first()

    if not usuario or not risco:
        return JsonResponse(
            {"detail": "Cadastre pelo menos um usuario e um risco antes do tratamento."},
            status=400,
        )

    form = TratamentoForm(request.POST)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    tratamento = form.save(commit=False)
    tratamento.usuario_responsavel = usuario
    tratamento.risco = risco
    tratamento.save()

    return JsonResponse(_tratamento_to_dict(tratamento), status=201)


def listar_tratamentos(request):
    tratamentos = Tratamento.objects.select_related("risco", "usuario_responsavel").all()
    return JsonResponse({"results": [_tratamento_to_dict(item) for item in tratamentos]})


def editar_tratamento(request, pk):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST para editar um tratamento."}, status=405)

    tratamento = get_object_or_404(Tratamento, pk=pk)
    form = TratamentoForm(request.POST, instance=tratamento)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    tratamento = form.save()
    return JsonResponse(_tratamento_to_dict(tratamento))


def desativar_tratamento(request, pk):
    tratamento = get_object_or_404(Tratamento, pk=pk)
    tratamento.situacao = "Desativado"
    tratamento.save(update_fields=["situacao", "data_atualizacao"])
    return JsonResponse(_tratamento_to_dict(tratamento))


def ativar_tratamento(request, pk):
    tratamento = get_object_or_404(Tratamento, pk=pk)
    tratamento.situacao = "Ativo"
    tratamento.save(update_fields=["situacao", "data_atualizacao"])
    return JsonResponse(_tratamento_to_dict(tratamento))


def detalhes_tratamento(request, pk):
    tratamento = get_object_or_404(Tratamento, pk=pk)
    return JsonResponse(_tratamento_to_dict(tratamento))
