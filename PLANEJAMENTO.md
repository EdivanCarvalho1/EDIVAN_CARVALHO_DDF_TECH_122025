# ITEM 0 - Planejamento do Projeto – Dadosfera

## Início

O objetivo deste documento é descrever o planejamento do projeto Dadosfera, incluindo suas etapas, cronograma, recursos necessários e aspectos de controle.  
O método de diagramação utilizado é o de fluxograma, que permite visualizar o fluxo de atividades e decisões ao longo do projeto, seguindo as boas práticas de gestão propostas pelo PMBOK.

## Fluxograma

O fluxograma abaixo ilustra as principais etapas do projeto, desde a ingestão dos dados até a entrega final do case, considerando a organização dos dados em camadas da arquitetura Medallion e as fases de gerenciamento do projeto conforme o PMBOK.

![Fluxograma Dadosfera](/images/fluxograma_planejamento.drawio.png)

## Modelagem Medallion

Esse diagrama representa a estrutura da arquitetura Medallion adotada no projeto, detalhando as camadas Bronze, Silver e Gold

![Arquitetura Medallion](/images/medallion.drawio.png)
---

## Fases do Projeto (PMBOK)

| Fase | Descrição |
|----|----|
| Iniciação | Identificação do problema de negócio, definição do objetivo analítico do projeto, escolha do domínio de dados e identificação dos stakeholders. |
| Planejamento | Definição do escopo, escolha do dataset, definição da arquitetura Medallion, planejamento das etapas do pipeline, análise de riscos e custos. |
| Execução | Ingestão dos dados, organização nas camadas Bronze, Silver e Gold, tratamento e validação da qualidade, preparação dos dados para análise e visualização. |
| Monitoramento e Controle | Acompanhamento da execução das etapas, validação contínua da qualidade dos dados, verificação das métricas e ajustes no pipeline de dados. |
| Encerramento | Validação final dos resultados, consolidação da documentação, entrega do case no GitHub e gravação do vídeo final. |

---

## Análise de Riscos

| Risco Identificado | Probabilidade | Impacto | Estratégia de Mitigação |
|------------------|---------------|---------|-------------------------|
| Dataset com volume insuficiente | Baixa | Alto | Validação prévia do volume mínimo de dados antes da ingestão. |
| Problemas de qualidade nos dados brutos | Média | Médio | Aplicação de validações e controles na camada Silver. |
| Inconsistências entre camadas do pipeline | Média | Alto | Revisão das regras de transformação e testes entre Bronze, Silver e Gold. |
| Erros na definição de métricas analíticas | Baixa | Alto | Validação cruzada das métricas geradas na camada Gold. |
| Atraso na execução das etapas | Baixa | Médio | Planejamento incremental e acompanhamento contínuo das tarefas. |

---

## Estimativa de Custos

| Item | Tipo | Custo Estimado |
|----|----|----|
| Plataforma de análise e visualização Dadosfera | SaaS | Gratuito |
| GitHub | Versionamento | Gratuito |
| Google Colab | Processamento | Gratuito |
| Mão de obra | Recurso humano | Projeto acadêmico (não monetizado) |

---

## Alocação de Recursos

| Recurso | Papel | Responsabilidades |
|------|------|------------------|
| Desenvolvedor Único | Engenheiro de Dados | Ingestão dos dados, organização das camadas Medallion, pipelines e validação de qualidade. |
| Desenvolvedor Único | Analista de Dados | Exploração dos dados, definição de métricas, criação de análises e visualizações. |
| Desenvolvedor Único | Gestor do Projeto | Planejamento, gestão de riscos, acompanhamento das etapas e documentação do projeto. |

---

## Interdependências do Projeto

| Etapa | Depende de |
|----|-----------|
| Planejamento | Iniciação |
| Execução | Planejamento |
| Organização das camadas Medallion | Execução da ingestão |
| Monitoramento e Controle | Execução |
| Encerramento | Execução validada e resultados consolidados |

---

## Pontos Críticos do Projeto

| Ponto Crítico | Justificativa |
|-------------|---------------|
| Definição clara das camadas Medallion | Impacta diretamente a organização e rastreabilidade dos dados. |
| Qualidade dos dados na camada Silver | Garante confiabilidade das análises finais. |
| Consistência entre as camadas | Evita divergências entre dados brutos, tratados e analíticos. |
| Validação das métricas | Previne interpretações incorretas dos resultados. |
| Documentação final | Facilita entendimento, manutenção e avaliação do case. |

---

## Considerações Finais

O planejamento do projeto foi estruturado conforme as boas práticas do PMBOK, contemplando desde a concepção até a implementação e entrega final. A adoção da arquitetura Medallion, aliada a controles de qualidade, análise de riscos e definição clara de recursos, contribui para a organização, confiabilidade dos dados e sucesso do projeto.
