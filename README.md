# TaskAnalyzer — Specification-Driven Development (SDD) & AI Harness

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/pytest-100%25%20passed-success)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

Repositório oficial do sistema **TaskAnalyzer**, desenvolvido durante o **Bootcamp III (CEUB)** aplicando a metodologia **Specification-Driven Development (SDD)**, governança de contexto para Inteligência Artificial (`CONTEXT_RULES.md`) e validação automatizada via **Test Harness (`pytest`)**.

---

## Estrutura do Projeto

```text
sdd-task-analyzer/
├── README.md                   # Documentação geral do projeto, instruções de execução e status do build
├── CONTEXT_RULES.md            # Regras de governança de IA transpostas da Fase 1
├── .gitignore                  # Arquivos/diretórios ignorados (__pycache__/, .pytest_cache/, venv/)
├── requirements.txt            # Dependências autorizadas (pytest, etc.)
├── specs/
│   └── task_analyzer_spec.md   # Especificação do contrato SDD transposta da Fase 1
├── tests/
│   └── test_harness.py         # Suíte de testes automatizados com pytest (Cenários 1, 2 e Borda)
└── src/
    └── task_analyzer.py        # Código-fonte do sistema gerado via IA e homologado por humano
```

---

## Requisitos e Instalação

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

---

## Como Executar o Test Harness (`pytest`)

Para executar a suíte de testes automatizados que valida o contrato SDD:

```bash
pytest -v tests/test_harness.py
```

*(No Windows com Python Launcher, você também pode executar `py -m pytest -v tests/test_harness.py`)*

### Cenários Validados pela Suíte
- **Cenário 1 (Sucesso):** Validação exata de `total_tarefas`, `total_concluidas`, `total_pendentes`, `tempo_medio_conclusao_horas` (`geral`, `alta`, `media`, `baixa`) e `taxa_atraso_percentual`.
- **Cenário 2 (Exceção/Erro):** Validação de datas inconsistentes (`data_conclusao < data_criacao`) e tarefas concluídas incompletas disparando `TaskValidationError`.
- **Casos de Borda:** Listas vazias (`[]`) ou contendo apenas tarefas pendentes retornando `0.0` nas médias e percentuais, prevenindo `ZeroDivisionError`.

---

## Governança de IA e Homologação

Todo o código em `src/task_analyzer.py` foi gerado seguindo estritamente:
- [`CONTEXT_RULES.md`](./CONTEXT_RULES.md): Regras de governança para assistentes de IA (100% de *type hints*, biblioteca padrão do Python 3.11+, proibição de alucinações e prevenção de divisão por zero).
- [`specs/task_analyzer_spec.md`](./specs/task_analyzer_spec.md): Contrato técnico executável SDD e cenários BDD (Dado-Quando-Então).
