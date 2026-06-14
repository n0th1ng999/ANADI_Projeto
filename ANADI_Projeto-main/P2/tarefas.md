# Plano de Trabalho - ANADI (TP2)

## 📅 Marcos Importantes
* **Data de Entrega:** Até 14 de junho de 2026, às 23:59 (no Moodle).
* **Formato de Entrega:** Um único ficheiro compactado (.zip) com o nome no formato: ANADI_YYY_XXX_Nºaluno1_ºaluno2_ºaluno3.zip.
* **Apresentação:** Defesa oral de 10 minutos com suporte em PowerPoint.

---

## 📋 Plano de Trabalho

### Etapa 1: Configuração e Preparação Inicial
* [X] **Tarefa 1.1:** Criar o repositório privado no GitHub e partilhar o acesso com os professores das PL.
* [X] **Tarefa 1.2:** Configurar o ambiente de trabalho local e descarregar o ficheiro de dados PTD_level_dataset.xlsx.
* [X] **Tarefa 1.3:** Configurar o documento do artigo com o template IEEE (Word ou LaTeX).

### Etapa 2: Análise Exploratória e Pré-Processamento
* [X] **Tarefa 2.1:** Carregar os dados em Python, verificar a dimensão do dataset e gerar um sumário estatístico.
* [X] **Tarefa 2.2:** Criar os gráficos mais adequados para explorar visualmente as variáveis.
* [X] **Tarefa 2.3:** Realizar o pré-processamento dos dados:
  * [X] Tratamento de valores omissos.
  * [X] Transformação de variáveis categóricas.
  * [X] Normalização ou standardização onde necessário.
  * [X] Seleção de variáveis relevantes para a modelação.

### Etapa 3: Desenvolvimento dos Modelos de Regressão
*O objetivo é prever o valor contínuo da variável PFolga_PTD usando a técnica de k-fold cross validation.*

* [X] **Tarefa 3.1:** Criar e interpretar o diagrama de correlação entre PFolga_PTD e as restantes variáveis.
* [X] **Tarefa 3.2:** Remover variáveis que não fazem sentido para o modelo de regressão
* [ ] **Tarefa 3.3:** Desenvolver o modelo de Regressão Linear Simples com uma variável explicativa relevante:
  * [ ] Apresentar a função linear resultante.
  * [ ] Desenhar a reta no diagrama de dispersão.
  * [ ] Calcular os erros MAE e RMSE.
* [ ] **Tarefa 3.4:** Desenvolver e otimizar os modelos avançados através de k-fold:
  * [ ] Regressão Linear Múltipla.
  * [ ] Árvore de Regressão (e visualizar a árvore obtida).
  * [ ] SVM (otimizar o kernel).
  * [ ] Rede Neuronal (testar 3 configurações, desenhar curvas de loss de treino/validação e discutir o impacto da learning rate e do early stopping).
* [ ] **Tarefa 3.5:** Comparar todos os modelos usando MAE e RMSE, identificar as variáveis mais relevantes e gerar as curvas de aprendizagem para os dois melhores modelos.
* [ ] **Tarefa 3.6:** Aplicar testes estatísticos adequados (nível de significância de 5%) para validar o desempenho dos dois melhores modelos.

### Etapa 4: Desenvolvimento dos Modelos de Classificação
*O objetivo é prever o nível de ocupação criando a variável utilizRede (baixo, médio, alto) a partir de Util_Decimal, usando k-fold cross validation.*

* [ ] **Tarefa 4.1:** Criar e justificar a discretização da variável utilizRede (intervalos ou quantis).
* [ ] **Tarefa 4.2:** Desenvolver os modelos de classificação através de k-fold:
  * [ ] Árvore de Decisão.
  * [ ] Rede Neuronal (otimização com 3 configurações, gráficos de loss e análise de learning rate/early stopping).
  * [ ] SVM (otimizar o kernel).
  * [ ] K-Vizinhos-Mais-Próximos (KNN) (otimizar o parâmetro K).
* [ ] **Tarefa 4.3:** Calcular a média e o desvio padrão das métricas Accuracy, Precision, Recall e F1-score por classe.
* [ ] **Tarefa 4.4:** Visualizar a importância das variáveis na Árvore de Decisão e comparar com as correlações iniciais.
* [ ] **Tarefa 4.5:** Executar testes estatísticos (nível de significância de 5%) para avaliar a diferença entre os dois melhores modelos.
* [ ] **Tarefa 4.6:** Comparar detalhadamente o melhor e o pior modelo, apresentando as suas curvas de aprendizagem e discutindo o treino.

### Etapa 5: Escrita do Artigo Científico e Conclusões
*O artigo deve ter no máximo 8 páginas e seguir a estrutura metodológica do template.*

* [ ] **Tarefa 5.1:** Redigir o Abstract e a Introdução (motivação, objetivos e metodologia seguida).
* [ ] **Tarefa 5.2:** Integrar a descrição de todos os modelos desenvolvidos, decisões de parametrização, tabelas de resultados e análise crítica no corpo do artigo.
* [ ] **Tarefa 5.3:** Escrever as conclusões gerais e identificar as principais limitações dos dados ou modelos, propondo estratégias de melhoria.

### Etapa 6: Preparação da Defesa e Submissão
* [ ] **Tarefa 6.1:** Criar a apresentação em PowerPoint estruturada para o tempo regulamentar de 10 minutos.
* [ ] **Tarefa 6.2:** Garantir que todos os elementos do grupo preparam a apresentação de uma componente do trabalho para a discussão individual.
* [ ] **Tarefa 6.3:** Organizar a pasta final, verificar se todos os ficheiros pedidos estão presentes e submeter o arquivo ZIP no Moodle dentro do prazo.

---

## 📦 Lista de Verificação da Entrega (Checklist)
Garante que o ficheiro .zip final contém os seguintes elementos obrigatórios:
- [ ] Artigo científico em formato PDF (máximo 8 páginas).
- [ ] Dados utilizados em formato .xlsx.
- [ ] Jupyter Notebook (.ipynb) completo e devidamente comentado.
- [ ] Apresentação em PowerPoint (.ppt ou .pptx).