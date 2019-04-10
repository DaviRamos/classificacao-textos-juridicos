# -*- coding: utf-8 -*-
"""df_chi_quadrado.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ObJT0AGJTF46-BNmIUHzyh_lL_psMj1B

efetua os imports das dependencias
"""

import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

"""importa os dados do arquivo excel referente ao civil e adiciona a coluna CLASSE com o valor 0, representando o tipo de dado civil"""

uri_data_civel = 'https://github.com/julianopacheco/classificacao-textos-juridicos/blob/master/arquivos/xls/civel.xlsx?raw=true'
dados_civil = pd.read_excel(uri_data_civel)
dados_civil["CLASSE"] = 0

"""importa os dados do arquivo excel referente ao crime e adiciona a coluna CLASSE com o valor 1, representando o tipo de dado crime"""

uri_data_crime = 'https://github.com/julianopacheco/classificacao-textos-juridicos/blob/master/arquivos/xls/crime.xlsx?raw=true'
dados_crime = pd.read_excel(uri_data_crime)
dados_crime["CLASSE"] = 1

"""concatena as duas fontes de dados e gera uma nova contendo as duas"""

dados_civil_e_crime = pd.concat([dados_civil, dados_crime], axis=0)

"""como agora a fonte de dados contem as duas listas e necessário embaralhar elas para que o civil e crime nao venha na ordem que foram concatenados

isso e feito com o shuffle
"""

dados_civil_e_crime = shuffle(dados_civil_e_crime)
dados_civil_e_crime.head()

"""verifica a proporcionalidade de cada um dos tipos (civil = 0, crime = 1)"""

dados_civil_e_crime.CLASSE.value_counts()

"""extrai as ementas dos dados"""

ementas = dados_civil_e_crime["EMENTA"]

"""instancia o CountVectorizer e TfidfVectorizer para vetorizar os textos das ementas"""

count_vectorizer = CountVectorizer(max_features = 50)
tfidf_vetorizar = TfidfVectorizer(max_features = 50)
tfidf_vetorizar_use_idf = TfidfVectorizer(max_features = 50, use_idf=False)

"""cria os bag of words através da transformação com os vetores CountVectorizer e TfidfVectorizer"""

bag_of_words_count = count_vectorizer.fit_transform(ementas)
bag_of_words_tfidf = tfidf_vetorizar.fit_transform(ementas)
bag_of_words_tfidf_use_idf = tfidf_vetorizar_use_idf.fit_transform(ementas)

"""gera as variaveis treino, teste, classe_treino, classe_teste através do train_test_split passando um seed de 48

estas variaveis serão utilizadas abaixo na aplicação dos algortimos
"""

treino, teste, classe_treino, classe_teste = train_test_split(bag_of_words_count,
                                                              dados_civil_e_crime.CLASSE,
                                                              random_state = 48)
treino_tfidf, teste_tfidf, classe_treino_tfidf, classe_teste_tfidf = train_test_split(bag_of_words_tfidf,
                                                                                      dados_civil_e_crime.CLASSE,
                                                                                      random_state = 48)
treino_tfidf_use_idf, teste_tfidf_use_idf, classe_treino_tfidf_use_idf, classe_teste_tfidf_use_idf = train_test_split(bag_of_words_tfidf_use_idf,
                                                                                                                      dados_civil_e_crime.CLASSE,
                                                                                                                      random_state = 48)

"""define metodos abaixo para testar a regressão logistica e o svc

define o metodo que aplica e escreve os resultados do algortimo LogisticRegression
"""

def execute_LogisticRegression(treino, classe_treino, teste, classe_teste):
  regressao_logistica = LogisticRegression(solver='lbfgs', max_iter=10000)
  regressao_logistica.fit(treino, classe_treino)
  #acuracia = regressao_logistica.score(teste, classe_teste)
  #print(f'LogisticRegression acuracia: {acuracia}')
  predicted = regressao_logistica.predict(teste)
  print(classification_report(classe_teste, predicted))

"""define um método que cria um pipeline para normalizar os dados e instanciar o algortimo SVC

efetua o treino, aplica o metodo que irá prever o teste e escreve o relatório da aplicação
"""

def execute_SVC(treino, classe_treino, teste, classe_teste):
  pipeline = Pipeline([
    ('normalizer', Normalizer()),
    ('svc', SVC(gamma='auto'))
  ])

  pipeline.fit(treino, classe_treino)
  predicted = pipeline.predict(teste)
  print(classification_report(classe_teste, predicted))

"""executa o algortimo LogisticRegression passando os dados referentes ao CountVectorizer"""

execute_LogisticRegression(treino, classe_treino, teste, classe_teste)

"""executa o algortimo LogisticRegression passando os dados referentes ao TfidfVectorizer"""

execute_LogisticRegression(treino_tfidf, classe_treino_tfidf, teste_tfidf, classe_teste_tfidf)

"""executa o algortimo SVC passando os dados referentes ao TfidfVectorizer(use_idf)"""

execute_LogisticRegression(treino_tfidf_use_idf, classe_treino_tfidf_use_idf, teste_tfidf_use_idf, classe_teste_tfidf_use_idf)

"""executa o algortimo SVC passando os dados referentes ao CountVectorizer"""

execute_SVC(treino, classe_treino, teste, classe_teste)

"""executa o algortimo SVC passando os dados referentes ao TfidfVectorizer"""

execute_SVC(treino_tfidf, classe_treino_tfidf, teste_tfidf, classe_teste_tfidf)

"""executa o algortimo SVC passando os dados referentes ao TfidfVectorizer(use_idf)"""

execute_SVC(treino_tfidf_use_idf, classe_treino_tfidf_use_idf, teste_tfidf_use_idf, classe_teste_tfidf_use_idf)