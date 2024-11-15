# -*- coding: utf-8 -*-

# Técnicas de Machine Learning
# MBA em Engenharia de Software USP ESALQ

# Prof. Dr. Wilson Tarantin Jr.

#%% Instalando os pacotes necessários

!pip install pandas
!pip install numpy
!pip install statsmodels
!pip install matplotlib
!pip install -U seaborn
!pip install pingouin
!pip install statstests
!pip install scipy

#%% Importando os pacotes

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from statstests.process import stepwise

#%% Importando o banco de dados

gestao_rh = pd.read_excel('recursos_humanos.xlsx')
# Fonte: adaptado de https://www.kaggle.com/datasets/sanjanchaudhari/employees-performance-for-hr-analytics

gestao_rh.info()

#%% Vamos remover as observações com valores faltantes

gestao_rh.dropna(inplace=True)

#%% Estatísticas descritivas

# Variáveis métricas
gestao_rh[['treinamentos', 'idade', 'nota_setor', 'anos_emprego', 'avaliacao']].describe()

# Variáveis categóricas
gestao_rh[['educacao']].value_counts()
gestao_rh[['sexo']].value_counts()
gestao_rh[['recrutamento']].value_counts()
gestao_rh[['bateu_metas']].value_counts()
gestao_rh[['premiado']].value_counts()

#%% Análise de médias entre grupos

# Média por quantidade de treinamentos
media_treino = gestao_rh[['avaliacao', 'treinamentos']].groupby('treinamentos').mean()
ax1 = sns.barplot(data=media_treino, y='avaliacao', x=media_treino.index, color='green')
ax1.bar_label(ax1.containers[0], fontsize=8, fmt='%.1f')
plt.xlabel('Qtd. Treinamentos',fontsize=12)
plt.ylabel('Avaliação Média',fontsize=12)

# Média por tipo de recrutamento
media_recrut = gestao_rh[['avaliacao', 'recrutamento']].groupby('recrutamento').mean()
ax2 = sns.barplot(data=media_recrut, y='avaliacao', x=media_recrut.index, color='purple')
ax2.bar_label(ax2.containers[0], fontsize=8, fmt='%.1f')
plt.xlabel('Origem Contratação',fontsize=12)
plt.ylabel('Avaliação Média',fontsize=12)

#%% Criação das variáveis binárias

gestao_rh = pd.get_dummies(data=gestao_rh, 
                           columns=['educacao', 'sexo', 'recrutamento'], 
                           drop_first=True,
                           dtype='float')

# Note que 'bateu_metas' e 'premiado' já são variáveis binárias

#%% Regressão Linear Simples - Treinamentos

# Estimação do modelo
modelo_treino = sm.OLS.from_formula(formula = 'avaliacao ~ treinamentos',
                                    data=gestao_rh).fit()

# Obtenção dos outputs
modelo_treino.summary()

#%% Regressão Linear Múltipla - Recrutamento

# Estimação do modelo
modelo_recrut_1 = sm.OLS.from_formula(formula = 'avaliacao ~ recrutamento_sites_midias + recrutamento_sourcing',
                                      data=gestao_rh).fit()

# Obtenção dos outputs
modelo_recrut_1.summary()

# Estimação do modelo removendo a variável não significante
modelo_recrut_2 = sm.OLS.from_formula(formula = 'avaliacao ~ recrutamento_sourcing',
                                      data=gestao_rh).fit()

# Obtenção dos outputs
modelo_recrut_2.summary()

#%% Criando o texto completo da fórmula

def texto_formula(df, var_dependente, excluir_cols):
    variaveis = list(df.columns.values)
    variaveis.remove(var_dependente)
    for col in excluir_cols:
        variaveis.remove(col)
    return var_dependente + ' ~ ' + ' + '.join(variaveis)

texto_regressao = texto_formula(gestao_rh, 'avaliacao', ['id_funcionario'])

#%% Regressão Linear Múltipla - Modelo Completo

# Estimação do modelo
modelo_rh = sm.OLS.from_formula(formula = texto_regressao,
                                data=gestao_rh).fit()

# Obtenção dos outputs
modelo_rh.summary()

#%% Procedimento de stepwise para remoção de variáveis não significantes

modelo_stepwise = stepwise(modelo_rh, pvalue_limit=0.05)

#%% Valores preditos pelo modelo para as observações da amostra

# Vamos elaborar uma tabela em separado
tabela_fitted = pd.DataFrame({'observado': gestao_rh['avaliacao'],
                              'previsao': modelo_stepwise.fittedvalues,
                              'residuos': modelo_stepwise.resid})

#%% Realizando predições para outras observações

obs_multipla = pd.DataFrame({'treinamentos': [2],
                             'idade': [40],
                             'nota_setor': [3],
                             'bateu_metas': [1],
                             'premiado': [0],
                             'educacao_pos_grad': [0],
                             'sexo_masculino': [1],
                             'recrutamento_sourcing':[0]})

print(f'avaliação média predita: {round(modelo_stepwise.predict(obs_multipla)[0],1)}')

#%% Também é possível fazer previsões considerando os intervalos de confiança

# Para o nível de confiança de 95%
# Quais são os valores mínimo e máximo previstos da avaliação do funcionário?

pred_int = pd.DataFrame({'ci_inf': modelo_stepwise.conf_int(alpha=0.05)[0],
                         'ci_sup': modelo_stepwise.conf_int(alpha=0.05)[1]})

pred_int['obs']=[1, 2, 40, 3, 1, 0, 0, 1, 0]
# Note que o primeiro "1" da lista refere-se ao intercepto

# Mínimo (limite inferior de intervalo de confiança)
sum(pred_int['ci_inf'] * pred_int['obs'])

# Máximo (limite superior de intervalo de confiança)
sum(pred_int['ci_sup'] * pred_int['obs'])

#%% Comparando graficamente os ajustes dos modelos

sns.regplot(tabela_fitted, x='observado', y='previsao', color='blue', scatter_kws={'s':0.10}, line_kws={'color':'red', 'lw':2})
plt.title('Análise Gráfica do Ajuste', fontsize=10)
plt.xlabel('Avaliação Observada', fontsize=10)
plt.ylabel('Avaliação Prevista pelo Modelo', fontsize=10)
plt.tick_params(labelsize=6)
plt.axline((2, 2), (max(tabela_fitted['observado']), max(tabela_fitted['observado'])), linewidth=1, color='grey')
plt.show()

#%% Fim!