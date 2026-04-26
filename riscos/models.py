import time

from django.db import models


# Create your models here.
class Risco(models.Model):
    TIPOS_DE_RISCO = [
        ("riscos_operacionais", "Riscos Operacionais"),
        ("riscos_de_imagem_reputacao", "Riscos de Imagem/Reputação"),
        ("riscos_legais", "Riscos Legais"),
        ("riscos_financeiros_orcamentarios", "Riscos Financeiros/Orçamentários"),
    ]

    DEPARTAMENTO = [
        ("departamento_1", "Departamento 1"),
        ("departamento_2", "Departamento 2"),
        ("departamento_3", "Departamento 3"),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPOS_DE_RISCO)
    departamento = models.CharField(max_length=100)
    impacto = models.CharField(max_length=50)
    probabilidade = models.CharField(max_length=50)
    nivel_de_risco = models.CharField(max_length=50)
    eficacia_dos_controles = models.CharField(max_length=50)
    nivel_residual = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
