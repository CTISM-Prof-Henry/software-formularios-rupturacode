from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
        dados = {
            "nome": "Risco de Teste",
            "descricao": "Descricao do risco de teste",
            "tipo": "riscos_operacionais",
            "departamento": "departamento_1",
            "impacto": "Alto",
            "probabilidade": "Media",
            "nivel_de_risco": "Alto",
            "eficacia_dos_controles": "Media",
            "nivel_residual": "Medio",
        }
        dados.update(kwargs)
        return Risco.objects.create(**dados)

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
        url = reverse("dashboard")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_riscos"], 0)
        self.assertEqual(response.context["riscos_alto_impacto"], 0)
        self.assertEqual(response.context["riscos_com_tratamentos"], 0)
        self.assertEqual(response.context["riscos_recentes"], 0)

    def test_dashboard_com_dados(self):
        usuario = self.criar_usuario()
        risco_alto = self.criar_risco(nome="Risco Alto", impacto="Alto")
        self.criar_risco(nome="Risco Baixo", impacto="Baixo")
        self.criar_tratamento(usuario, risco_alto)

        url = reverse("dashboard")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_riscos"], 2)
        self.assertEqual(response.context["riscos_alto_impacto"], 1)
        self.assertEqual(response.context["riscos_com_tratamentos"], 1)
        self.assertEqual(response.context["riscos_recentes"], 2)

    def test_dashboard_ignora_riscos_antigos_em_recentes(self):
        risco = self.criar_risco(nome="Risco Antigo")
        Risco.objects.filter(id=risco.id).update(
            data_criacao=timezone.now() - timedelta(days=31)
        )

        url = reverse("dashboard")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_riscos"], 1)
        self.assertEqual(response.context["riscos_recentes"], 0)
