from django.db import models


# Create your models here.
class Tratamento(models.Model):
    SITUACAO = []

    resposta = models.CharField(max_length=100)
    acao = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    situacao = models.CharField(max_length=50)
    usuario_responsavel = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)
    risco = models.ForeignKey("riscos.Risco", on_delete=models.CASCADE)
