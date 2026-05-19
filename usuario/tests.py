from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Usuario


class UsuarioTests(TestCase):
    def criar_usuario(self, **kwargs):
        dados = {
            "nome": "Usuario de Teste",
            "matricula": "12345",
            "departamento": "Departamento 1",
            "cargo": "Analista",
        }
        dados.update(kwargs)
        return Usuario.objects.create(**dados)

    # Test criar usuario
    def test_criar_usuario_valido(self):
        usuario = self.criar_usuario()

        self.assertEqual(usuario.nome, "Usuario de Teste")
        self.assertEqual(usuario.matricula, "12345")
        self.assertEqual(usuario.departamento, "Departamento 1")
        self.assertEqual(usuario.cargo, "Analista")
        self.assertFalse(usuario.is_admin)

    def test_criar_usuario_invalido(self):
        usuario = self.criar_usuario(nome="")

        with self.assertRaises(ValidationError):
            usuario.full_clean()

    def test_criar_usuario_com_matricula_repetida_invalido(self):
        self.criar_usuario(matricula="12345")
        usuario = Usuario(
            nome="Usuario Duplicado",
            matricula="12345",
            departamento="Departamento 1",
            cargo="Analista",
        )

        with self.assertRaises(ValidationError):
            usuario.full_clean()

    # Test editar usuario
    def test_editar_usuario_valido(self):
        usuario = self.criar_usuario()

        usuario.nome = "Usuario Editado"
        usuario.departamento = "Departamento 2"
        usuario.cargo = "Coordenador"
        usuario.is_admin = True
        usuario.save()

        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, "Usuario Editado")
        self.assertEqual(usuario.departamento, "Departamento 2")
        self.assertEqual(usuario.cargo, "Coordenador")
        self.assertTrue(usuario.is_admin)

    def test_editar_usuario_invalido(self):
        usuario = self.criar_usuario()
        usuario.matricula = ""

        with self.assertRaises(ValidationError):
            usuario.full_clean()

    # Test detalhes usuario
    def test_detalhes_usuario_valido(self):
        usuario = self.criar_usuario(
            nome="Usuario para Detalhes",
            matricula="54321",
            cargo="Gerente",
        )

        self.assertEqual(usuario.nome, "Usuario para Detalhes")
        self.assertEqual(usuario.matricula, "54321")
        self.assertEqual(usuario.cargo, "Gerente")

    def test_detalhes_usuario_invalido(self):
        with self.assertRaises(Usuario.DoesNotExist):
            Usuario.objects.get(id=999)

    # Test listar usuarios
    def test_listar_usuarios_valido(self):
        self.criar_usuario(matricula="12345")
        self.criar_usuario(nome="Usuario 2", matricula="67890")

        usuarios = Usuario.objects.all()
        self.assertEqual(usuarios.count(), 2)

    def test_listar_usuarios_invalido(self):
        usuarios = Usuario.objects.all()
        self.assertEqual(usuarios.count(), 0)
