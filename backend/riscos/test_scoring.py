from django.test import SimpleTestCase

from .scoring import nivel_de_risco, nivel_por_score, score


class ScoringTests(SimpleTestCase):
    def test_score_por_rotulo(self):
        self.assertEqual(score("Muito Baixa", "Insignificante"), 1)
        self.assertEqual(score("Muito Alta", "Catastrófico"), 25)
        self.assertEqual(score("Alta", "Grande"), 16)

    def test_score_aceita_numero(self):
        self.assertEqual(score("3", "4"), 12)
        self.assertEqual(score(5, 5), 25)

    def test_score_tolera_acento(self):
        self.assertEqual(score("Média", "Moderado"), 9)
        self.assertEqual(score("media", "moderado"), 9)

    def test_score_invalido_retorna_none(self):
        self.assertIsNone(score("Alto", "Grande"))  # "Alto" nao e probabilidade
        self.assertIsNone(score("", "Catastrófico"))
        self.assertIsNone(score("9", "Catastrófico"))  # fora de 1-5

    def test_faixas_de_nivel(self):
        self.assertEqual(nivel_por_score(4), "BAIXO")
        self.assertEqual(nivel_por_score(5), "MODERADO")
        self.assertEqual(nivel_por_score(9), "MODERADO")
        self.assertEqual(nivel_por_score(10), "ALTO")
        self.assertEqual(nivel_por_score(16), "ALTO")
        self.assertEqual(nivel_por_score(20), "EXTREMO")
        self.assertEqual(nivel_por_score(25), "EXTREMO")

    def test_nivel_none_vira_vazio(self):
        self.assertEqual(nivel_por_score(None), "")

    def test_nivel_de_risco_ponta_a_ponta(self):
        self.assertEqual(nivel_de_risco("Muito Baixa", "Insignificante"), "BAIXO")
        self.assertEqual(nivel_de_risco("Muito Alta", "Catastrófico"), "EXTREMO")
        self.assertEqual(nivel_de_risco("Alto", "Grande"), "")  # legado nao mapeavel
