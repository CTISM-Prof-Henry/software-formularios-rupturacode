from django.shortcuts import render
from .models import Subunidade
from .forms import SubunidadeForm


# Create your views here.
def criar_subunidade(request):
    if request.method == "POST":
        form = SubunidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "subunidade/sucesso.html")
    else:
        form = SubunidadeForm()

    return render(request, "subunidade/criar_subunidade.html", {"form": form})


def listar_subunidades(request):
    subunidades = Subunidade.objects.all()
    return render(
        request, "subunidade/listar_subunidades.html", {"subunidades": subunidades}
    )


def detalhes_subunidade(request, subunidade_id):
    subunidade = Subunidade.objects.get(id=subunidade_id)
    return render(
        request, "subunidade/detalhes_subunidade.html", {"subunidade": subunidade}
    )


def editar_subunidade(request, subunidade_id):
    subunidade = Subunidade.objects.get(id=subunidade_id)
    if request.method == "POST":
        form = SubunidadeForm(request.POST, instance=subunidade)
        if form.is_valid():
            form.save()
            return render(request, "subunidade/sucesso.html")
    else:
        form = SubunidadeForm(instance=subunidade)

    return render(request, "subunidade/editar_subunidade.html", {"form": form})


def desativar_subunidade(request, subunidade_id):
    subunidade = Subunidade.objects.get(id=subunidade_id)
    subunidade.ativo = False
    subunidade.save()
    return render(request, "subunidade/sucesso.html")


def ativar_subunidade(request, subunidade_id):
    subunidade = Subunidade.objects.get(id=subunidade_id)
    subunidade.ativo = True
    subunidade.save()
    return render(request, "subunidade/sucesso.html")
