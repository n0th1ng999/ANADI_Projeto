# Justificação e Especificação dos Scripts Auxiliares

Durante a transição do teu Jupyter Notebook (`P2_V2.ipynb`) para o formato de Dashboard Web interativo, foi necessário adicionar alguns ficheiros `.py` auxiliares. Estes scripts **não alteram** a tua análise matemática nem as tuas conclusões originais. O seu único propósito é agir como "pontes" (extratores) para exportar os dados do Python para a Web.

## 1. `generate_eda_images.py`

### Porquê adicionar?
O HTML e o JavaScript (via bibliotecas como Chart.js ou Plotly) são excelentes para gráficos interativos de barras ou linhas. No entanto, não conseguem reproduzir mapas geoespaciais (latitude/longitude), matrizes de correlação densas (heatmaps) ou estruturar dezenas de boxplots e histogramas sem sobrecarregar gravemente a memória do navegador web (especialmente com 70.000+ linhas de dados).

### Funcionalidade (Especificações)
Este script isola a secção inicial de pré-processamento do teu notebook. Lê o `dataset` final, constrói os gráficos utilizando as bibliotecas `Matplotlib` e `Seaborn` com o estilo estético do dashboard, e exporta-os silenciosamente como imagens PNG para a pasta `dashboard/assets/`:
- **`mapa.png`**: Mapa de distribuição geográfica.
- **`heatmap.png`**: Matriz de Correlação de Pearson.
- **`boxplots.png`**: Visualização dos Outliers.
- **`arvore.png`**: Estrutura base da Árvore de Regressão/Decisão.
- **`histogramas.png`**: Distribuição assimétrica das variáveis numéricas.

## 2. `P2_V2_no_gui.py` e `fast_extractor.py`

### Porquê adicionar?
Para que os gráficos web de Performance dos Modelos (`Plotly` e `Chart.js`) mostrem dados reais, eles precisam de arrays com as métricas exatas calculadas pelo teu Cross-Validation (ex: Accuracies, F1-Scores, Tempos de Treino, Erros MAE/RMSE). 

### Funcionalidade (Especificações)
Estes componentes foram criados para correr as tuas secções de treino (`Pipeline`, `GridSearchCV`, `cross_validate`), recolher os arrays numéricos gerados pelo `scikit-learn` e injetá-los no objeto JSON estático que o Dashboard web consome (visível no topo do ficheiro `dashboard.js`). 
Isto garante que os valores observados no Dashboard (e visualizados nos radares e nas barras) representam **rigorosamente** os mesmos outputs matemáticos obtidos durante a tua defesa no Jupyter Notebook, impedindo a adulteração visual.
