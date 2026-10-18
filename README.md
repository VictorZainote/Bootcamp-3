# TaskAnalyzer — Specification-Driven Development (SDD) & AI Harness

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/pytest-100%25%20passed-success)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

Repositório oficial do sistema **TaskAnalyzer**, desenvolvido durante o **Bootcamp III (CEUB — Entrega Intermediária / Fase 2)** aplicando a metodologia **Specification-Driven Development (SDD)**, governança de contexto para Inteligência Artificial (`CONTEXT_RULES.md`) e validação automatizada via **Test Harness (`pytest`)**.

---

## Sumário

1. [Estrutura do Repositório](#1-estrutura-do-repositório)
2. [Requisitos e Instruções de Execução](#2-requisitos-e-instruções-de-execução)
3. [Relatório Técnico da Fase 2 (SDD & Homologação de IA)](#3-relatório-técnico-da-fase-2-sdd--homologação-de-ia)
   - [3.1 Fluxo de Branches e Pull Requests](#31-fluxo-de-branches-e-pull-requests)
   - [3.2 Relato dos Prompts Utilizados](#32-relato-dos-prompts-utilizados)
   - [3.3 Como as `CONTEXT_RULES` Evitaram Alucinações da IA](#33-como-as-context_rules-evitaram-alucinações-da-ia)
4. [Evidências Comprobatórias (Prints)](#4-evidências-comprobatórias-prints)

---

## 1. Estrutura do Repositório

```text
sdd-task-analyzer/
├── README.md                   # Documentação geral, Relatório Técnico da Fase 2, prints e status do build
├── CONTEXT_RULES.md            # Regras de governança de IA transpostas da Fase 1
├── .gitignore                  # Arquivos/diretórios ignorados (__pycache__/, .pytest_cache/, venv/)
├── requirements.txt            # Dependências autorizadas (pytest, etc.)
├── specs/
│   └── task_analyzer_spec.md   # Especificação do contrato SDD transposta da Fase 1
├── tests/
│   └── test_harness.py         # Suíte de testes automatizados com pytest (Cenários 1, 2 e Borda)
├── src/
│   └── task_analyzer.py        # Código-fonte do sistema gerado via IA e homologado por humano
└── docs/
    └── screenshots/            # Prints comprobatórios de execução do pytest, árvore de arquivos e PRs
```

---

## 2. Requisitos e Instruções de Execução

1. Certifique-se de possuir o **Python 3.11+** instalado.
2. (Opcional) Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   ```
3. Instale as dependências autorizadas:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a suíte de testes automatizados (`pytest`):
   ```bash
   pytest -v tests/test_harness.py
   ```
   *(No Windows com Python Launcher: `py -m pytest -v tests/test_harness.py`)*

---

## 3. Relatório Técnico da Fase 2 (SDD & Homologação de IA)

### 3.1 Fluxo de Branches e Pull Requests
O desenvolvimento seguiu rigorosamente a estratégia de ramificação por funcionalidade (*Feature Branch Workflow*) com commits atômicos e homologação via Pull Requests para a branch `main`:

- **[PR #1 — `feature/sdd-specification`](https://github.com/VictorZainote/Bootcamp-3/pull/1):** Estruturação inicial (`.gitignore`, `requirements.txt`), regras de governança em [`CONTEXT_RULES.md`](./CONTEXT_RULES.md) e especificação do contrato executável em [`specs/task_analyzer_spec.md`](./specs/task_analyzer_spec.md).
- **[PR #2 — `feature/task-analyzer-impl`](https://github.com/VictorZainote/Bootcamp-3/pull/2):** Implementação assistida por IA do módulo [`src/task_analyzer.py`](./src/task_analyzer.py) contendo a função `analyze_tasks` e a exceção customizada `TaskValidationError`.
- **[PR #3 — `feature/test-harness`](https://github.com/VictorZainote/Bootcamp-3/pull/3):** Implementação da suíte de testes automatizados em [`tests/test_harness.py`](./tests/test_harness.py) validando os Cenários 1, 2 e casos de borda com 100% de aprovação.

---

### 3.2 Relato dos Prompts Utilizados

Durante a Fase 2, os arquivos [`CONTEXT_RULES.md`](./CONTEXT_RULES.md) e [`specs/task_analyzer_spec.md`](./specs/task_analyzer_spec.md) foram fornecidos integralmente como contexto de sistema ao assistente de IA antes da geração de código:

1. **Prompt 1 — Geração do Módulo `src/task_analyzer.py`:**
   > *"Atue como engenheiro de software Python 3.11+. Utilizando estritamente as regras de governança definidas em `CONTEXT_RULES.md` e o contrato técnico executável em `specs/task_analyzer_spec.md`, implemente o módulo `src/task_analyzer.py` contendo a exceção customizada `TaskValidationError` e a função `analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]`. Garanta 100% de cobertura de Type Hints, uso exclusivo da biblioteca padrão do Python, validação temporal (`data_conclusao < data_criacao` disparando `TaskValidationError`) e prevenção total contra `ZeroDivisionError` retornando `0.0` quando não houver tarefas concluídas."*

2. **Prompt 2 — Geração do Test Harness `tests/test_harness.py`:**
   > *"Com base nos Cenários de Aceite (Dado-Quando-Então) definidos em `specs/task_analyzer_spec.md`, implemente a suíte de testes automatizados em `tests/test_harness.py` utilizando `pytest`. Cubra integralmente: (1) Cenário 1 de sucesso validando `total_tarefas`, `total_concluidas`, `total_pendentes`, `tempo_medio_conclusao_horas` (geral e por prioridade: alta, media, baixa) e `taxa_atraso_percentual`; (2) Cenário 2 de erro validando o disparo de `TaskValidationError` para datas inconsistentes (`data_conclusao < data_criacao`); e (3) Casos de borda com lista vazia e apenas tarefas pendentes."*

---

### 3.3 Como as `CONTEXT_RULES` Evitaram Alucinações da IA

A presença do arquivo [`CONTEXT_RULES.md`](./CONTEXT_RULES.md) funcionou como um *AI Harness* determinístico, impedindo desvios arquiteturais e alucinações comuns em modelos de linguagem:

1. **Bloqueio de Dependências Externas Não Autorizadas:** Sem restrições explícitas, assistentes de IA frequentemente importam bibliotecas externas como `pandas`, `numpy` ou `python-dateutil` para manipular datas e calcular médias. As `CONTEXT_RULES` restringiram a implementação exclusivamente à biblioteca padrão do Python 3.11+ (`datetime.fromisoformat`, `typing`).
2. **Aderência Literal ao Contrato de Entrada/Saída (Anti-Hallucination):** Impediu que a IA inventasse nomes de chaves em inglês (ex.: `average_completion_time`) ou omitisse chaves de prioridades sem tarefas concluídas. O dicionário retornado respeita exatamente as chaves `total_tarefas`, `total_concluidas`, `total_pendentes`, `tempo_medio_conclusao_horas` (`geral`, `alta`, `media`, `baixa`) e `taxa_atraso_percentual`.
3. **Tratamento de Erros de Domínio (`TaskValidationError`):** Evitou que datas inconsistentes (`data_conclusao < data_criacao`) retornassem durações negativas silenciosamente ou disparassem exceções genéricas (`ValueError`), garantindo o lançamento da exceção específica `TaskValidationError`.
4. **Prevenção Determinística de `ZeroDivisionError`:** Forçou a verificação explícita do denominador antes do cálculo das médias gerais, por prioridade e da taxa de atraso, garantindo retorno seguro de `0.0` para listas vazias ou apenas com tarefas pendentes.

---

## 4. Evidências Comprobatórias (Prints)

### 4.1 Execução e Aprovação dos Testes Automatizados com `pytest` (100% Passed)
![Execução do Pytest no Terminal](./docs/screenshots/1_pytest_terminal.png)

---

### 4.2 Árvore de Arquivos do Repositório no GitHub
![Árvore de Arquivos no GitHub](./docs/screenshots/2_github_arvore_arquivos.png)

---

### 4.3 Fluxo de Pull Requests Abertos e Homologados (Merged) no GitHub
![Pull Requests no GitHub](./docs/screenshots/3_github_pull_requests.png)
