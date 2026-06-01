from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from riscos.test_helpers import dados_risco_padrao
from riscos.models import Risco
from tratamentos.models import Tratamento
from usuario.models import Usuario


class DashboardTests(TestCase):
    def criar_usuario(self):
        return Usuario.objects.create(
            nome="Usuario Teste",
            matricula="12345",
            departamento="Departamento 1",
            cargo="Analista",
        )

    def criar_risco(self, **kwargs):
        return Risco.objects.create(**dados_risco_padrao(**kwargs))

    def criar_tratamento(self, usuario, risco):
        return Tratamento.objects.create(
            resposta="Resposta de teste",
            acao="Acao de teste",
            data_inicio=date(2026, 5, 1),
            data_fim=date(2026, 5, 30),
            situacao="Ativo",
            usuario_responsavel=usuario,
            risco=risco,
        )

    def test_dashboard_sem_dados(self):
        url = reverse("api_dashboard_summary")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["totalRiscos"], 0)
        self.assertEqual(data["riscosAltoImpacto"], 0)
        self.assertEqual(data["riscosComTratamento"], 0)
        self.assertEqual(data["novosRiscos"], 0)

    def test_dashboard_com_dados(self):
        usuario = self.criar_usuario()
        risco_alto = self.criar_risco(nome="Risco Alto", impacto="Alto")
        self.criar_risco(nome="Risco Baixo", impacto="Baixo")
        self.criar_tratamento(usuario, risco_alto)

        url = reverse("api_dashboard_summary")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["totalRiscos"], 2)
        self.assertEqual(data["riscosAltoImpacto"], 1)
        self.assertEqual(data["riscosComTratamento"], 1)
        self.assertEqual(data["novosRiscos"], 2)

    def test_dashboard_ignora_riscos_antigos_em_recentes(self):
        risco = self.criar_risco(nome="Risco Antigo")
        Risco.objects.filter(id=risco.id).update(
            data_criacao=timezone.now() - timedelta(days=31)
        )

        url = reverse("api_dashboard_summary")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["totalRiscos"], 1)
        self.assertEqual(data["novosRiscos"], 0)
