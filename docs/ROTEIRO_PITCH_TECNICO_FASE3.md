# Roteiro Oficial do Pitch Técnico de Defesa (Fase 3 — 5 Minutos)

**Disciplina:** Bootcamp III — Fase 3 (25,0 Pontos)  
**Projeto:** `sdd-task-analyzer` (`TaskAnalyzer`)  
**Aluno:** Victor Hugo Azevedo Alves Zainote  
**Tempo Total:** `00:00` a `05:00` (5 minutos)

---

## Preparação Antes de Gravar (Abas e Terminal Abertos)

Deixe abertas na sua tela as seguintes janelas antes de iniciar a gravação (OBS Studio, Loom ou Gravador do Windows `Win + G`):

1. **Aba 1 do Navegador:** Página principal do repositório no GitHub (`https://github.com/VictorZainote/Bootcamp-3`) mostrando a árvore de arquivos completa (`.github/workflows/ci.yml`, `Dockerfile`, `docker-compose.yml`, `CONTEXT_RULES.md`, `specs/`, `src/`, `tests/`).
2. **Aba 2 do Navegador:** Aba **Actions** do GitHub (`https://github.com/VictorZainote/Bootcamp-3/actions`) mostrando os workflows com **Green Build (`100% Passed`)** e um workflow aberto nos detalhes do passo `Executar suíte de testes automatizados (Test Harness)`.
3. **Aba 3 / Terminal (Docker Desktop ou GitHub Codespaces):**
   - **Dica Rápida (GitHub Codespaces — Zero Instalação Local):** Na página do seu repositório no GitHub, clique no botão verde **`<> Code`** -> aba **`Codespaces`** -> **`Create codespace on main`**. Ele abrirá um VS Code completo no navegador com **Docker já instalado e pronto**!
   - Ou, se estiver usando o terminal local com Docker Desktop aberto, deixe na pasta do projeto (`cd "C:\Users\Windows 11\Documents\antigravity\nifty-curie"`).
4. **Aba 4:** O arquivo `Relatorio_Tecnico_Governanca_Etica_Fase3.pdf` (ou os arquivos `CONTEXT_RULES.md` e `src/task_analyzer.py` abertos no VS Code).

---

## Storyboard Cronometrado (Slide 10)

### Bloco 1 (`0:00 - 0:30`) — Abertura (Nome, Polo e Contexto da Fase 3)
**[Na tela: Mostrar a página principal do repositório no GitHub com o seu rosto na webcam ou áudio claro]**

> **Fala sugerida:**  
> *"Olá professor e avaliadores! Meu nome é **Victor Hugo Azevedo Alves Zainote**, aluno do **CEUB** [mencione seu polo/campus, ex: Asa Norte / Taguatinga], e este é o Pitch Técnico de defesa da **Fase 3 — O Desafio Final do sistema TaskAnalyzer**.*  
> *Nas Fases 1 e 2, estruturamos a arquitetura baseada em especificações — o SDD —, criamos as regras de contexto em `CONTEXT_RULES.md` e homologamos o algoritmo em Python com `pytest`. Agora, na **Fase 3**, evoluímos o projeto para o padrão corporativo de produção: eliminando o 'na minha máquina funciona' por meio de **Integração Contínua (CI/CD)** com GitHub Actions, **Containerização Isolada com Docker** e **Auditoria Ética de IA no modelo Critical-in-the-Loop**."*

---

### Bloco 2 (`0:30 - 2:00`) — Demo CI/CD (Aba Actions do GitHub)
**[Na tela: Clicar na aba `Actions` do repositório no GitHub, mostrar a lista de execuções com ícone verde ✅ e abrir uma execução para mostrar o log do `pytest tests/test_harness.py -v`]**

> **Fala sugerida:**  
> *"Começando pelo **Pilar 1: O Motor de Integração Contínua (CI/CD)**. Aqui no arquivo `.github/workflows/ci.yml`, configuramos a nossa esteira automatizada no GitHub Actions.*  
> *Como podemos ver na configuração do workflow, definimos gatilhos automáticos para qualquer evento de `push` ou `pull_request` direcionado às branches `main` e `develop`.*  
> *A cada alteração de código, o GitHub provisiona uma máquina limpa com sistema `ubuntu-latest` e **Python 3.11**, instala exclusivamente as dependências homologadas no `requirements.txt` e executa o comando `pytest tests/test_harness.py -v`.*  
> *Abrindo aqui a aba **Actions** do nosso repositório público, vemos todos os workflows com **Green Build**. Entrando nos logs da etapa de execução do Test Harness, comprovamos que os 7 testes automatizados — cobrindo o Cenário 1 de cálculo de métricas gerais e por prioridade, o Cenário 2 de bloqueio de inconsistências temporais com `TaskValidationError`, os casos de borda contra divisão por zero e as validações de domínio — passaram com **100% de aprovação (100% Passed)**."*

---

### Bloco 3 (`2:00 - 3:30`) — Demo Docker (Terminal executando `docker build`, `docker run` e `docker compose run`)
**[Na tela: Alternar para o Terminal (no GitHub Codespaces ou no PowerShell com Docker) e executar os comandos ao vivo]**

**Comandos para rodar ao vivo durante a fala:**
```bash
# 1. Construir a imagem isolada a partir do Dockerfile (python:3.11-slim)
docker build -t sdd-task-analyzer .

# 2. Executar o container isolado rodando o CMD padrão (pytest tests/test_harness.py -v)
docker run --rm sdd-task-analyzer

# 3. Demonstrar também a orquestração via Docker Compose com comando único
docker compose run --rm task-analyzer
```

> **Fala sugerida:**  
> *"Passando para o **Pilar 2: Containerização Isolada com Docker**. Para garantir portabilidade absoluta e reprodutibilidade idêntica em qualquer servidor, empacotamos a aplicação no `Dockerfile` utilizando a imagem oficial leve e imutável `python:3.11-slim`. Nela, configuramos o diretório de trabalho `/app`, instalamos o `requirements.txt`, copiamos o código-fonte e definimos o `pytest tests/test_harness.py -v` como comando principal de entrada (`CMD`).*  
> *Além disso, criamos o `docker-compose.yml` para orquestrar o serviço de testes de forma padronizada.*  
> *Aqui no terminal, vou executar primeiro o comando `docker build -t sdd-task-analyzer .` para construir a imagem isolada... [aguarda concluir].*  
> *Agora, executando `docker run --rm sdd-task-analyzer` — e também `docker compose run --rm task-analyzer` — vemos o container subir de forma totalmente independente do sistema operacional hospedeiro e executar toda a suíte de testes com **100% de aprovação (7 passed)**."*

---

### Bloco 4 (`3:30 - 5:00`) — Governança Ética de IA (`Critical-in-the-Loop`) e Conclusão
**[Na tela: Mostrar o `CONTEXT_RULES.md`, o código em `src/task_analyzer.py` (linhas de validação temporal e divisão por zero) e o PDF `Relatorio_Tecnico_Governanca_Etica_Fase3.pdf`]**

> **Fala sugerida:**  
> *"Por fim, no **Pilar 3: Governança e Ética de IA**, aplicamos o modelo **Critical-in-the-Loop** detalhado no nosso Relatório Técnico em PDF.*  
> *Em vez de aceitar cegamente o código gerado por IA, construímos uma barreira determinística unindo o contrato SDD (`specs/task_analyzer_spec.md` e `specs/requirements.yaml`) ao arquivo `CONTEXT_RULES.md`.*  
> *Isso bloqueou alucinações críticas na origem: primeiro, impediu que a IA importasse bibliotecas externas não autorizadas como `pandas` ou `numpy`, mantendo o código 100% na biblioteca padrão do Python 3.11. Segundo, na etapa de homologação humana, atuamos ativamente sobre dois pontos críticos em `src/task_analyzer.py`:*  
> *1) A validação estrita de integridade temporal: sempre que `data_conclusao` é anterior à `data_criacao`, o sistema interrompe o cálculo e lança a exceção de domínio `TaskValidationError`, jamais permitindo durações negativas silenciosas;*  
> *2) A proteção determinística contra `ZeroDivisionError`: quando a lista de tarefas está vazia ou nenhuma tarefa foi concluída — seja no cálculo geral ou em uma prioridade específica (`alta`, `media` ou `baixa`) — o sistema retorna `0.0` com segurança.*  
> *Dessa forma, unimos **Confiabilidade Técnica** (Docker + CI/CD) e **Confiabilidade Ética** (SDD + Critical-in-the-Loop), entregando um software robusto, auditável e pronto para produção. Muito obrigado!"*
