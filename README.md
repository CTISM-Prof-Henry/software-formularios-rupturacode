# software-formularios-rupturacode

Descrição curta do repositório.

## Sumário

* [Pré-requisitos](#pré-requisitos)
* [Instalação](#instalação)
* [Instruções de uso](#instruções-de-uso)
* [Contato](#contato)
* [Bibliografia](#bibliografia)

## Pré-requisitos

Descreva aqui brevemente os pré-requisitos necessários para executar o código-fonte. Descreva também
a configuração mínima da máquina em que o código foi desenvolvido, e se alguma configuração em particular é essencial
para sua execução (por exemplo, placa de vídeo dedicada):

| Configuração        | Valor                    |
|---------------------|--------------------------|
| Sistema operacional | Windows 10 Pro (64 bits) |
| Processador         | Intel core i7 9700       |
| Memória RAM         | 16GB                     |
| Necessita rede?     | Sim                      |


## Instalação

Descreva aqui as instruções para instalação das ferramentas para execução do código-fonte: 

```bash
sudo apt-get install nano
```

## Instruções de Uso

Descreva aqui o passo-a-passo que outros usuários precisam realizar para conseguir executar com sucesso o código-fonte
deste projeto:

```bash
echo "olá mundo!"
```

## Contato

O repositório foi originalmente desenvolvido por Fulano: [fulano@ufsm.br]()

## Bibliografia

Adicione aqui entradas numa lista com a documentação pertinente:

* [Documentação coplin-db2](https://pypi.org/project/coplin-db2/)


# Diagrama Entidade-Relacionamento

```mermaid
    erDiagram
        USUARIO {
        int id
        string nome
        string matricula
        string senha
        boolean is_admin
        int fk_departamento
    }

    DEPARTAMENTO {
        int id
        string nome
    }

    RISCO {
        int id
        string titulo
        string tipo
        int impacto
        int probabilidade
        string descricao
        int nivel_risco
        string eficacia_controle
        int nivel_residual
        datetime data_criacao
        int fk_usuario
        int fk_departamento
    }

    TRATAMENTO {
        int id
        string resposta
        string acao
        string descricao
        string situacao
        datetime data_inicio
        datetime data_fim
        datetime data_criacao
        int fk_risco
        int fk_usuario
    }

    SETORES {
        int id
        string nome
        int fk_departamento
    }

    %% RELACIONAMENTOS
    DEPARTAMENTO ||--o{ USUARIO : possui
    USUARIO ||--o{ RISCO : cria
    DEPARTAMENTO ||--o{ RISCO : associado
    RISCO ||--o{ TRATAMENTO : possui
    DEPARTAMENTO ||--o{ SETORES : associado
    SETORES ||--o{ SETORES : subSetor
```


# Diagrama de caso de uso



# Diagrama de classes

```mermaid
classDiagram
    class Usuario
    class Departamento
    class Risco
    class Tratamento
    class Setores

    Usuario : -int id
    Usuario : -string nome
    Usuario : -string matricula
    Usuario : -string senha
    Usuario : -boolean is_admin
    Usuario : -int fk_departamento

    Usuario : +autenticar()
    Usuario : +criarUsuario()
    Usuario : +editarUsuario()
    Usuario : +listarUsuarios()
    Usuario : +detalhesUsuario()
    Usuario : +desativarUsuario()

    Departamento : -int id
    Departamento : -string nome

    Departamento : +criarDepartamento()
    Departamento : +listarDepartamentos()
    Departamento : +editarDepartamento()
    Departamento : +detalhesDepartamento()
    Departamento : +desativarDepartamento()
    Departamento : +designarDepartamento()

    Risco : -int id
    Risco : -string titulo
    Risco : -string tipo
    Risco : -int impacto
    Risco : -int probabilidade
    Risco : -string descricao
    Risco : -int nivel_risco
    Risco : -string eficacia_controle
    Risco : -int nivel_residual
    Risco : -datetime data_criacao
    Risco : -int fk_departamento
    Risco : -int fk_usuario

    Risco : +criarRisco()
    Risco : +editarRisco()
    Risco : +desativarRisco()
    Risco : +listarRiscos()
    Risco : +detalhesRisco()
    Risco : +calcularNivelRisco()
    Risco : +avaliarImpacto()

    Tratamento : -int id
    Tratamento : -string resposta
    Tratamento : -string acao
    Tratamento : -string descricao
    Tratamento : -string situacao
    Tratamento : -datetime data_inicio
    Tratamento : -datetime data_fim
    Tratamento : -datetime data_criacao
    Tratamento : -int fk_risco
    Tratamento : -int fk_usuario

    Tratamento : +criarTratamento()
    Tratamento : +editarTratamento()
    Tratamento : +listarTratamentos()
    Tratamento : +desativarTratamento()
    Tratamento : +detalhesTratamento()

    Setores : -int id
    Setores : -string nome
    Setores : -int fk_departamento

    Setores : +criarSetor()
    Setores : +editarSetor()
    Setores : +desativarSetor()
    Setores : +listarSetores()
    Setores : +detalhesSetor()
    Setores : +criarSubSetor()

    Usuario "1" --> "0..*" Departamento
    Departamento "1" --> "0..*" Usuario

    Risco --> Departamento : associado
    Risco "1" --> "0..*" Tratamento
    Tratamento --> Risco

    Usuario --> Risco : identifica

    Departamento "1" -- "0..*" Setores : associado
    Setores "1" -- "0..*" Setores : subSetor
```
