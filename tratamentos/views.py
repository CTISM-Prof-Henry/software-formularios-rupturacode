from django.shortcuts import get_object_or_404, render, redirect
from .forms import TratamentoForm
from .models import Tratamento
from usuario.models import Usuario
from riscos.models import Risco



def criar_tratamento(request):
    if request.method == "POST":
        form = TratamentoForm(request.POST)
        if form.is_valid():
            tratamento = form.save(commit=False)

            tratamento.usuario_responsavel = Usuario.objects.first()
            tratamento.risco = Risco.objects.first()

            tratamento.save()

            return redirect("listar_tratamentos")

    else:
        form = TratamentoForm()

    return render(request, "criar_tratamento.html", {"form": form})


def listar_tratamentos(request):
    tratamentos = Tratamento.objects.all()
    return render(request, "listar_tratamentos.html", {"tratamentos": tratamentos})


def editar_tratamento(request, pk):
    tratamento = get_object_or_404(Tratamento, pk=pk)
    if request.method == "POST":
        form = TratamentoForm(request.POST, instance=tratamento)
        if form.is_valid():
            form.save()
            return render(request, "sucesso_tratamento.html")
    else:
        form = TratamentoForm(instance=tratamento)

    return render(request, "editar_tratamento.html", {"form": form})


def desativar_tratamento(request, pk):
    tratamento = get_object_or_404(Tratamento, pk=pk)
    tratamento.situacao = "Desativado"
    tratamento.save()
    return render(request, "sucesso_tratamento.html")


def ativar_tratamento(request, pk):
    tratamento = get_object_or_404(Tratamento, pk=pk)
    tratamento.situacao = "Ativo"
    tratamento.save()
    return render(request, "sucesso_tratamento.html")


def detalhes_tratamento(request, pk):
    tratamento = get_object_or_404(Tratamento, pk=pk)
    return render(request, "detalhes_tratamento.html", {"tratamento": tratamento})


