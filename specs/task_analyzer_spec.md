# Especificação Técnica Executável — Sistema `TaskAnalyzer` (SDD)

## 1. Visão Geral do Contrato de Negócio

O módulo `src/task_analyzer.py` é responsável por processar uma coleção de tarefas operacionais e calcular indicadores de desempenho (KPIs) de produtividade, tempo médio de conclusão (geral e segmentado por prioridade) e taxa de atraso percentual, validando rigorosamente a integridade temporal dos registros.

---

## 2. Assinaturas e Componentes Obrigatórios

### 2.1 Exceção Customizada: `TaskValidationError`
```python
class TaskValidationError(Exception):
    """Exceção lançada quando uma tarefa apresenta dados inconsistentes ou inválidos."""
```

### 2.2 Função Principal: `analyze_tasks`
```python
def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
```

---

## 3. Contrato de Entrada (`tasks`)

A função `analyze_tasks` recebe uma lista de dicionários (`list[dict[str, Any]]`). Cada dicionário representa uma tarefa com a seguinte estrutura:

| Campo | Tipo Aceito | Obrigatório | Descrição |
| :--- | :--- | :---: | :--- |
| `id` | `int \| str` | Sim | Identificador único da tarefa |
| `titulo` | `str` | Não | Título ou descrição da tarefa |
| `prioridade` | `str` | Sim | Prioridade da tarefa: `"alta"`, `"media"` ou `"baixa"` (case-insensitive) |
| `status` | `str` | Sim | Estado da tarefa: `"concluida"` ou `"pendente"` (case-insensitive, aceita `"concluída"`) |
| `data_criacao` | `str \| datetime` | Sim | Data/hora de criação no formato ISO 8601 (`"YYYY-MM-DDTHH:MM:SS"` ou `"YYYY-MM-DD HH:MM:SS"`) ou objeto `datetime` |
| `data_conclusao` | `str \| datetime \| None` | Condicional | Obrigatório quando `status == "concluida"`. `None` quando `"pendente"` |
| `prazo_estimado_horas` | `float \| int \| None` | Condicional | Limite de horas estimado para conclusão (opcional; se ausente, usa `data_prazo`) |
| `data_prazo` | `str \| datetime \| None` | Condicional | Data/hora limite (deadline) da tarefa (opcional; alternativa ou complemento a `prazo_estimado_horas`) |
| `entregue_Com_atraso` / `atrasada` | `bool \| None` | Não | Flag explícita opcional indicando atraso |

### Regras de Determinação de Atraso (em tarefas concluídas)
Uma tarefa concluída é contabilizada como **atrasada** se satisfizer qualquer uma das condições abaixo:
1. Possuir `data_prazo` (deadline) definida e `data_conclusao > data_prazo`; **OU**
2. Possuir `prazo_estimado_horas` definido e a duração em horas `(data_conclusao - data_criacao) > prazo_estimado_horas`; **OU**
3. Possuir a flag booleana `atrasada=True`.

---

## 4. Contrato de Saída (Retorno)

A função deve retornar um dicionário Python contendo exatamente a estrutura abaixo:

```python
{
    "total_tarefas": int,
    "total_concluidas": int,
    "total_pendentes": int,
    "tempo_medio_conclusao_horas": {
        "geral": float,
        "alta": float,
        "media": float,
        "baixa": float,
    },
    "taxa_atraso_percentual": float,
}
```

### Fórmulas de Cálculo
- **`total_tarefas`**: Quantidade total de tarefas recebidas na lista (`len(tasks)`).
- **`total_concluidas`**: Quantidade de tarefas com `status == "concluida"`.
- **`total_pendentes`**: Quantidade de tarefas com `status == "pendente"`.
- **Duração de uma tarefa concluída (em horas)**:
  $$\text{duracao\_horas} = \frac{(\text{data\_conclusao} - \text{data\_criacao}).\text{total\_seconds}()}{3600}$$
- **`tempo_medio_conclusao_horas["geral"]`**: Soma das durações (em horas) de todas as tarefas concluídas dividida por `total_concluidas` (arredondado em 2 casas decimais). Se `total_concluidas == 0`, retorna `0.0`.
- **`tempo_medio_conclusao_horas[prioridade]`**: Média das durações (em horas) das tarefas concluídas daquela prioridade específica (`"alta"`, `"media"`, `"baixa"`), arredondada em 2 casas decimais. Se não houver tarefas concluídas na prioridade, retorna `0.0`.
- **`taxa_atraso_percentual`**:
  $$\text{taxa\_atraso\_percentual} = \text{round}\left(\left(\frac{\text{tarefas\_concluidas\_com\_atraso}}{\text{total\_concluidas}}\right) \times 100, 2\right)$$
  Se `total_concluidas == 0`, retorna `0.0`.

---

## 5. Regras de Validação e Exceções (`TaskValidationError`)

A função deve lançar `TaskValidationError` nos seguintes casos:
1. **Inconsistência Temporal (Regra Principal):** `data_conclusao < data_criacao` (data de conclusão anterior à data de criação).
2. **Tarefa concluída sem data de conclusão:** `status == "concluida"` e `data_conclusao` ausente ou `None`.
3. **Datas em formato inválido:** Strings de data que não sigam o padrão ISO 8601.
4. **Status ou Prioridade inválidos:** Valores fora do domínio permitido (`status` fora de `{"concluida", "pendente"}` ou `prioridade` fora de `{"alta", "media", "baixa"}`).

---

## 6. Cenários de Aceite (BDD / Dado-Quando-Então)

### Cenário 1: Sucesso no Cálculo de Métricas e Indicadores
- **DADO** um conjunto válido de tarefas contendo tarefas concluídas (de prioridades `"alta"`, `"media"` e `"baixa"`, com e sem atraso) e tarefas pendentes;
- **QUANDO** a função `analyze_tasks(tasks)` for executada;
- **ENTÃO** o sistema deve retornar os contadores exatos (`total_tarefas`, `total_concluidas`, `total_pendentes`), o `tempo_medio_conclusao_horas` (`"geral"`, `"alta"`, `"media"`, `"baixa"`) e a `taxa_atraso_percentual` devidamente calculados e arredondados em 2 casas decimais.

### Cenário 2: Falha de Validação por Datas Inconsistentes
- **DADO** uma lista de tarefas onde pelo menos uma tarefa possui `data_conclusao` anterior à `data_criacao` (`data_conclusao < data_criacao`);
- **QUANDO** a função `analyze_tasks(tasks)` for invocada;
- **ENTÃO** o sistema deve interromper o processamento imediatamente e disparar a exceção customizada `TaskValidationError`.

### Cenário 3: Casos de Borda (Lista Vazia ou Apenas Tarefas Pendentes)
- **DADO** uma lista de tarefas vazia (`[]`) ou uma lista contendo exclusivamente tarefas com `status == "pendente"`;
- **QUANDO** a função `analyze_tasks(tasks)` for executada;
- **ENTÃO** o sistema não deve lançar `ZeroDivisionError` e deve retornar `0.0` para todas as médias em `tempo_medio_conclusao_horas` e `0.0` para `taxa_atraso_percentual`.
