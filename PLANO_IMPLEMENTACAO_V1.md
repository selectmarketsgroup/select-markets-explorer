# Plano de implementação V1 — select-markets-explorer

> **Projeto:** Market Explorer — investigação autónoma de novos mercados  
> **Estado:** plano de desenvolvimento, **não** implementação concluída.  
> **Dossier global:** [Select Markets Group — V1](https://github.com/selectmarketsgroup/select-markets-platform/blob/main/docs/SELECT_MARKETS_GROUP_V1_GLOBAL.md)  
> **Conta:** selectmarketsgroup · **Acesso:** repositório privado · **Idioma:** PT-PT

## 1. Missão deste repositório

Descobrir novos segmentos úteis para o grupo, dentro ou fora de Homes/Motors/Deals, avaliar viabilidade económica e técnica e recomendar integrações fundamentadas.

**Dependências e fronteiras:** Utiliza Platform para hipóteses e dossiers, Discovery para provas de fontes, Intelligence para comparar relevância e risco.

**Base técnica prevista:** Python, pesquisa web/fonte permitida, pipelines de estudos e métricas, contratos Platform; camada de IA abstrata até fase 2.

A Select Markets é inicialmente um **sistema privado de uso pessoal**, não um marketplace público. Este projeto não executa compras, vendas ou licitações; toda a ação financeira continua dependente da decisão humana.

## 2. Funcionalidades e blocos de implementação

Os blocos são implementados **um a um**, com testes relevantes concluídos antes do seguinte. As funcionalidades complexas devem ser subdivididas em tarefas pequenas, sem criar burocracia de aprovações.

### E01 — Geração de hipóteses aberta
**Implementar:** Propor segmentos a partir de oportunidades, tendências, lacunas de oferta, fontes emergentes e investigação, não de lista fixa.

**Validar/testar:** Hipóteses desconhecidas previamente entram sem editar arrays no código.

### E02 — Mapa de mercado
**Implementar:** Definir âmbito, bens, participantes, canais, geografias, fontes e casos de uso pessoal.

**Validar/testar:** Dossier com campos obrigatórios e lacunas explícitas.

### E03 — Pesquisa de fontes
**Implementar:** Descobrir APIs, datasets, anúncios públicos, universidades e estudos, com datas, termos e URLs.

**Validar/testar:** Fontes inexistentes ou não autorizadas são rejeitadas.

### E04 — Viabilidade de acesso
**Implementar:** Avaliar mecanismos técnicos, qualidade, cobertura, atualização, custo e restrições jurídicas das fontes.

**Validar/testar:** Cenário sem dados disponíveis classificado não viável, sem desbloqueio artificial.

### E05 — Potencial económico
**Implementar:** Investigar possibilidade de comparação real, fricção, custos, liquidez, dimensão qualitativa e diferenciação.

**Validar/testar:** Sem ROI ou dimensão de mercado fictícios; incerteza sinalizada.

### E06 — Protótipo controlado
**Implementar:** Testar amostra limitada com dados reais permitidos e indicadores de qualidade antes de integrar.

**Validar/testar:** Prova demonstra exemplos verificados, não apenas relatório textual.

### E07 — Proposta de destino
**Implementar:** Recomendar adicionar segmento a Homes/Motors/Deals ou justificar novo motor se indispensável.

**Validar/testar:** Testes de classificação de mercados e defesa de não duplicar módulos.

### E08 — Prioridade e carteira de hipóteses
**Implementar:** Registar fases pesquisar/testar/integrar/descartar, deduplicar ideias, rever quando surgem novos dados.

**Validar/testar:** Sem pedidos de aprovação para investigação corrente; alertar apenas expansão material.

### E09 — Avaliação posterior
**Implementar:** Recolher resultados reais de segmentos integrados e comparar com premissas; ajustar critérios.

**Validar/testar:** Dossiers reavaliados sem apagar o histórico da hipótese.

## 3. Integrações e contratos

- Explorer ↔ Platform: MarketHypothesis, evidence, experiments, decision.
- Consultas à Discovery e Intelligence seguem contratos; Explorer não assume controlo de jobs.
- IA fornecida apenas na fase 2, mantendo pesquisa e lógica de validação testáveis na fase 1.

Os contratos partilhados pertencem à Platform; alterações incompatíveis exigem migração versionada e testes de consumidores. Não criar cópias paralelas da base central.

## 4. Sequência de desenvolvimento e validação

**Etapa A — Fundação do projeto:** estrutura de pastas, configuração, ferramentas de lint/typecheck, dependências fixadas, CI **GitHub Actions**, testes de arranque, README de execução local e configurações de exemplo sem segredos.

**Etapa B — Domínio e contratos:** modelos, validação de entradas/saídas, interfaces e fixtures representativas, incluindo falhas e casos limites; testes unitários e contratuais.

**Etapa C — Funcionalidades:** implementar todos os blocos da secção 2 e respetivos testes; nunca marcar como funcional uma integração mockada.

**Etapa D — Integração:** testes com a Platform e outros consumidores relevantes; segurança, observabilidade, erros, idempotência e integração de dados reais **permitidos**, com recursos de teste identificados.

**Etapa E — Fecho técnico:** executar lint, typecheck, testes unitários/de integração, análise de dependências, build e validação dos critérios de aceitação; corrigir até CI verde; documentar limitações factuais sem as esconder.

**Processo repetível por funcionalidade:** implementar → validar → testar → corrigir → integrar → confirmar critérios. Sem relatórios duplicados ou circuitos de aprovação para tarefas normais.

## 5. Critérios de aceitação específicos

1. Dossiers com fontes concretas, confiança, riscos, custo e decisão fundamentada.
2. Demonstração de nichos fora de uma lista codificada.
3. Propostas indicam integrar em motor existente quando possível.
4. Nenhum mercado é ativado sem dados mínimos verificáveis.
5. CI verde; nenhuma expansão automática compromete recursos/pagamentos.

## 6. Testes obrigatórios e política de qualidade

- **Unitários:** transformações, regras, casos limites e entradas inválidas.
- **Contrato:** schema de eventos e APIs Platform/consumidores; versão e compatibilidade.
- **Integração:** caminhos felizes, falha parcial, dados ausentes, repetição e idempotência.
- **Segurança:** permissões, proteção de segredos, inputs não fiáveis e limites adequados ao módulo.
- **Qualidade dos dados:** referências/proveniência, timestamps e distinção entre facto, estimativa e hipótese.
- **Regressão:** fixtures reais autorizadas ou sintéticas claramente marcadas; bugs corrigidos geram testes.
- **CI:** GitHub Actions exclusivamente para build/verificações/testes; **não** criar jobs operacionais aqui.

Se uma dependência ainda não estiver implementada, usar contratos e testes isolados identificados. Isso **não** comprova integração real. Não publicar classificações artificiais de qualidade nem afirmar CI verde antes de executar.

## 7. Sequência global obrigatória

1. **Fase 1:** implementar e validar o código-base dos **nove** repositórios, com GitHub Actions para CI. Esta é a fase atual.
2. **Fase 2:** após os nove projetos concluídos, **avaliar, escolher e integrar IA**, com benchmarks e repetição dos testes. Preparar interfaces/contratos desde já, sem selecionar fornecedor antes.
3. **Fase 3:** apenas depois da fase 2, configurar **CircleCI** para jobs operacionais, agendamentos, manutenção e deploy. Não criar projetos/jobs CircleCI na fase 1.

A infraestrutura aprovada é **GitHub + Supabase + Hugging Face + IA posteriormente selecionada + CircleCI na fase final**, segregada da Strata Capital. Não existe exigência de usar serviços pagos para executar as funcionalidades.

## 8. Definição objetiva de conclusão deste repositório

Considerar o projeto **implementado** apenas quando código e migrações/scripts aplicáveis existirem, funcionalidades previstas estiverem efetivamente testadas, contratos integrados ou dependências em falta documentadas, segurança e observabilidade verificadas, e GitHub Actions apresentar resultados aprovados. Um documento escrito ou mocks não contam como funcionalidades terminadas.

**Estado ao criar este plano:** apenas especificação; execução técnica por iniciar.
