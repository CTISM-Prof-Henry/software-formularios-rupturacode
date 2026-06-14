def dados_risco_padrao(**kwargs):
    dados = {
        "nome": "Risco de Teste",
        "descricao": "Descricao do risco de teste",
        "tipo": "riscos_operacionais",
        "departamento": "departamento_1",
        "impacto": "Alto",
        "probabilidade": "Media",
        "nivel_de_risco": "Alto",
        "eficacia_dos_controles": "Media",
        "nivel_residual": "Medio",
    }
    dados.update(kwargs)
    return dados
