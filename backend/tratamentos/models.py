from django.db import models


class Tratamento(models.Model):
    RESPOSTAS = [
        ("mitigar", "Mitigar / Reduzir"),
        ("evitar", "Evitar"),
        ("transferir", "Transferir"),
        ("aceitar", "Aceitar"),
    ]

    SITUACAO = [
        ("nao_iniciado", "Não Iniciado"),
        ("em_andamento", "Em andamento"),
        ("concluido", "Concluído"),
        ("suspenso", "Suspenso"),
    ]

    resposta = models.CharField(max_length=100, choices=RESPOSTAS)
    acao = models.CharField(max_length=255, blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    situacao = models.CharField(max_length=50, choices=SITUACAO, default="nao_iniciado")
    ativo = models.BooleanField(default=True)
    usuario_responsavel = models.ForeignKey(
        "usuario.Usuario", on_delete=models.SET_NULL, null=True, blank=True
    )
    risco = models.ForeignKey(
        "riscos.Risco", on_delete=models.CASCADE, related_name="tratamentos"
    )

    def __str__(self):
        return f"{self.get_resposta_display()} - {self.risco_id}"
