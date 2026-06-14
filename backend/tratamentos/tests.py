import json
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from riscos.models import Risco
from riscos.test_helpers import dados_risco_padrao
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
        self.risco = Risco.objects.create(**dados_risco_padrao())

    def dados_tratamento(self, **kwargs):
        dados = {
            "resposta": "mitigar",
            "acao": "Acao de teste",
            "data_inicio": date(2026, 5, 1),
            "data_fim": date(2026, 5, 30),
            "situacao": "em_andamento",
            "usuario_responsavel": self.usuario,
            "risco": self.risco,
        }
        dados.update(kwargs)
        return dados

    def criar_tratamento(self, **kwargs):
        return Tratamento.objects.create(**self.dados_tratamento(**kwargs))

    def test_criar_tratamento_valido(self):
        tratamento = self.criar_tratamento()
        self.assertEqual(tratamento.resposta, "mitigar")
        self.assertEqual(tratamento.situacao, "em_andamento")
        self.assertEqual(tratamento.usuario_responsavel, self.usuario)
        self.assertEqual(tratamento.risco, self.risco)
        self.assertTrue(tratamento.ativo)

    def test_resposta_invalida_falha_no_clean(self):
        tratamento = self.criar_tratamento(resposta="valor_invalido")
        with self.assertRaises(ValidationError):
            tratamento.full_clean()

    def test_situacao_invalida_falha_no_clean(self):
        tratamento = self.criar_tratamento(situacao="valor_invalido")
        with self.assertRaises(ValidationError):
            tratamento.full_clean()

    def test_editar_tratamento_valido(self):
        tratamento = self.criar_tratamento()
        tratamento.situacao = "concluido"
        tratamento.save()
        tratamento.refresh_from_db()
        self.assertEqual(tratamento.situacao, "concluido")


class TratamentoApiTests(TestCase):
    def setUp(self):
        self.risco = Risco.objects.create(**dados_risco_padrao())
        self.usuario = Usuario.objects.create(
            nome="Responsavel",
            email="resp@atlas.com",
            matricula="123",
            departamento="departamento_1",
            cargo="Analista",
        )
        # A API exige sessao; autentica o client de teste.
        session = self.client.session
        session["usuario_id"] = self.usuario.id
        session.save()

    def _payload(self, **kwargs):
        dados = {
            "riscoId": self.risco.id,
            "resposta": "Mitigar / Reduzir",
            "acao": "Implementar backup em nuvem",
            "dataInicio": "2026-01-01",
            "dataFim": "2026-02-01",
            "status": "Em andamento",
            "usuarioResponsavelId": self.usuario.id,
        }
        dados.update(kwargs)
        return dados

    def _post(self, payload):
        return self.client.post(
            reverse("api_tratamentos_collection"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_criar_tratamento_valido(self):
        resp = self._post(self._payload())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Tratamento.objects.count(), 1)
        body = resp.json()
        self.assertEqual(body["resposta"], "mitigar")
        self.assertEqual(body["situacao"], "em_andamento")
        self.assertEqual(body["usuarioResponsavelNome"], "Responsavel")

    def test_criar_aceitar_sem_acao_e_prazo(self):
        resp = self._post(
            self._payload(resposta="Aceitar", acao="", dataInicio="", dataFim="")
        )
        self.assertEqual(resp.status_code, 201)

    def test_mitigar_sem_acao_falha(self):
        resp = self._post(self._payload(acao="", dataFim=""))
        self.assertEqual(resp.status_code, 400)
        self.assertIn("acao", resp.json()["errors"])

    def test_risco_inexistente_falha(self):
        resp = self._post(self._payload(riscoId=9999))
        self.assertEqual(resp.status_code, 400)

    def test_filtra_por_risco(self):
        Tratamento.objects.create(risco=self.risco, resposta="mitigar", situacao="nao_iniciado")
        outro = Risco.objects.create(**dados_risco_padrao(nome="Outro"))
        Tratamento.objects.create(risco=outro, resposta="evitar", situacao="nao_iniciado")
        resp = self.client.get(reverse("api_tratamentos_collection"), {"risco": self.risco.id})
        self.assertEqual(len(resp.json()["results"]), 1)

    def test_delete_faz_soft_delete(self):
        t = Tratamento.objects.create(
            risco=self.risco, resposta="mitigar", situacao="nao_iniciado"
        )
        resp = self.client.delete(reverse("api_tratamentos_detail", args=[t.id]))
        self.assertEqual(resp.status_code, 200)
        t.refresh_from_db()
        self.assertFalse(t.ativo)

    def test_com_tratamento_no_risco(self):
        Tratamento.objects.create(risco=self.risco, resposta="mitigar", situacao="nao_iniciado")
        resp = self.client.get(reverse("api_riscos_detail", args=[self.risco.id]))
        self.assertTrue(resp.json()["comTratamento"])

    def test_atrasado_quando_prazo_vencido_e_nao_concluido(self):
        Tratamento.objects.create(
            risco=self.risco,
            resposta="mitigar",
            situacao="em_andamento",
            data_fim=date(2020, 1, 1),
        )
        resp = self.client.get(reverse("api_tratamentos_collection"), {"risco": self.risco.id})
        self.assertTrue(resp.json()["results"][0]["atrasado"])

    def test_nao_atrasado_quando_concluido(self):
        Tratamento.objects.create(
            risco=self.risco,
            resposta="mitigar",
            situacao="concluido",
            data_fim=date(2020, 1, 1),
        )
        resp = self.client.get(reverse("api_tratamentos_collection"), {"risco": self.risco.id})
        self.assertFalse(resp.json()["results"][0]["atrasado"])

    def test_filtra_por_responsavel(self):
        Tratamento.objects.create(
            risco=self.risco,
            resposta="mitigar",
            situacao="nao_iniciado",
            usuario_responsavel=self.usuario,
        )
        Tratamento.objects.create(risco=self.risco, resposta="evitar", situacao="nao_iniciado")
        resp = self.client.get(
            reverse("api_tratamentos_collection"), {"responsavel": self.usuario.id}
        )
        self.assertEqual(len(resp.json()["results"]), 1)
