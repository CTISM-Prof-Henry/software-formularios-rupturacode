from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Risco


class RiscoTests(TestCase):

    # Test criar risco
    def test_criar_risco_valido(self):
        risco = Risco.objects.create(
            nome="Risco de Teste",
            descricao="Descrição do risco de teste",
        )
        self.assertEqual(risco.nome, "Risco de Teste")
        self.assertEqual(risco.descricao, "Descrição do risco de teste")
        self.assertTrue(risco.ativo)
        
    def test_criar_risco_invalido(self):
        with self.assertRaises(ValidationError):
            Risco.objects.create(
                nome="",
                descricao="Descrição do risco sem nome",
            ).full_clean()
            
    # Test editar risco
    def test_editar_risco_valido(self):
        risco = Risco.objects.create(
            nome="Risco para Editar",
            descricao="Descrição do risco para editar",
        )

        risco.nome = "Risco Editado"
        risco.descricao = "Descrição do risco editado"
        risco.save()

        risco.refresh_from_db()
        self.assertEqual(risco.nome, "Risco Editado")
        self.assertEqual(risco.descricao, "Descrição do risco editado")
    
    def test_editar_risco_invalido(self):
        risco = Risco.objects.create(
            nome="Risco para Editar",
            descricao="Descrição do risco para editar",
        )

        risco.nome = ""

        with self.assertRaises(ValidationError):
            risco.full_clean()
            
    # Test desativar risco
    def test_desativar_risco_valido(self):
        risco = Risco.objects.create(
            nome="Risco para Desativar",
            descricao="Descrição do risco para desativar",
        )

        risco.ativo = False
        risco.save()

        risco.refresh_from_db()
        self.assertFalse(risco.ativo)
        
    def test_desativar_risco_invalido(self):
        risco = Risco.objects.create(
            nome="Risco para Desativar",
            descricao="Descrição do risco para desativar",
        )

        risco.ativo = "invalid_value"

        with self.assertRaises(ValidationError):
            risco.full_clean()
    
    # Test detalhes risco
    def test_detalhes_risco_valido(self):
        risco = Risco.objects.create(
            nome="Risco para Detalhes",
            descricao="Descrição do risco para detalhes",
        )

        self.assertEqual(risco.nome, "Risco para Detalhes")
        self.assertEqual(risco.descricao, "Descrição do risco para detalhes")
        
    def test_detalhes_risco_invalido(self):
        risco = Risco.objects.create(
            nome="Risco para Detalhes",
            descricao="Descrição do risco para detalhes",
        )

        risco.nome = ""

        with self.assertRaises(ValidationError):
            risco.full_clean()