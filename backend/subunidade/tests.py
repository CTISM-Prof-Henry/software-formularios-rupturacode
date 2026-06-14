from django.test import TestCase
from django.urls import reverse

from .models import Subunidade


def criar_unidade(**kwargs):
    dados = {
        "cod_estruturado": "07.67.00.00.0.0",
        "nome": "Departamento de Computacao Aplicada",
        "centro_nome": "Centro de Tecnologia",
        "centro_sigla": "CT",
        "tipo": "Departamento Didático",
        "situacao": "Formal",
        "ativo": True,
    }
    dados.update(kwargs)
    return Subunidade.objects.create(**dados)


class SubunidadeModelTest(TestCase):
    def test_criar_unidade_valida(self):
        unidade = criar_unidade()
        self.assertEqual(unidade.centro_sigla, "CT")
        self.assertTrue(unidade.ativo)
        self.assertEqual(str(unidade), "Departamento de Computacao Aplicada")

    def test_cod_estruturado_unico(self):
        criar_unidade()
        with self.assertRaises(Exception):
            criar_unidade(nome="Outra")


class SubunidadeApiTests(TestCase):
    def setUp(self):
        criar_unidade(cod_estruturado="07.67.00.00.0.0", nome="Computacao Aplicada", centro_sigla="CT")
        criar_unidade(cod_estruturado="07.37.00.00.0.0", nome="Eletromecanica", centro_sigla="CT")
        criar_unidade(
            cod_estruturado="10.01.00.00.0.0",
            nome="Letras",
            centro_sigla="CAL",
            centro_nome="Centro de Artes e Letras",
        )

    def test_centros_distintos(self):
        response = self.client.get(reverse("api_subunidades_centros"))
        self.assertEqual(response.status_code, 200)
        siglas = sorted(c["sigla"] for c in response.json()["results"])
        self.assertEqual(siglas, ["CAL", "CT"])

    def test_listar_unidades_por_centro(self):
        response = self.client.get(reverse("api_subunidades_collection"), {"centro": "CT"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_busca_por_nome(self):
        response = self.client.get(reverse("api_subunidades_collection"), {"busca": "Letras"})
        self.assertEqual(len(response.json()["results"]), 1)

    def test_unidade_inativa_nao_aparece(self):
        criar_unidade(cod_estruturado="99.99.00.00.0.0", nome="Extinta", situacao="Extinta", ativo=False)
        response = self.client.get(reverse("api_subunidades_collection"), {"centro": "CT"})
        self.assertEqual(len(response.json()["results"]), 2)
