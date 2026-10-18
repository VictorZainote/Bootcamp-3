# Regras de Governança de Contexto para IA (`CONTEXT_RULES.md`)

Este documento define as diretrizes arquiteturais, restrições técnicas e regras de governança de Inteligência Artificial (AI Harness) para o desenvolvimento do sistema **TaskAnalyzer** sob a metodologia **Specification-Driven Development (SDD)**.

Qualquer assistente de IA (Gemini, ChatGPT, GitHub Copilot, Claude) utilizado para geração ou refatoração de código neste repositório **deve** obedecer estritamente às regras abaixo.

---

## 1. Ambiente Tecnológico e Dependências Autorizadas

1. **Versão da Linguagem:** O código deve ser compatível com **Python 3.11+**.
2. **Biblioteca Padrão:** A implementação em `src/task_analyzer.py` deve utilizar exclusivamente módulos da biblioteca padrão do Python (`datetime`, `typing`, etc.). **É proibido** importar bibliotecas externas não listadas em `requirements.txt` (ex.: `pandas`, `numpy`, `pydantic`, `arrow`) para a lógica de negócio.
3. **Framework de Testes:** A suíte de testes automatizados (`tests/test_harness.py`) deve ser implementada exclusivamente com `pytest`.

---

## 2. Padrões de Codificação e Tipagem Estática

1. **Type Hints Obrigatórios (100%):** Todas as funções, métodos, variáveis de assinatura e valores de retorno devem possuir anotações de tipo explícitas utilizando a sintaxe moderna do Python 3.11+ (ex.: `list[dict[str, Any]]`, `dict[str, Any]`, `float | int`).
2. **Docstrings Claras:** Todas as classes de exceção e funções públicas devem conter docstrings explicando objetivo, parâmetros (`Args`), retorno (`Returns`) e exceções disparadas (`Raises`).
3. **Nomenclatura Estrita:** Os nomes de arquivos, funções, exceções e chaves de dicionário devem respeitar literalmente o contrato definido em `specs/task_analyzer_spec.md`:
   - Módulo principal: `src/task_analyzer.py`
   - Função principal: `analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]`
   - Exceção customizada: `TaskValidationError(Exception)`
   - Chaves de saída:
     - `total_tarefas` (`int`)
     - `total_concluidas` (`int`)
     - `total_pendentes` (`int`)
     - `tempo_medio_conclusao_horas` (`dict[str, float]`) contendo as chaves `"geral"` e por prioridade (`"alta"`, `"media"`, `"baixa"`)
     - `taxa_atraso_percentual` (`float`)

---

## 3. Tratamento de Erros e Prevenção de Alucinações

1. **Proibição de Exceções Genéricas para Regras de Negócio:** Inconsistências nos dados de entrada das tarefas (como datas inválidas ou `data_conclusao < data_criacao`) **nunca** devem ser silenciadas ou lançar `ValueError`/`Exception` genéricos sem tratamento; devem obrigatoriamente disparar a exceção customizada `TaskValidationError`.
2. **Prevenção de Divisão por Zero (`ZeroDivisionError`):**
   - Caso a lista de tarefas esteja vazia (`[]`) ou nenhuma tarefa esteja concluída (`total_concluidas == 0`), todos os cálculos de média (`tempo_medio_conclusao_horas`) e percentual (`taxa_atraso_percentual`) devem retornar `0.0` de forma segura, sem lançar `ZeroDivisionError`.
   - Caso uma prioridade específica (`"alta"`, `"media"` ou `"baixa"`) não possua tarefas concluídas, sua respectiva média em `tempo_medio_conclusao_horas` deve ser `0.0`.
3. **Arredondamento Padronizado:** Valores de ponto flutuante (`tempo_medio_conclusao_horas` e `taxa_atraso_percentual`) devem ser arredondados para **2 casas decimais** (`round(valor, 2)`).
4. **Proibição de Invenção de Requisitos (Anti-Hallucination):** O assistente de IA não deve adicionar campos extras no dicionário de retorno, criar bancos de dados, APIs HTTP ou alterar o contrato de entrada/saída especificado em `specs/task_analyzer_spec.md`.

---

## 4. Homologação Humana e Test Harness

1. Nenhum código gerado por IA pode ser integrado à branch `main` sem passar com **100% de aprovação** na suíte `pytest` (`tests/test_harness.py`).
2. O fluxo de trabalho exige versionamento em branches de funcionalidade (`feature/*`), commits atômicos e revisão via Pull Request.
