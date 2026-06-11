from django.db import models


class Subunidade(models.Model):
    cod_estruturado = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=200)
    centro_nome = models.CharField(max_length=200)
    centro_sigla = models.CharField(max_length=30)
    tipo = models.CharField(max_length=100)
    situacao = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome
