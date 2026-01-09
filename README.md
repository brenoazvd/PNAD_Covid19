# PNAD_Covid19

Projeto de Data Analytics com base tratada da PNAD-COVID-19, voltado a responder
perguntas de negocio sobre sintomas clinicos, comportamento e impactos
economicos durante a pandemia.

## Trabalho

Tech Challenge - Fase 3 (Data Analytics)

## Integrantes

- Giovanni Piratelo (gpiratelo@gmail.com)
- Breno Rodrigues Azevedo (brenorazevedo@hotmail.com)

## Contexto de extracao (AWS)

- A extracao dos microdados foi feita em bucket AWS (free tier).
- Scripts e credenciais nao ficam neste repo porque sao temporarios.

## Pipeline (limpeza + ETL)

1. Rode `Limpeza_Base_PNAD.ipynb` para gerar `dados_tratados_completo.csv`
2. Rode `ETL.ipynb` (usa `dados_tratados.csv`)
3. (Opcional) Rode `python gerar_graficos.py` para criar os graficos do relatorio

Dependencias principais: `pandas` e `matplotlib`.

## Perguntas de negocio e tabelas

- c. Caracterizacao dos sintomas clinicos
  - `gold_sintomas_mes`
  - `gold_sintomas_perfil`
  - `gold_sintomas_frequentes_mes`
  - `frequencia_sintomas`
- d. Comportamento da populacao na COVID-19
  - `gold_comportamento_mes`
- e. Caracteristicas economicas da sociedade
  - `gold_economia_mes`

## Graficos e fontes

- `relatorios/figuras/sintomas_evolucao.png`
  - Fonte: `gold_sintomas_mes` (pct_sim por mes, top sintomas)
- `relatorios/figuras/medida_isolamento.png`
  - Fonte: `gold_comportamento_mes` (categorias por mes)
- `relatorios/figuras/economia_indicadores.png`
  - Fonte: `gold_economia_mes` (indicadores com categoria = Sim)
- `relatorios/figuras/faixa_rendimento.png`
  - Fonte: `gold_economia_mes` (faixa_rendimento por mes)

## Tabelas gold (BI)

1. `gold_sintomas_mes`
   - mes, sintoma, contagens e percentuais por resposta
2. `gold_sintomas_perfil`
   - mes, faixa_etaria, sexo, UF, total, com_sintoma, pct
3. `gold_economia_mes`
   - mes, indicador economico, categoria, contagem, pct
4. `gold_comportamento_mes`
   - mes, indicador de comportamento, categoria, contagem, pct
5. `gold_sintomas_frequentes_mes`
   - mes, sintoma, pct_sim, rank_pct_sim

## Visao de apoio

`frequencia_sintomas`
- linhas = resposta (Nao/Sim/Ignorado/Nao_sabe)
- colunas = sintomas
- valores = percentual por sintoma (0-100)
- objetivo: responder diretamente "% sintomas mais frequentes"

## Observacao sobre meses

O dataset atual possui `mes_referencia = 07, 08, 09`. Ao carregar outros meses,
as tabelas e relatorios serao gerados com o historico completo.
