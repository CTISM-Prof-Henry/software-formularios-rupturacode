from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Subunidade


class SubUnidadeModelTest(TestCase):
    def criar_subunidade(self, **kwargs):
        dados = {
            "nome": "SubUnidade de Teste",
            "descricao": "Descricao da subunidade de teste",
            "sigla": "SUT",
        }
        dados.update(kwargs)
        return Subunidade.objects.create(**dados)

    # Test criar subunidade
    def test_criar_subunidade_valida(self):
        subunidade = self.criar_subunidade()

        self.assertEqual(subunidade.nome, "SubUnidade de Teste")
        self.assertEqual(subunidade.descricao, "Descricao da subunidade de teste")
        self.assertEqual(subunidade.sigla, "SUT")
        self.assertTrue(subunidade.ativo)

    def test_criar_subunidade_invalida(self):
        subunidade = self.criar_subunidade(nome="")

        with self.assertRaises(ValidationError):
            subunidade.full_clean()

    # Test editar subunidade
    def test_editar_subunidade_valida(self):
        subunidade = self.criar_subunidade()

        subunidade.nome = "SubUnidade Editada"
        subunidade.descricao = "Descricao da subunidade editada"
        subunidade.sigla = "SE"
        subunidade.save()

        subunidade.refresh_from_db()
        self.assertEqual(subunidade.nome, "SubUnidade Editada")
        self.assertEqual(subunidade.descricao, "Descricao da subunidade editada")
        self.assertEqual(subunidade.sigla, "SE")

    def test_editar_subunidade_invalida(self):
        subunidade = self.criar_subunidade()
        subunidade.nome = ""

        with self.assertRaises(ValidationError):
            subunidade.full_clean()

    # Test desativar subunidade
    def test_desativar_subunidade_valida(self):
        subunidade = self.criar_subunidade()
        subunidade.ativo = False
        subunidade.save()

        subunidade.refresh_from_db()
        self.assertFalse(subunidade.ativo)

    def test_desativar_subunidade_invalida(self):
        subunidade = self.criar_subunidade()
        subunidade.ativo = False
        subunidade.save()

        subunidade.refresh_from_db()
        self.assertFalse(subunidade.ativo)

    # Test detalhes subunidade
    def test_detalhes_subunidade_valida(self):
        subunidade = self.criar_subunidade(
            nome="SubUnidade para Detalhes",
            descricao="Descricao da subunidade para detalhes",
            sigla="SPD",
        )

        self.assertEqual(subunidade.nome, "SubUnidade para Detalhes")
        self.assertEqual(subunidade.descricao, "Descricao da subunidade para detalhes")
        self.assertEqual(subunidade.sigla, "SPD")

    def test_detalhes_subunidade_invalida(self):
        with self.assertRaises(Subunidade.DoesNotExist):
            Subunidade.objects.get(id=999)

    # Test listar subunidades
    def test_listar_subunidades_valida(self):
        self.criar_subunidade(nome="SubUnidade 1", sigla="SU1")
        self.criar_subunidade(nome="SubUnidade 2", sigla="SU2")

        subunidades = Subunidade.objects.all()
        self.assertEqual(subunidades.count(), 2)

    def test_listar_subunidades_invalida(self):
        subunidades = Subunidade.objects.all()
        self.assertEqual(subunidades.count(), 0)
