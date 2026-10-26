# ==============================================================================
# Dockerfile — Empacotamento Isolado e Imutável do Sistema TaskAnalyzer
# Imagem base leve oficial conforme especificação da Fase 3 (python:3.11-slim)
# ==============================================================================

FROM python:3.11-slim

LABEL maintainer="Victor Hugo Azevedo Alves Zainote <vh.azvd@sempreceub.com>"
LABEL project="sdd-task-analyzer"
LABEL phase="Bootcamp III - Fase 3 (DevOps, Docker & Governança de IA)"

# Evita geração de arquivos .pyc e força flush imediato de logs no terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Instala exclusivamente as dependências autorizadas no contrato de governança
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte, especificações SDD, regras de contexto e suíte de testes
COPY CONTEXT_RULES.md README.md ./
COPY specs/ ./specs/
COPY src/ ./src/
COPY tests/ ./tests/

# Comando de entrada principal (CMD): executa a suíte de testes automatizados
CMD ["pytest", "tests/test_harness.py", "-v"]
