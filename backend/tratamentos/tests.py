from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

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

    # Test listar tratamentos
    def test_listar_tratamentos_valido(self):
        self.criar_tratamento(resposta="Resposta 1")
        self.criar_tratamento(resposta="Resposta 2")

        tratamentos = Tratamento.objects.all()
        self.assertEqual(tratamentos.count(), 2)

    def test_listar_tratamentos_invalido(self):
        tratamentos = Tratamento.objects.all()
        self.assertEqual(tratamentos.count(), 0)
