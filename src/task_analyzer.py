"""Módulo principal do sistema TaskAnalyzer.

Implementado sob a metodologia Specification-Driven Development (SDD) e governado
pelas diretrizes de CONTEXT_RULES.md.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class TaskValidationError(Exception):
    """Exceção customizada lançada quando uma tarefa possui dados inconsistentes ou inválidos."""


def _parse_datetime(value: str | datetime, field_name: str, task_id: Any) -> datetime:
    """Converte um valor string ISO 8601 ou objeto datetime em datetime validado.

    Args:
        value: Data em string ISO 8601 ou objeto datetime.
        field_name: Nome do campo sendo validado para mensagem de erro.
        task_id: Identificador da tarefa para rastreabilidade.

    Returns:
        Objeto datetime correspondente.

    Raises:
        TaskValidationError: Se o valor for nulo, de tipo inválido ou formato ISO inválido.
    """
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str) or not value.strip():
        raise TaskValidationError(
            f"Tarefa '{task_id}': campo '{field_name}' deve ser uma string ISO 8601 ou datetime válido."
        )
    try:
        return datetime.fromisoformat(value.strip())
    except ValueError as exc:
        raise TaskValidationError(
            f"Tarefa '{task_id}': formato de data inválido em '{field_name}': '{value}'."
        ) from exc


def _normalize_priority(priority: Any, task_id: Any) -> str:
    """Normaliza e valida o campo de prioridade da tarefa.

    Args:
        priority: Valor bruto de prioridade recebido no dicionário.
        task_id: Identificador da tarefa.

    Returns:
        String normalizada ('alta', 'media' ou 'baixa').

    Raises:
        TaskValidationError: Se a prioridade não pertencer ao domínio permitido.
    """
    if not isinstance(priority, str):
        raise TaskValidationError(
            f"Tarefa '{task_id}': prioridade inválida '{priority}'. Valores aceitos: alta, media, baixa."
        )
    normalized: str = (
        priority.strip()
        .lower()
        .replace("é", "e")
    )
    if normalized not in {"alta", "media", "baixa"}:
        raise TaskValidationError(
            f"Tarefa '{task_id}': prioridade desconhecida '{priority}'. Valores aceitos: alta, media, baixa."
        )
    return normalized


def _normalize_status(status: Any, task_id: Any) -> str:
    """Normaliza e valida o campo de status da tarefa.

    Args:
        status: Valor bruto de status recebido no dicionário.
        task_id: Identificador da tarefa.

    Returns:
        String normalizada ('concluida' ou 'pendente').

    Raises:
        TaskValidationError: Se o status não pertencer ao domínio permitido.
    """
    if not isinstance(status, str):
        raise TaskValidationError(
            f"Tarefa '{task_id}': status inválido '{status}'. Valores aceitos: concluida, pendente."
        )
    normalized: str = (
        status.strip()
        .lower()
        .replace("í", "i")
    )
    if normalized not in {"concluida", "pendente"}:
        raise TaskValidationError(
            f"Tarefa '{task_id}': status desconhecido '{status}'. Valores aceitos: concluida, pendente."
        )
    return normalized


def _is_task_delayed(
    task: dict[str, Any],
    data_criacao: datetime,
    data_conclusao: datetime,
    duration_hours: float,
    task_id: Any,
) -> bool:
    """Verifica se uma tarefa concluída foi entregue com atraso.

    Suporta verificação via:
    1. 'data_prazo' (deadline em ISO 8601 ou datetime): atrasada se data_conclusao > data_prazo.
    2. 'prazo_estimado_horas' ou 'prazo_horas' (float | int): atrasada se duration_hours > prazo.
    3. Flag booleana explícita 'atrasada' ou 'entregue_com_atraso'.

    Args:
        task: Dicionário original da tarefa.
        data_criacao: Data/hora de criação já validada.
        data_conclusao: Data/hora de conclusão já validada.
        duration_hours: Duração calculada em horas.
        task_id: Identificador da tarefa.

    Returns:
        True se a tarefa foi concluída com atraso, False caso contrário.

    Raises:
        TaskValidationError: Se os campos de prazo contiverem valores inválidos.
    """
    if task.get("atrasada") is True or task.get("entregue_com_atraso") is True:
        return True

    data_prazo_raw: Any = task.get("data_prazo") or task.get("prazo")
    if data_prazo_raw is not None:
        data_prazo: datetime = _parse_datetime(data_prazo_raw, "data_prazo", task_id)
        if data_prazo < data_criacao:
            raise TaskValidationError(
                f"Tarefa '{task_id}': data_prazo ({data_prazo.isoformat()}) anterior à "
                f"data_criacao ({data_criacao.isoformat()})."
            )
        if data_conclusao > data_prazo:
            return True

    prazo_horas_raw: Any = (
        task.get("prazo_estimado_horas")
        if task.get("prazo_estimado_horas") is not None
        else task.get("prazo_horas")
    )
    if prazo_horas_raw is not None:
        if not isinstance(prazo_horas_raw, (int, float)) or isinstance(prazo_horas_raw, bool) or prazo_horas_raw < 0:
            raise TaskValidationError(
                f"Tarefa '{task_id}': 'prazo_estimado_horas' deve ser um número não negativo."
            )
        if duration_hours > float(prazo_horas_raw):
            return True

    return False


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Analisa uma lista de tarefas e calcula métricas operacionais de desempenho.

    Cumpre rigorosamente o contrato definido em specs/task_analyzer_spec.md e
    as diretrizes de governança de CONTEXT_RULES.md.

    Args:
        tasks: Lista de dicionários representando as tarefas a serem analisadas.

    Returns:
        Dicionário contendo:
            - total_tarefas (int)
            - total_concluidas (int)
            - total_pendentes (int)
            - tempo_medio_conclusao_horas (dict[str, float]) com chaves 'geral', 'alta', 'media', 'baixa'
            - taxa_atraso_percentual (float)

    Raises:
        TaskValidationError: Quando os dados de entrada são inválidos ou quando
            data_conclusao < data_criacao.
    """
    if not isinstance(tasks, list):
        raise TaskValidationError("A entrada 'tasks' deve ser uma lista de dicionários.")

    total_tarefas: int = len(tasks)
    total_concluidas: int = 0
    total_pendentes: int = 0
    concluidas_com_atraso: int = 0

    duracoes_geral: list[float] = []
    duracoes_por_prioridade: dict[str, list[float]] = {
        "alta": [],
        "media": [],
        "baixa": [],
    }

    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise TaskValidationError(
                f"Elemento no índice {index} não é um dicionário válido."
            )

        task_id: Any = task.get("id", f"index_{index}")
        prioridade: str = _normalize_priority(task.get("prioridade"), task_id)
        status: str = _normalize_status(task.get("status"), task_id)

        if "data_criacao" not in task or task["data_criacao"] is None:
            raise TaskValidationError(
                f"Tarefa '{task_id}': campo obrigatório 'data_criacao' ausente."
            )
        data_criacao: datetime = _parse_datetime(
            task["data_criacao"], "data_criacao", task_id
        )

        data_conclusao_raw: Any = task.get("data_conclusao")

        if status == "concluida":
            if data_conclusao_raw is None:
                raise TaskValidationError(
                    f"Tarefa '{task_id}': tarefas concluídas exigem 'data_conclusao' preenchida."
                )
            data_conclusao: datetime = _parse_datetime(
                data_conclusao_raw, "data_conclusao", task_id
            )

            if data_conclusao < data_criacao:
                raise TaskValidationError(
                    f"Tarefa '{task_id}': inconsistência temporal detectada — "
                    f"data_conclusao ({data_conclusao.isoformat()}) é anterior à "
                    f"data_criacao ({data_criacao.isoformat()})."
                )

            duracao_horas: float = (
                data_conclusao - data_criacao
            ).total_seconds() / 3600.0

            total_concluidas += 1
            duracoes_geral.append(duracao_horas)
            duracoes_por_prioridade[prioridade].append(duracao_horas)

            if _is_task_delayed(
                task, data_criacao, data_conclusao, duracao_horas, task_id
            ):
                concluidas_com_atraso += 1
        else:
            if data_conclusao_raw is not None:
                data_conclusao_pendente: datetime = _parse_datetime(
                    data_conclusao_raw, "data_conclusao", task_id
                )
                if data_conclusao_pendente < data_criacao:
                    raise TaskValidationError(
                        f"Tarefa '{task_id}': inconsistência temporal detectada — "
                        f"data_conclusao ({data_conclusao_pendente.isoformat()}) é anterior à "
                        f"data_criacao ({data_criacao.isoformat()})."
                    )
            total_pendentes += 1

    media_geral: float = (
        round(sum(duracoes_geral) / total_concluidas, 2)
        if total_concluidas > 0
        else 0.0
    )

    medias_prioridade: dict[str, float] = {}
    for prio in ("alta", "media", "baixa"):
        lista_prio: list[float] = duracoes_por_prioridade[prio]
        medias_prioridade[prio] = (
            round(sum(lista_prio) / len(lista_prio), 2)
            if len(lista_prio) > 0
            else 0.0
        )

    taxa_atraso: float = (
        round((concluidas_com_atraso / total_concluidas) * 100.0, 2)
        if total_concluidas > 0
        else 0.0
    )

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "total_pendentes": total_pendentes,
        "tempo_medio_conclusao_horas": {
            "geral": media_geral,
            "alta": medias_prioridade["alta"],
            "media": medias_prioridade["media"],
            "baixa": medias_prioridade["baixa"],
        },
        "taxa_atraso_percentual": taxa_atraso,
    }
