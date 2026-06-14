import json

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from usuario.models import Usuario

from .models import Risco
from .test_helpers import dados_risco_padrao


class RiscoTests(TestCase):
    def setUp(self):
        # A API exige sessao; autentica o client de teste.
        usuario = Usuario.objects.create(
            nome="Auth", email="auth@atlas.com", matricula="999",
            departamento="TI", cargo="Analista",
        )
        session = self.client.session
        session["usuario_id"] = usuario.id
        session.save()

    def dados_risco(self, **kwargs):
        return dados_risco_padrao(**kwargs)

    def test_sem_sessao_retorna_401(self):
        sem_auth = self.client_class()
        response = sem_auth.get(reverse("api_riscos_collection"))
        self.assertEqual(response.status_code, 401)

    def criar_risco(self, **kwargs):
        return Risco.objects.create(**self.dados_risco(**kwargs))

    # Test criar risco
    def test_criar_risco_valido(self):
        risco = self.criar_risco()

        self.assertEqual(risco.nome, "Risco de Teste")
        self.assertEqual(risco.descricao, "Descricao do risco de teste")
        self.assertEqual(risco.tipo, "riscos_operacionais")
        self.assertEqual(risco.departamento, "departamento_1")
        self.assertTrue(risco.ativo)

    def test_criar_risco_invalido(self):
        risco = self.criar_risco(nome="")

        with self.assertRaises(ValidationError):
            risco.full_clean()

    def test_criar_risco_invalido_endpoint(self):
        url = reverse("api_riscos_collection")
        response = self.client.post(
            url,
            data=json.dumps(self.dados_risco(nome="")),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Risco.objects.count(), 0)

    def test_criar_risco_valido_endpoint(self):
        url = reverse("api_riscos_collection")
        response = self.client.post(
            url,
            data=json.dumps(self.dados_risco()),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Risco.objects.count(), 1)
        self.assertEqual(response.json()["nome"], "Risco de Teste")

    # Test editar risco
    def test_editar_risco_valido(self):
        risco = self.criar_risco()

        risco.nome = "Risco Editado"
        risco.descricao = "Descricao do risco editado"
        risco.impacto = "Baixo"
        risco.save()

        risco.refresh_from_db()
        self.assertEqual(risco.nome, "Risco Editado")
        self.assertEqual(risco.descricao, "Descricao do risco editado")
        self.assertEqual(risco.impacto, "Baixo")

    def test_editar_risco_invalido(self):
        risco = self.criar_risco()
        risco.nome = ""

        with self.assertRaises(ValidationError):
            risco.full_clean()

    # Test desativar risco
    def test_desativar_risco_valido(self):
        risco = self.criar_risco()
        risco.ativo = False
        risco.save()

        risco.refresh_from_db()
        self.assertFalse(risco.ativo)

    def test_desativar_risco_invalido(self):
        risco = self.criar_risco()
        risco.ativo = "invalid_value"

        with self.assertRaises(ValidationError):
            risco.full_clean()

    # Test detalhes risco
    def test_detalhes_risco_valido(self):
        risco = self.criar_risco(
            nome="Risco para Detalhes",
            descricao="Descricao do risco para detalhes",
            nivel_de_risco="Medio",
        )

        self.assertEqual(risco.nome, "Risco para Detalhes")
        self.assertEqual(risco.descricao, "Descricao do risco para detalhes")
        self.assertEqual(risco.nivel_de_risco, "Medio")

    def test_detalhes_risco_invalido(self):
        with self.assertRaises(Risco.DoesNotExist):
            Risco.objects.get(id=999)

    # Test listar riscos
    def test_listar_riscos_valido(self):
        self.criar_risco(nome="Risco 1")
        self.criar_risco(nome="Risco 2")

        riscos = Risco.objects.all()
        self.assertEqual(riscos.count(), 2)

    def test_listar_riscos_invalido(self):
        riscos = Risco.objects.all()
        self.assertEqual(riscos.count(), 0)

    def test_listar_riscos_invalido_endpoint(self):
        url = reverse("api_riscos_collection")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"], [])

    # Test endpoint de detalhe (GET/PUT/DELETE)
    def test_detalhe_risco_get_endpoint(self):
        risco = self.criar_risco()
        url = reverse("api_riscos_detail", args=[risco.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome"], "Risco de Teste")

    def test_detalhe_risco_put_endpoint(self):
        risco = self.criar_risco()
        url = reverse("api_riscos_detail", args=[risco.id])
        payload = self.dados_risco(nome="Risco Atualizado", descricao="Nova descricao do risco")
        response = self.client.put(url, data=json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        risco.refresh_from_db()
        self.assertEqual(risco.nome, "Risco Atualizado")

    def test_detalhe_risco_delete_faz_soft_delete(self):
        risco = self.criar_risco()
        url = reverse("api_riscos_detail", args=[risco.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        risco.refresh_from_db()
        self.assertFalse(risco.ativo)

    def test_detalhe_risco_inexistente_retorna_404(self):
        url = reverse("api_riscos_detail", args=[999])
        self.assertEqual(self.client.get(url).status_code, 404)

    # Test risco residual (Fase 4)
    def test_nivel_residual_calculado_no_endpoint(self):
        url = reverse("api_riscos_collection")
        payload = self.dados_risco(
            probability="Muito Baixa",
            impact="Insignificante",
            probabilityResidual="Muito Baixa",
            impactResidual="Insignificante",
        )
        response = self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["nivelResidual"], "BAIXO")
        self.assertEqual(response.json()["scoreResidual"], 1)

    def test_criar_risco_sem_residual_ok(self):
        url = reverse("api_riscos_collection")
        payload = self.dados_risco(nivel_residual="", residualLevel="")
        response = self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_listar_riscos_valido_endpoint(self):
        self.criar_risco(nome="Risco 1")
        self.criar_risco(nome="Risco 2")
        url = reverse("api_riscos_collection")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
