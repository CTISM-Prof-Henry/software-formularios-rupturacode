from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Tratamento

# Create your tests here.
class TratamentoTests(TestCase):
    
    # Test criar tratamento
    def test_criar_tratamento_valido(self):
        tratamento = Tratamento.objects.create(
            nome="Tratamento de Teste",
            descricao="Descrição do tratamento de teste",
        )
        self.assertEqual(tratamento.nome, "Tratamento de Teste")
        self.assertEqual(tratamento.descricao, "Descrição do tratamento de teste")
        self.assertTrue(tratamento.ativo)
    
    def test_criar_tratamento_invalido(self):
        with self.assertRaises(ValidationError):
            Tratamento.objects.create(
                nome="",
                descricao="Descrição do tratamento sem nome",
            ).full_clean()
    
    # Test editar tratamento
    def test_editar_tratamento_valido(self):
        tratamento = Tratamento.objects.create(
            nome="Tratamento para Editar",
            descricao="Descrição do tratamento para editar",
        )

        tratamento.nome = "Tratamento Editado"
        tratamento.descricao = "Descrição do tratamento editado"
        tratamento.save()

        tratamento.refresh_from_db()
        self.assertEqual(tratamento.nome, "Tratamento Editado")
        self.assertEqual(tratamento.descricao, "Descrição do tratamento editado")
        
    def test_editar_tratamento_invalido(self):
        tratamento = Tratamento.objects.create(
            nome="Tratamento para Editar",
            descricao="Descrição do tratamento para editar",
        )

        tratamento.nome = ""

        with self.assertRaises(ValidationError):
            tratamento.full_clean()
            
    # Test desativar tratamento
    def test_desativar_tratamento_valido(self):
        tratamento = Tratamento.objects.create(
            nome="Tratamento para Desativar",
            descricao="Descrição do tratamento para desativar",
        )

        tratamento.ativo = False
        tratamento.save()
        
    def test_desativar_tratamento_invalido(self):
        tratamento = Tratamento.objects.create(
            nome="Tratamento para Desativar",
            descricao="Descrição do tratamento para desativar",
        )

        tratamento.ativo = "invalid_value"

        with self.assertRaises(ValidationError):
            tratamento.full_clean()
            
    # Test detalhes tratamento
    def test_detalhes_tratamento_valido(self):
        tratamento = Tratamento.objects.create(
            nome="Tratamento para Detalhes",
            descricao="Descrição do tratamento para detalhes",
        )

        self.assertEqual(tratamento.nome, "Tratamento para Detalhes")
        self.assertEqual(tratamento.descricao, "Descrição do tratamento para detalhes")
        
    def test_detalhes_tratamento_invalido(self):
        tratamento = Tratamento.objects.create(
            nome="Tratamento para Detalhes",
            descricao="Descrição do tratamento para detalhes",
        )

        self.assertEqual(tratamento.nome, "Tratamento para Detalhes")
        self.assertEqual(tratamento.descricao, "Descrição do tratamento para detalhes")
    