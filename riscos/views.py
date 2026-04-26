from django.shortcuts import get_object_or_404, render
from .models import Risco
from .forms import RiscoForm


# Create your views here.
def criar_risco(request):
    if request.method == "POST":
        form = RiscoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "sucesso.html")
    else:
        form = RiscoForm()

    return render(request, "criar_risco.html", {"form": form})


def listar_riscos(request):
    riscos = Risco.objects.all()
    return render(request, "listar_risco.html", {"riscos": riscos})


def desativar_risco(request, risco_id):
    risco = get_object_or_404(Risco, id=risco_id)
    risco.ativo = False
    risco.save()
    return render(request, "desativar_sucesso.html")


def ativar_risco(request, risco_id):
    risco = get_object_or_404(Risco, id=risco_id)
    risco.ativo = True
    risco.save()
    return render(request, "ativar_sucesso.html")


def editar_risco(request, risco_id):
    risco = get_object_or_404(Risco, id=risco_id)
    if request.method == "POST":
        form = RiscoForm(request.POST, instance=risco)
        if form.is_valid():
            form.save()
            return render(request, "sucesso.html")
    else:
        form = RiscoForm(instance=risco)

    return render(request, "editar_risco.html", {"form": form})


def detalhes_risco(request, risco_id):
    risco = get_object_or_404(Risco, id=risco_id)
    return render(request, "detalhes_risco.html", {"risco": risco})
