from django.db import models


# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50, unique=True)
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
