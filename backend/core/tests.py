from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from riscos.test_helpers import dados_risco_padrao
from riscos.models import Risco
from tratamentos.models import Tratamento
from usuario.models import Usuario


class DashboardTests(TestCase):
    def setUp(self):
        # O endpoint do dashboard exige sessao.
        usuario = Usuario.objects.create(
            nome="Auth", email="auth_dash@atlas.com", matricula="9200",
            departamento="TI", cargo="Analista",
        )
        session = self.client.session
        session["usuario_id"] = usuario.id
        session.save()

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

    def test_dashboard_mapa_de_risco(self):
        # Eixos na escala canônica (probabilidade x impacto -> 1-5).
        self.criar_risco(nome="R1", probabilidade="Média", impacto="Grande")
        self.criar_risco(nome="R2", probabilidade="Média", impacto="Grande")
        self.criar_risco(nome="R3", probabilidade="Alta", impacto="Catastrófico")
        # Fora da escala: não entra no mapa.
        self.criar_risco(nome="R4", probabilidade="?", impacto="?")

        data = self.client.get(reverse("api_dashboard_summary")).json()
        mapa = {(c["probabilidade"], c["impacto"]): c["total"] for c in data["mapaDeRisco"]}

        self.assertEqual(mapa.get((3, 4)), 2)
        self.assertEqual(mapa.get((4, 5)), 1)
        self.assertNotIn((0, 0), mapa)
        self.assertEqual(sum(mapa.values()), 3)

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
