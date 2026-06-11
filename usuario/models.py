from django.db import models


# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    matricula = models.CharField(max_length=50, unique=True)
    centro = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    senha = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
