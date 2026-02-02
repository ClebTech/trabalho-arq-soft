# Locadora DSC

Este é o módulo de gerenciamento de locação de veículos. O sistema utiliza uma arquitetura distribuída com Flask e MySQL para gerenciar usuários, clientes, veículos e contratos de aluguel.

## Sobre o Projeto

Este sistema trata-se de uma refatoração e migração do projeto **[Locadora DSC](https://github.com/WallanMelo/Desenvolvimento-De-Sistemas-Corporativos-DSC-)**, originalmente escrito em Java.

**Principais Mudanças:**
* **Tecnologia:** Migração de Java para Python/Flask com foco em alta disponibilidade.
* **Arquitetura:** Implementação do padrão *Application Factory* e *Blueprints*.
* **Banco de Dados:** Uso de MySQL para persistência robusta.


---

## Como Rodar o Projeto

Você pode executar o projeto usando o gerenciador de pacotes padrão (`pip/venv`):

### 1: Configuração do Ambiente

1. Clonar o repositório.
2. Acessar o diretório do projeto:
```bash
cd trabalho-arq-soft
```
3. Criar o ambiente virtual Python:
```bash
python3 -m venv .venv
```
4. Ativar o ambiente virtual:
*  `source .venv/bin/activate`
5. Instalar as dependências:
```bash
pip install -r requirements.txt
```


---

## Configuração da Infraestrutura

Diferente da versão original, utilizamos scripts personalizados para garantir que o banco de dados MySQL reflita exatamente o *models.py*.

1. Configuração da URI:
```bash
Certifique-se de que a senha do MySQL no arquivo app/__init__.py está correta para o seu ambiente local.
```
2. Criação e População do Banco:
*Execute o script de seed para criar as tabelas e inserir os dados iniciais de teste (Admin, Veículos e Clientes):*
```bash
python seed.py
```


---

## Executando a Aplicação

1. Inicie o servidor:
```bash
python run.py
```
2. Acesse no navegador: http://127.0.0.1:5000/

---

### Estrutura do Projeto

* `app/`: Pasta principal contendo o código fonte.
* `app/auth/, app/clientes/, app/alugueis/`: Módulos separados por Blueprints.
* `app/templates/`: Arquivos HTML organizados por módulos (Jinja2).
* `app/models.py`: Definição das tabelas MySQL (Usuario, Cliente, Veiculo, Aluguel).
* `seed.py`: Script de infraestrutura para reset e carga inicial de dados.
* `requirements.txt`: Lista de dependências do projeto.

## 👥 Equipe

| Integrante | Funções Principais | GitHub |
| :--- | :--- | :--- |
| **Geovana Rodrigues** | Arquitetura Modular, Modelagem de Dados, Automação de Ambiente e Persistência e Status | [@murphiie](https://github.com/murphiie) |
| **Clebson Santos** | Regras de Negócio, Gestão Operacional, Fluxo Financeiro e Relatórios e Inteligência | [@ClebTech](https://github.com/ClebTech) |


