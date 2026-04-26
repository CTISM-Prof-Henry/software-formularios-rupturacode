from django.db import models


# Create your models here.
class Subunidade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    sigla = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
