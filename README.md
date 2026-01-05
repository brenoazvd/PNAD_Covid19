# PNAD_Covid19

Projeto de Data Analytics com base tratada da PNAD-COVID-19, voltado a responder
perguntas de negocio com enfase em percentuais de sintomas mais frequentes,
comportamento da populacao e impactos economicos durante a pandemia.
Isso encaixa no que o PDF pede: sintomas + populacao + economico + meses + analise.

## Tabelas gold (BI)

1. `gold_sintomas_mes`
   - mes
   - sintoma
   - contagens e percentuais por resposta (sim/nao/ignorado)
   - foco principal: % de sintomas mais frequentes por mes

2. `gold_sintomas_perfil`
   - mes
   - faixa_etaria / sexo / UF
   - total, com_sintoma e % com sintomas chave

3. `gold_economia_mes`
   - mes
   - indicador economico (renda, ocupacao, trabalho remoto, etc.)
   - categoria, contagem e percentual

4. `gold_comportamento_mes`
   - mes
   - indicador de comportamento (isolamento, busca de atendimento, etc.)
   - categoria, contagem e percentual

## Como gerar

As tabelas sao criadas no `ETL.ipynb` e exportadas em CSV na raiz do projeto:
`gold_sintomas_mes.csv`, `gold_sintomas_perfil.csv`,
`gold_economia_mes.csv`, `gold_comportamento_mes.csv`.

Observacao: o dataset atual possui apenas `mes_referencia = 9`. Ao carregar
outros meses, as tabelas serao geradas com o historico completo.
