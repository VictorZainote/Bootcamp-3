"""Suíte de Testes Automatizados (Test Harness) para o sistema TaskAnalyzer.

Valida rigorosamente os Cenários de Aceite 1, 2 e Casos de Borda especificados
em specs/task_analyzer_spec.md utilizando pytest.
"""

from __future__ import annotations

from typing import Any

import pytest

from src.task_analyzer import TaskValidationError, analyze_tasks


# ============================================================================
# CENÁRIO 1: Teste de Sucesso (Cálculo de Métricas Gerais, por Prioridade e Atraso)
# ============================================================================


def test_cenario_1_sucesso_calculo_completo_metricas() -> None:
    """Valida cálculos de totais, tempo médio (geral e por prioridade) e taxa de atraso."""
    tarefas: list[dict[str, Any]] = [
        {
            "id": 1,
            "titulo": "Corrigir bug crítico em produção",
            "prioridade": "alta",
            "status": "concluida",
            "data_criacao": "2026-10-01T08:00:00",
            "data_conclusao": "2026-10-01T12:00:00",  # 4.0 horas
            "prazo_estimado_horas": 6.0,  # No prazo
        },
        {
            "id": 2,
            "titulo": "Implementar autenticação MFA",
            "prioridade": "alta",
            "status": "concluida",
            "data_criacao": "2026-10-02T09:00:00",
            "data_conclusao": "2026-10-02T17:00:00",  # 8.0 horas
            "prazo_estimado_horas": 5.0,  # Atrasada (8h > 5h)
        },
        {
            "id": 3,
            "titulo": "Atualizar documentação da API",
            "prioridade": "media",
            "status": "concluida",
            "data_criacao": "2026-10-03T10:00:00",
            "data_conclusao": "2026-10-03T13:00:00",  # 3.0 horas
            "data_prazo": "2026-10-03T14:00:00",  # No prazo
        },
        {
            "id": 4,
            "titulo": "Revisar logs de auditoria",
            "prioridade": "baixa",
            "status": "concluida",
            "data_criacao": "2026-10-04T14:00:00",
            "data_conclusao": "2026-10-04T19:00:00",  # 5.0 horas
            "data_prazo": "2026-10-04T16:00:00",  # Atrasada (conclusão > prazo)
        },
        {
            "id": 5,
            "titulo": "Planejar arquitetura da Fase 3",
            "prioridade": "media",
            "status": "pendente",
            "data_criacao": "2026-10-05T09:00:00",
            "data_conclusao": None,
            "prazo_estimado_horas": 10.0,
        },
    ]

    resultado: dict[str, Any] = analyze_tasks(tarefas)

    # Totais: 5 tarefas (4 concluídas, 1 pendente)
    assert resultado["total_tarefas"] == 5
    assert resultado["total_concluidas"] == 4
    assert resultado["total_pendentes"] == 1

    # Médias de conclusão:
    # Geral: (4.0 + 8.0 + 3.0 + 5.0) / 4 = 20.0 / 4 = 5.0
    # Alta: (4.0 + 8.0) / 2 = 6.0
    # Média: 3.0 / 1 = 3.0
    # Baixa: 5.0 / 1 = 5.0
    medias: dict[str, float] = resultado["tempo_medio_conclusao_horas"]
    assert medias["geral"] == 5.0
    assert medias["alta"] == 6.0
    assert medias["media"] == 3.0
    assert medias["baixa"] == 5.0

    # Taxa de atraso: 2 atrasadas em 4 concluídas = 50.0%
    assert resultado["taxa_atraso_percentual"] == 50.0


# ============================================================================
# CENÁRIO 2: Teste de Exceção/Erro (Datas Inconsistentes -> TaskValidationError)
# ============================================================================


def test_cenario_2_erro_data_conclusao_anterior_data_criacao() -> None:
    """Valida disparo de TaskValidationError quando data_conclusao < data_criacao."""
    tarefas_invalidas: list[dict[str, Any]] = [
        {
            "id": 101,
            "titulo": "Tarefa com anomalia temporal",
            "prioridade": "alta",
            "status": "concluida",
            "data_criacao": "2026-10-10T15:00:00",
            "data_conclusao": "2026-10-10T10:00:00",  # 5 horas ANTES da criação
            "prazo_estimado_horas": 4.0,
        }
    ]

    with pytest.raises(TaskValidationError, match="inconsistência temporal"):
        analyze_tasks(tarefas_invalidas)


def test_cenario_2_erro_tarefa_concluida_sem_data_conclusao() -> None:
    """Valida disparo de TaskValidationError quando tarefa concluída não tem data_conclusao."""
    tarefas_sem_conclusao: list[dict[str, Any]] = [
        {
            "id": 102,
            "titulo": "Tarefa concluída incompleta",
            "prioridade": "media",
            "status": "concluida",
            "data_criacao": "2026-10-10T08:00:00",
            "data_conclusao": None,
        }
    ]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas_sem_conclusao)


# ============================================================================
# CENÁRIO 3: Testes de Casos de Borda (Lista Vazia e Apenas Tarefas Pendentes)
# ============================================================================


def test_caso_borda_lista_vazia_retorna_zeros_sem_divisao_por_zero() -> None:
    """Garante que uma lista vazia retorne 0 e 0.0 sem lançar ZeroDivisionError."""
    resultado: dict[str, Any] = analyze_tasks([])

    assert resultado["total_tarefas"] == 0
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 0
    assert resultado["tempo_medio_conclusao_horas"] == {
        "geral": 0.0,
        "alta": 0.0,
        "media": 0.0,
        "baixa": 0.0,
    }
    assert resultado["taxa_atraso_percentual"] == 0.0


def test_caso_borda_apenas_tarefas_pendentes_retorna_medias_zero() -> None:
    """Garante retorno de 0.0 para médias e taxa de atraso quando só há tarefas pendentes."""
    tarefas_pendentes: list[dict[str, Any]] = [
        {
            "id": 201,
            "titulo": "Configurar pipeline GitHub Actions",
            "prioridade": "alta",
            "status": "pendente",
            "data_criacao": "2026-10-12T08:00:00",
            "data_conclusao": None,
        },
        {
            "id": 202,
            "titulo": "Criar Dockerfile multi-stage",
            "prioridade": "baixa",
            "status": "pendente",
            "data_criacao": "2026-10-12T09:30:00",
            "data_conclusao": None,
        },
    ]

    resultado: dict[str, Any] = analyze_tasks(tarefas_pendentes)

    assert resultado["total_tarefas"] == 2
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 2
    assert resultado["tempo_medio_conclusao_horas"] == {
        "geral": 0.0,
        "alta": 0.0,
        "media": 0.0,
        "baixa": 0.0,
    }
    assert resultado["taxa_atraso_percentual"] == 0.0
