from django import forms
from .models import Risco


class RiscoForm(forms.ModelForm):
    class Meta:
        model = Risco
        fields = [
            "nome",
            "descricao",
            "tipo",
            "departamento",
            "impacto",
            "probabilidade",
            "nivel_de_risco",
            "eficacia_dos_controles",
            "nivel_residual",
        ]
