from django.shortcuts import render
from .forms import TratamentoForm
from .models import Tratamento


# Create your views here.
def criar_tratamento(request):
    if request.method == "POST":
        form = TratamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "sucesso.html")
    else:
        form = TratamentoForm()

    return render(request, "criar_tratamento.html", {"form": form})


def listar_tratamentos(request):
    tratamentos = Tratamento.objects.all()
    return render(request, "listar_tratamentos.html", {"tratamentos": tratamentos})


def editar_tratamento(request, pk):
    tratamento = Tratamento.objects.get(pk=pk)
    if request.method == "POST":
        form = TratamentoForm(request.POST, instance=tratamento)
        if form.is_valid():
            form.save()
            return render(request, "sucesso.html")
    else:
        form = TratamentoForm(instance=tratamento)

    return render(request, "editar_tratamento.html", {"form": form})


def desativar_tratamento(request, pk):
    tratamento = Tratamento.objects.get(pk=pk)
    tratamento.situacao = "Desativado"
    tratamento.save()
    return render(request, "sucesso.html")


def ativar_tratamento(request, pk):
    tratamento = Tratamento.objects.get(pk=pk)
    tratamento.situacao = "Ativo"
    tratamento.save()
    return render(request, "sucesso.html")


def detalhes_tratamento(request, pk):
    tratamento = Tratamento.objects.get(pk=pk)
    return render(request, "detalhes_tratamento.html", {"tratamento": tratamento})
