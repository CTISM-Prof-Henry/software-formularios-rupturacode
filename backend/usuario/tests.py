import json

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

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
        dados.setdefault("email", f"usuario{dados['matricula']}@teste.com")
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


class UsuarioApiTests(TestCase):
    def _post(self, url, payload):
        return self.client.post(url, data=json.dumps(payload), content_type="application/json")

    def _autenticar(self, **kwargs):
        # Gestao de usuarios exige nivel admin; default = admin via is_admin.
        dados = {
            "nome": "Auth", "email": "auth_api@atlas.com", "matricula": "9001",
            "departamento": "TI", "cargo": "Analista", "is_admin": True,
        }
        dados.update(kwargs)
        usuario = Usuario.objects.create(**dados)
        session = self.client.session
        session["usuario_id"] = usuario.id
        session.save()
        return usuario

    def test_criar_usuario_via_api(self):
        self._autenticar()
        response = self._post(
            reverse("api_usuarios_collection"),
            {
                "nome": "Joao",
                "email": "joao@atlas.com",
                "matricula": "777",
                "departamento": "TI",
                "cargo": "Analista",
                "senha": "segredo",
            },
        )
        self.assertEqual(response.status_code, 201)
        usuario = Usuario.objects.get(email="joao@atlas.com")
        # senha deve ser armazenada com hash, nunca em texto puro
        self.assertNotEqual(usuario.senha, "segredo")

    def test_criar_usuario_sem_campos_obrigatorios(self):
        self._autenticar()
        response = self._post(reverse("api_usuarios_collection"), {"nome": "X"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json()["errors"])

    def test_criar_usuario_cargo_invalido(self):
        self._autenticar()
        response = self._post(
            reverse("api_usuarios_collection"),
            {
                "nome": "Joao", "email": "j2@atlas.com", "matricula": "778",
                "departamento": "TI", "cargo": "Faxineiro", "senha": "x",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("cargo", response.json()["errors"])

    def test_me_inclui_nivel(self):
        # Cargo mapeia p/ nivel; is_admin sobrepoe para admin.
        Usuario.objects.create(
            nome="Prof", email="prof@atlas.com", matricula="500",
            departamento="TI", cargo="Professor", senha=make_password("1234"),
        )
        self._post(reverse("api_auth_login"), {"email": "prof@atlas.com", "senha": "1234"})
        self.assertEqual(self.client.get(reverse("api_auth_me")).json()["nivel"], "leitor")

    def test_gestao_usuarios_exige_admin(self):
        # Editor (cargo Analista, sem is_admin) nao pode criar usuarios.
        self._autenticar(cargo="Analista", is_admin=False)
        response = self._post(
            reverse("api_usuarios_collection"),
            {
                "nome": "Joao", "email": "j3@atlas.com", "matricula": "779",
                "departamento": "TI", "cargo": "Analista", "senha": "x",
            },
        )
        self.assertEqual(response.status_code, 403)


class CargoPermissaoApiTests(TestCase):
    def _post(self, url, payload):
        return self.client.post(url, data=json.dumps(payload), content_type="application/json")

    def _login_como(self, cargo, is_admin=False):
        usuario = Usuario.objects.create(
            nome=cargo, email=f"{cargo}@atlas.com", matricula=f"m{cargo}",
            departamento="TI", cargo=cargo, is_admin=is_admin,
        )
        session = self.client.session
        session["usuario_id"] = usuario.id
        session.save()

    def test_leitor_nao_cria_risco(self):
        from riscos.test_helpers import dados_risco_padrao

        self._login_como("Professor")  # leitor
        response = self._post(reverse("api_riscos_collection"), dados_risco_padrao())
        self.assertEqual(response.status_code, 403)

    def test_editor_cria_risco(self):
        from riscos.test_helpers import dados_risco_padrao

        self._login_como("Analista")  # editor
        response = self._post(reverse("api_riscos_collection"), dados_risco_padrao())
        self.assertEqual(response.status_code, 201)

    def test_cargos_list_traz_nivel(self):
        self._login_como("Diretor", is_admin=True)
        data = self.client.get(reverse("api_cargos_list")).json()
        niveis = {c["value"]: c["nivel"] for c in data["results"]}
        self.assertEqual(niveis["Diretor"], "admin")
        self.assertEqual(niveis["Analista"], "editor")
        self.assertEqual(niveis["Professor"], "leitor")

    def test_login_e_me(self):
        Usuario.objects.create(
            nome="Admin",
            email="admin@atlas.com",
            matricula="1",
            departamento="TI",
            cargo="Coord",
            senha=make_password("1234"),
        )
        login = self._post(reverse("api_auth_login"), {"email": "admin@atlas.com", "senha": "1234"})
        self.assertEqual(login.status_code, 200)

        me_response = self.client.get(reverse("api_auth_me"))
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()["email"], "admin@atlas.com")

    def test_login_invalido(self):
        response = self._post(reverse("api_auth_login"), {"email": "x@y.com", "senha": "errada"})
        self.assertEqual(response.status_code, 401)

    def test_me_sem_sessao(self):
        self.assertEqual(self.client.get(reverse("api_auth_me")).status_code, 401)
