from django import forms
from .models import Subunidade


class SubunidadeForm(forms.ModelForm):
    class Meta:
        model = Subunidade
        fields = ["nome", "descricao", "sigla"]
        labels = {
            "nome": "Nome da Subunidade",
            "descricao": "Descrição",
            "sigla": "Sigla",
        }
        widgets = {"descricao": forms.Textarea}

    sigla = forms.CharField(label="Sigla", max_length=100)
