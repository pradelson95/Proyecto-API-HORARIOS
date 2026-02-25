# ⏱ API de Controle de Jornada de Funcionários

API REST desenvolvida com FastAPI para gerenciamento e controle de horários de funcionários.  
O sistema permite registrar entrada e saída, aplicar validações de regras de negócio e realizar testes de carga para análise de desempenho.

---

## 🚀 Tecnologias Utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic v2
- Uvicorn
- Locust (Testes de carga)
- python-dotenv

---

## 📌 Objetivo do Projeto

Este projeto foi desenvolvido como parte de portfólio profissional com foco em:

- Desenvolvimento de APIs REST modernas
- Validação robusta de dados
- Integração com banco de dados relacional
- Testes de carga e análise de performance
- Preparação para ambiente de produção

---

## 📊 Funcionalidades

- CRUD completo de funcionários
- Registro de horário de entrada e saída
- Validações de regras de negócio
- Controle de jornada máxima de 8 horas
- Restrição de horário mínimo (não antes das 07:00)
- Prevenção de registros duplicados
- Configuração via variáveis de ambiente
- Estrutura preparada para deploy em produção

---

## 🔎 Validações Implementadas

### 🆔 id_identification
- Máximo de 6 dígitos
- Chave primária (não permite duplicados)

### 👤 full_name
- Comprimento mínimo e máximo
- Remoção automática de espaços extras
- Não pode estar vazio

### ⏰ check_in
- Não pode ser antes das 07:00

### ⏳ check_out
- Deve ser maior que o horário de entrada
- Jornada máxima permitida: 8 horas

---

## 🗄 Banco de Dados

O projeto utiliza PostgreSQL como banco principal.

Configuração através de variável de ambiente:


O uso de `.env` garante que credenciais não sejam expostas no repositório.


---

## 📡 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|------------|
| POST   | /employees | Criar funcionário |
| GET    | /employees | Listar funcionários |
| PUT    | /employees/{id} | Atualizar funcionário |
| DELETE | /employees/{id} | Remover funcionário |

---

## 🧪 Testes de Carga

Foram realizados testes utilizando Locust para simular múltiplos usuários concorrentes.

Exemplo de teste executado:

- 60 usuários
- Spawn rate: 5
- Duração: 3 minutos
- Migração de SQLite para PostgreSQL para melhorar concorrência

Projeto preparado para deploy em:

- Railway
- Render
- Servidor VPS com PostgreSQL

---

## 👨‍💻 Autor

Pradelson Francois  
Backend Developer | Python | FastAPI  

Projeto desenvolvido para demonstrar competências em:

- Arquitetura de APIs
- Validação de dados
- Integração com banco relacional
- Testes de carga
- Preparação para produção
