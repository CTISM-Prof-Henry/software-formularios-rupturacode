from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

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

    def test_criar_subunidade_invalida_endpoint(self):
        url = reverse('criar_subunidade')
        response = self.client.post(url, data={
            "nome": "",
            "descricao": "Descricao da subunidade sem nome",
            "sigla": "SUSN",
        })
        self.assertEqual(response.status_code, 200)

    def test_criar_subunidade_valida_endpoint(self):
        url = reverse('criar_subunidade')
        response = self.client.post(url, data={
            "nome": "SubUnidade de Teste",
            "descricao": "Descricao da subunidade de teste",
            "sigla": "SUT",
        })
        self.assertEqual(response.status_code, 200)

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

    def test_editar_subunidade_invalida_endpoint(self):
        subunidade = self.criar_subunidade()
        url = reverse('editar_subunidade', args=[subunidade.id])
        response = self.client.post(url, data={
            "nome": "",
            "descricao": "Descricao da subunidade sem nome",
            "sigla": "SUSN",
        })
        self.assertEqual(response.status_code, 200)

    def test_editar_subunidade_valida_endpoint(self):
        subunidade = self.criar_subunidade()
        url = reverse('editar_subunidade', args=[subunidade.id])
        response = self.client.post(url, data={
            "nome": "SubUnidade Editada",
            "descricao": "Descricao da subunidade editada",
            "sigla": "SE",
        })
        self.assertEqual(response.status_code, 200)

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

    def test_desativar_subunidade_invalida_endpoint(self):
        subunidade = self.criar_subunidade()
        url = reverse('desativar_subunidade', args=[subunidade.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_desativar_subunidade_valida_endpoint(self):
        subunidade = self.criar_subunidade()
        url = reverse('desativar_subunidade', args=[subunidade.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

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

    def test_detalhes_subunidade_invalida_endpoint(self):
        url = reverse('detalhes_subunidade', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detalhes_subunidade_valida_endpoint(self):
        subunidade = self.criar_subunidade(
            nome="SubUnidade para Detalhes",
            descricao="Descricao da subunidade para detalhes",
            sigla="SPD",
        )

        url = reverse('detalhes_subunidade', args=[subunidade.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Test listar subunidades
    def test_listar_subunidades_valida(self):
        self.criar_subunidade(nome="SubUnidade 1", sigla="SU1")
        self.criar_subunidade(nome="SubUnidade 2", sigla="SU2")

        subunidades = Subunidade.objects.all()
        self.assertEqual(subunidades.count(), 2)

    def test_listar_subunidades_invalida(self):
        subunidades = Subunidade.objects.all()
        self.assertEqual(subunidades.count(), 0)

    def test_listar_subunidades_invalida_endpoint(self):
        url = reverse('listar_subunidades')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_listar_subunidades_valida_endpoint(self):
        self.criar_subunidade(nome="SubUnidade 1", sigla="SU1")
        self.criar_subunidade(nome="SubUnidade 2", sigla="SU2")

        url = reverse('listar_subunidades')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
