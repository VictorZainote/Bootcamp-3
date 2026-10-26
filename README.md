# TaskAnalyzer — SDD, CI/CD, Docker & Governança Ética de IA (Bootcamp III)

![TaskAnalyzer CI/CD Pipeline](https://github.com/VictorZainote/Bootcamp-3/actions/workflows/ci.yml/badge.svg)
![Tests](https://img.shields.io/badge/pytest-100%25%20passed-success)
![Docker](https://img.shields.io/badge/docker-python%3A3.11--slim-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)

Repositório oficial do sistema **TaskAnalyzer** (`sdd-task-analyzer`), desenvolvido ao longo das **Fases 1, 2 e 3 do Bootcamp III (CEUB)** aplicando a metodologia **Specification-Driven Development (SDD)**, governança determinística de Inteligência Artificial ([`CONTEXT_RULES.md`](./CONTEXT_RULES.md)), validação automatizada com **Test Harness (`pytest`)**, **Integração Contínua (GitHub Actions)**, **Containerização Isolada (`Docker` & `Docker Compose`)** e **Auditoria Ética (`Critical-in-the-Loop`)**.

---

## Sumário

1. [Arquitetura Final do Repositório](#1-arquitetura-final-do-repositório)
2. [Pilar 1: Motor de Integração Contínua (CI/CD — GitHub Actions)](#2-pilar-1-motor-de-integração-contínua-cicd--github-actions)
3. [Pilar 2: Containerização e Orquestração Isolada (Docker & Compose)](#3-pilar-2-containerização-e-orquestração-isolada-docker--compose)
4. [Execução Local (Ambiente Python 3.11+)](#4-execução-local-ambiente-python-311)
5. [Pilar 3: Relatório Técnico de Governança e Ética de IA (Fase 3)](#5-pilar-3-relatório-técnico-de-governança-e-ética-de-ia-fase-3)
6. [Histórico da Fase 2 e Evidências Comprobatórias (Prints)](#6-histórico-da-fase-2-e-evidências-comprobatórias-prints)

---

## 1. Arquitetura Final do Repositório

```text
sdd-task-analyzer/
├── .github/
│   └── workflows/
│       └── ci.yml                      # Motor CI/CD (GitHub Actions - Python 3.11 + pytest)
├── Dockerfile                          # Empacotamento em imagem imutável (python:3.11-slim)
├── docker-compose.yml                  # Orquestração isolada da suíte de testes (docker compose run)
├── CONTEXT_RULES.md                    # Base de Governança e regras anti-alucinação (Fase 1)
├── specs/
│   ├── system_design_document.pdf      # System Design Document (SDD) formal em PDF (Fase 1)
│   ├── requirements.yaml               # Contrato declarativo de requisitos, regras e SLAs (Fase 1)
│   └── task_analyzer_spec.md           # Especificação técnica executável e cenários BDD
├── tests/
│   └── test_harness.py                 # Suíte de testes automatizados pytest (Fase 2 - 100% Passed)
├── src/
│   └── task_analyzer.py                # Código-fonte gerado via IA e homologado por humano (Fase 2)
├── requirements.txt                    # Dependências autorizadas (pytest>=8.0.0)
└── README.md                           # Documentação geral, instruções de execução e Governança de IA
```

---

## 2. Pilar 1: Motor de Integração Contínua (CI/CD — GitHub Actions)

O pipeline de Integração Contínua está definido em [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) e garante que nenhum código fora do contrato SDD seja integrado:

- **Gatilhos (`on`):** Disparo automático em eventos de `push` ou `pull_request` nas branches `main` e `develop`.
- **Ambiente:** Sistema `ubuntu-latest` com **Python 3.11** (`actions/setup-python@v5`).
- **Preparação:** Instalação das dependências homologadas via `pip install -r requirements.txt`.
- **Execução:** Comando padronizado da suíte de testes:
  ```bash
  pytest tests/test_harness.py -v
  ```

---

## 3. Pilar 2: Containerização e Orquestração Isolada (Docker & Compose)

Para eliminar definitivamente o problema *"na minha máquina funciona"*, o projeto utiliza empacotamento isolado via [`Dockerfile`](./Dockerfile) (baseado na imagem oficial leve e imutável `python:3.11-slim`) e orquestração via [`docker-compose.yml`](./docker-compose.yml).

### 3.1 Executando com Docker Compose (Comando Único)
```bash
docker compose run --rm task-analyzer
```

### 3.2 Construindo e Executando com Docker CLI
```bash
# 1. Constrói a imagem isolada
docker build -t sdd-task-analyzer .

# 2. Executa o container disparando automaticamente o pytest
docker run --rm sdd-task-analyzer
```

---

## 4. Execução Local (Ambiente Python 3.11+)

1. Crie e ative um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   # Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   ```
2. Instale as dependências autorizadas:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a suíte de testes automatizados (`pytest`):
   ```bash
   pytest tests/test_harness.py -v
   ```

---

## 5. Pilar 3: Relatório Técnico de Governança e Ética de IA (Fase 3)

### 5.1 Análise de Alucinações: Bloqueio via `CONTEXT_RULES.md` e SDD
A combinação do contrato executável ([`specs/system_design_document.pdf`](./specs/system_design_document.pdf), [`specs/requirements.yaml`](./specs/requirements.yaml) e [`specs/task_analyzer_spec.md`](./specs/task_analyzer_spec.md)) com as diretrizes restritivas de [`CONTEXT_RULES.md`](./CONTEXT_RULES.md) funcionou como um firewall determinístico contra desvios arquiteturais e alucinações de modelos de linguagem:

1. **Bloqueio de Bibliotecas Não Autorizadas:** Sem restrições explícitas, assistentes de IA frequentemente importam pacotes externos como `pandas`, `numpy`, `pydantic` ou `python-dateutil`. As regras de contexto restringiram a implementação em [`src/task_analyzer.py`](./src/task_analyzer.py) exclusivamente à biblioteca padrão do Python 3.11+ (`datetime.fromisoformat`, `typing`).
2. **Aderência Estrita ao Contrato de Negócio:** Impediu a invenção de chaves fora da especificação ou a omissão de prioridades sem tarefas concluídas, garantindo que o dicionário retornado contenha sempre `total_tarefas`, `total_concluidas`, `total_pendentes`, `tempo_medio_conclusao_horas` (`geral`, `alta`, `media`, `baixa`) e `taxa_atraso_percentual` arredondados em 2 casas decimais.
3. **Exceção de Domínio (`TaskValidationError`):** Evitou que datas inconsistentes (`data_conclusao < data_criacao`) gerassem durações negativas silenciosas ou lançassem `ValueError` genérico, impondo o disparo da exceção customizada `TaskValidationError`.

### 5.2 Homologação Humana: O Modelo `Critical-in-the-Loop` na Prática
O engenheiro atuou como filtro primário e homologador crítico (*Critical-in-the-Loop*) ao longo de 4 etapas:
1. **Geração:** O agente de IA propôs a implementação central de análise de tarefas subordinada ao SDD.
2. **Barreira SDD:** O código passou pela verificação de contrato executável, tipagem estática (100% *Type Hints*) e pureza de dependências.
3. **Validação Humana (QA Crítico):** Auditoria ativa de casos críticos de negócio e borda:
   - **Prevenção de `ZeroDivisionError`:** Proteção explícita no cálculo de médias (geral e por prioridade) e taxa de atraso, retornando `0.0` de forma segura para listas vazias (`[]`) ou quando `total_concluidas == 0`.
   - **Validação de Anomalias Temporais:** Garantia de interrupção imediata com `TaskValidationError` sempre que `data_conclusao < data_criacao` ou quando `status == "concluida"` não possui `data_conclusao`.
4. **Integração Segura:** Incorporação final em [`src/task_analyzer.py`](./src/task_analyzer.py) auditada automaticamente pela suíte [`tests/test_harness.py`](./tests/test_harness.py) via GitHub Actions e container Docker.

### 5.3 Sustentabilidade, Ética e Rastreabilidade de Prompts
1. **Prompt 1 — Geração do Módulo `src/task_analyzer.py`:**
   > *"Atue como engenheiro de software Python 3.11+. Utilizando estritamente as regras de governança definidas em `CONTEXT_RULES.md` e o contrato técnico executável em `specs/task_analyzer_spec.md`, implemente o módulo `src/task_analyzer.py` contendo a exceção customizada `TaskValidationError` e a função `analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]`. Garanta 100% de cobertura de Type Hints, uso exclusivo da biblioteca padrão do Python, validação temporal (`data_conclusao < data_criacao` disparando `TaskValidationError`) e prevenção total contra `ZeroDivisionError` retornando `0.0` quando não houver tarefas concluídas."*
2. **Prompt 2 — Geração do Test Harness `tests/test_harness.py`:**
   > *"Com base nos Cenários de Aceite (Dado-Quando-Então) definidos em `specs/task_analyzer_spec.md`, implemente a suíte de testes automatizados em `tests/test_harness.py` utilizando `pytest`. Cubra integralmente: (1) Cenário 1 de sucesso validando `total_tarefas`, `total_concluidas`, `total_pendentes`, `tempo_medio_conclusao_horas` (geral e por prioridade: alta, media, baixa) e `taxa_atraso_percentual`; (2) Cenário 2 de erro validando o disparo de `TaskValidationError` para datas inconsistentes (`data_conclusao < data_criacao`); e (3) Casos de borda com lista vazia, apenas tarefas pendentes e validações de domínio."*
3. **Prompt 3 — Esteira CI/CD e Orquestração Docker (Fase 3):**
   > *"Seguindo a arquitetura final do repositório `sdd-task-analyzer`, configure o pipeline `.github/workflows/ci.yml` (gatilhos `push` e `pull_request` em `main` e `develop`, `ubuntu-latest` com Python 3.11 executando `pytest tests/test_harness.py -v`) e os arquivos `Dockerfile` (`python:3.11-slim`) e `docker-compose.yml` para execução isolada da suíte de testes."*

---

## 6. Histórico da Fase 2 e Evidências Comprobatórias (Prints)

### 6.1 Execução e Aprovação dos Testes Automatizados com `pytest` (100% Passed)
![Execução do Pytest no Terminal](./docs/screenshots/1_pytest_terminal.png)

### 6.2 Árvore de Arquivos do Repositório no GitHub
![Árvore de Arquivos no GitHub](./docs/screenshots/2_github_arvore_arquivos.png)

### 6.3 Fluxo de Pull Requests Abertos e Homologados (Merged) no GitHub
![Pull Requests no GitHub](./docs/screenshots/3_github_pull_requests.png)
