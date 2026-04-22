from django.test import TestCase
from .views import criar_risco


# Create your tests here.
def test_criar_risco():
    # Simula uma requisição POST para criar um novo risco
    response = criar_risco(
        {
            "method": "POST",
            "POST": {
                "nome": "Risco de Teste",
                "descricao": "Descrição do risco de teste",
                "probabilidade": 0.5,
                "impacto": 0.5,
            },
        }
    )

    # Verifica se a resposta é um redirecionamento para a página de sucesso
    assert response.status_code == 200
    assert "sucesso.html" in response.template_name


def test_criar_risco_com_dados_invalidos():
    # Simula uma requisição POST com dados inválidos (probabilidade fora do intervalo)
    response = criar_risco(
        {
            "method": "POST",
            "POST": {
                "nome": "Risco de Teste",
                "descricao": "Descrição do risco de teste",
                "probabilidade": 1.5,  # Valor inválido
                "impacto": 0.5,
            },
        }
    )

    # Verifica se a resposta contém erros de validação
    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors


def test_criar_risco_com_dados_faltando():
    # Simula uma requisição POST com dados faltando (nome)
    response = criar_risco(
        {
            "method": "POST",
            "POST": {
                "descricao": "Descrição do risco de teste",
                "probabilidade": 0.5,
                "impacto": 0.5,
            },
        }
    )

    # Verifica se a resposta contém erros de validação
    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors
