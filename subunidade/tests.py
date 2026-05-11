from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import SubUnidade

# Create your tests here.
class SubUnidadeModelTest(TestCase):
    # Test criar subunidade
    def test_criar_subunidade_valida(self):
        subunidade = SubUnidade.objects.create(
            nome="SubUnidade de Teste",
            descricao="Descrição da subunidade de teste",
        )
        self.assertEqual(subunidade.nome, "SubUnidade de Teste")
        self.assertEqual(subunidade.descricao, "Descrição da subunidade de teste")
        self.assertTrue(subunidade.ativo)
    
    def test_criar_subunidade_invalida(self):
        with self.assertRaises(ValidationError):
            SubUnidade.objects.create(
                nome="",
                descricao="Descrição da subunidade sem nome",
            ).full_clean()
    
    # Test editar subunidade
    def test_editar_subunidade_valida(self):
        subunidade = SubUnidade.objects.create(
            nome="SubUnidade para Editar",
            descricao="Descrição da subunidade para editar",
        )

        subunidade.nome = "SubUnidade Editada"
        subunidade.descricao = "Descrição da subunidade editada"
        subunidade.save()

        subunidade.refresh_from_db()
        self.assertEqual(subunidade.nome, "SubUnidade Editada")
        self.assertEqual(subunidade.descricao, "Descrição da subunidade editada")
        
    def test_editar_subunidade_invalida(self):
        subunidade = SubUnidade.objects.create(
            nome="SubUnidade para Editar",
            descricao="Descrição da subunidade para editar",
        )

        subunidade.nome = ""

        with self.assertRaises(ValidationError):
            subunidade.full_clean()
    
    # Test desativar subunidade
    def test_desativar_subunidade_valida(self):
        subunidade = SubUnidade.objects.create(
            nome="SubUnidade para Desativar",
            descricao="Descrição da subunidade para desativar",
        )

        subunidade.ativo = False
        subunidade.save()
    
    # Test detalhes subunidade
    def test_detalhes_subunidade_valida(self):
        subunidade = SubUnidade.objects.create(
            nome="SubUnidade para Detalhes",
            descricao="Descrição da subunidade para detalhes",
        )

        self.assertEqual(subunidade.nome, "SubUnidade para Detalhes")
        self.assertEqual(subunidade.descricao, "Descrição da subunidade para detalhes")
    
    def test_detalhes_subunidade_invalida(self):
        with self.assertRaises(SubUnidade.DoesNotExist):
            SubUnidade.objects.get(id=999)
    
    # Test listar subunidades
    def test_listar_subunidades_valida(self):
        SubUnidade.objects.create(
            nome="SubUnidade 1",
            descricao="Descrição da subunidade 1",
        )
        SubUnidade.objects.create(
            nome="SubUnidade 2",
            descricao="Descrição da subunidade 2",
        )

        subunidades = SubUnidade.objects.all()
        self.assertEqual(subunidades.count(), 2)
        
    def test_listar_subunidades_invalida(self):
        subunidades = SubUnidade.objects.all()
        self.assertEqual(subunidades.count(), 0)
    
        