from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from riscos.models import Risco
from usuario.models import Usuario

from .models import Tratamento


class TratamentoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="Usuario Teste",
            matricula="12345",
            departamento="Departamento 1",
            cargo="Analista",
        )
        self.risco = Risco.objects.create(
            nome="Risco de Teste",
            descricao="Descricao do risco de teste",
            tipo="riscos_operacionais",
            departamento="departamento_1",
            impacto="Alto",
            probabilidade="Media",
            nivel_de_risco="Alto",
            eficacia_dos_controles="Media",
            nivel_residual="Medio",
        )

    def dados_tratamento(self, **kwargs):
        dados = {
            "resposta": "Resposta de teste",
            "acao": "Acao de teste",
            "data_inicio": date(2026, 5, 1),
            "data_fim": date(2026, 5, 30),
            "situacao": "Ativo",
            "usuario_responsavel": self.usuario,
            "risco": self.risco,
        }
        dados.update(kwargs)
        return dados

    def dados_formulario_tratamento(self, **kwargs):
        dados = {
            "resposta": "Resposta de teste",
            "acao": "Acao de teste",
            "data_inicio": "2026-05-01",
            "data_fim": "2026-05-30",
            "situacao": "Ativo",
        }
        dados.update(kwargs)
        return dados

    def criar_tratamento(self, **kwargs):
        return Tratamento.objects.create(**self.dados_tratamento(**kwargs))

    # Test criar tratamento
    def test_criar_tratamento_valido(self):
        tratamento = self.criar_tratamento()

        self.assertEqual(tratamento.resposta, "Resposta de teste")
        self.assertEqual(tratamento.acao, "Acao de teste")
        self.assertEqual(tratamento.situacao, "Ativo")
        self.assertEqual(tratamento.usuario_responsavel, self.usuario)
        self.assertEqual(tratamento.risco, self.risco)

    def test_criar_tratamento_invalido(self):
        tratamento = self.criar_tratamento(resposta="")

        with self.assertRaises(ValidationError):
            tratamento.full_clean()

    def test_criar_tratamento_invalido_endpoint(self):
        url = reverse("criar_tratamento")
        response = self.client.post(
            url,
            data=self.dados_formulario_tratamento(resposta=""),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tratamento.objects.count(), 0)

    def test_criar_tratamento_valido_endpoint(self):
        url = reverse("criar_tratamento")
        response = self.client.post(url, data=self.dados_formulario_tratamento())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tratamento.objects.count(), 1)

    # Test editar tratamento
    def test_editar_tratamento_valido(self):
        tratamento = self.criar_tratamento()

        tratamento.resposta = "Resposta editada"
        tratamento.acao = "Acao editada"
        tratamento.situacao = "Em andamento"
        tratamento.save()

        tratamento.refresh_from_db()
        self.assertEqual(tratamento.resposta, "Resposta editada")
        self.assertEqual(tratamento.acao, "Acao editada")
        self.assertEqual(tratamento.situacao, "Em andamento")

    def test_editar_tratamento_invalido(self):
        tratamento = self.criar_tratamento()
        tratamento.acao = ""

        with self.assertRaises(ValidationError):
            tratamento.full_clean()

    def test_editar_tratamento_invalido_endpoint(self):
        tratamento = self.criar_tratamento()
        url = reverse("editar_tratamento", args=[tratamento.id])
        response = self.client.post(
            url,
            data=self.dados_formulario_tratamento(acao=""),
        )

        tratamento.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tratamento.acao, "Acao de teste")

    def test_editar_tratamento_valido_endpoint(self):
        tratamento = self.criar_tratamento()
        url = reverse("editar_tratamento", args=[tratamento.id])
        response = self.client.post(
            url,
            data=self.dados_formulario_tratamento(
                resposta="Resposta editada",
                acao="Acao editada",
                situacao="Em andamento",
            ),
        )

        tratamento.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tratamento.resposta, "Resposta editada")
        self.assertEqual(tratamento.acao, "Acao editada")
        self.assertEqual(tratamento.situacao, "Em andamento")

    # Test desativar tratamento
    def test_desativar_tratamento_valido(self):
        tratamento = self.criar_tratamento()
        tratamento.situacao = "Desativado"
        tratamento.save()

        tratamento.refresh_from_db()
        self.assertEqual(tratamento.situacao, "Desativado")

    def test_desativar_tratamento_invalido(self):
        tratamento = self.criar_tratamento()
        tratamento.situacao = ""

        with self.assertRaises(ValidationError):
            tratamento.full_clean()

    def test_desativar_tratamento_invalido_endpoint(self):
        url = reverse("desativar_tratamento", args=[999])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_desativar_tratamento_valido_endpoint(self):
        tratamento = self.criar_tratamento()
        url = reverse("desativar_tratamento", args=[tratamento.id])
        response = self.client.post(url)

        tratamento.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tratamento.situacao, "Desativado")

    # Test detalhes tratamento
    def test_detalhes_tratamento_valido(self):
        tratamento = self.criar_tratamento(
            resposta="Resposta para detalhes",
            acao="Acao para detalhes",
        )

        self.assertEqual(tratamento.resposta, "Resposta para detalhes")
        self.assertEqual(tratamento.acao, "Acao para detalhes")

    def test_detalhes_tratamento_invalido(self):
        with self.assertRaises(Tratamento.DoesNotExist):
            Tratamento.objects.get(id=999)

    def test_detalhes_tratamento_invalido_endpoint(self):
        url = reverse("detalhes_tratamento", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detalhes_tratamento_valido_endpoint(self):
        tratamento = self.criar_tratamento(
            resposta="Resposta para detalhes",
            acao="Acao para detalhes",
        )
        url = reverse("detalhes_tratamento", args=[tratamento.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # Test listar tratamentos
    def test_listar_tratamentos_valido(self):
        self.criar_tratamento(resposta="Resposta 1")
        self.criar_tratamento(resposta="Resposta 2")

        tratamentos = Tratamento.objects.all()
        self.assertEqual(tratamentos.count(), 2)

    def test_listar_tratamentos_invalido(self):
        tratamentos = Tratamento.objects.all()
        self.assertEqual(tratamentos.count(), 0)

    def test_listar_tratamentos_invalido_endpoint(self):
        url = reverse("listar_tratamentos")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_listar_tratamentos_valido_endpoint(self):
        self.criar_tratamento(resposta="Resposta 1")
        self.criar_tratamento(resposta="Resposta 2")
        url = reverse("listar_tratamentos")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["tratamentos"]), 2)
