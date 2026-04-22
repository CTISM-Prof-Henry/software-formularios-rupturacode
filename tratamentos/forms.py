from django import forms
from .models import Tratamento

class TratamentoForm(forms.ModelForm):
    class Meta:
        model = Tratamento
        fields = ['resposta', 'acao', 'data_inicio', 'data_fim', 'situacao']