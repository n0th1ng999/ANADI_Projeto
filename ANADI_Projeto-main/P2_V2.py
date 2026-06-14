#!/usr/bin/env python
# coding: utf-8

# # P2

# ## Importar bibliotecas

# In[ ]:


import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import math
import scipy.stats as stats
import numpy as np
import sklearn 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler, OrdinalEncoder, StandardScaler
from sklearn.model_selection import KFold, cross_validate, learning_curve, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.svm import SVR, LinearSVR
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
# [SUBSTITUÍDO] import tensorflow as tf
# [KERAS removido] # [SUBSTITUÍDO] from tensorflow.keras.models import Sequential
# [KERAS removido] # [SUBSTITUÍDO] from tensorflow.keras.layers import Dense, Dropout, Input
# [KERAS removido] # [SUBSTITUÍDO] from tensorflow.keras.regularizers import l2
# [KERAS removido] # [SUBSTITUÍDO] from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
# --- Classificação ---
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, classification_report, confusion_matrix,
                             ConfusionMatrixDisplay)
from sklearn.model_selection import StratifiedKFold


# --- Redes Neuronais via sklearn (substitui Keras/TF) ---
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.pipeline import Pipeline


# #### Definir style sheet

# In[ ]:


# 1. Apply base seaborn-paper style
plt.style.use('seaborn-v0_8-paper')  # Use 'seaborn-paper' if on older matplotlib versions

# 2. Overhaul rcParams for maximum article readability
plt.rcParams.update({
    # Text and Typography
    "text.usetex": False,                   # Set to True ONLY if you have a local LaTeX installation

    # Font Sizes (Optimized for standard paper columns)
    "axes.labelsize": 10,                   # X and Y axis titles
    "axes.titlesize": 11,                   # Plot title
    "xtick.labelsize": 8,                   # X-axis tick labels
    "ytick.labelsize": 8,                   # Y-axis tick labels
    "legend.fontsize": 8,                   # Legend items font size
    "legend.title_fontsize": 9,             # Legend title font size

    # Figure Layout & Dimensions
    "figure.figsize": [3.39, 2.5],          # Fits standard 3.39-inch single columns (e.g., IEEE/Nature)
    "figure.constrained_layout.use": True,  # Auto-adjusts padding to prevent clipped text
    "figure.dpi": 150,                      # Crisp display rendering on high-res monitors

    # Plot Styling details
    "axes.spines.top": False,               # Strip away top bounding box border
    "axes.spines.right": False,             # Strip away right bounding box border
    "axes.grid": True,                      # Keep grids enabled for data alignment
    "grid.alpha": 0.3,                      # Make grid lines subtle and unobtrusive
    "grid.linestyle": "--",                 # Dashed grid lines
    "lines.linewidth": 1.25,                # Slightly thicker lines for visibility
    "lines.markersize": 4,                  # Balanced data marker dots

    # Vector Graphics Export Stability
    "pdf.fonttype": 42,                     # Embed true fonts inside PDFs (prevents text errors)
    "ps.fonttype": 42                       # Embed true fonts inside PostScript formats
})

pd.set_option('display.max_columns', 50)  # Remove o limite de colunas
pd.set_option('display.max_rows', 100)     # Remove o limite de linhas
pd.set_option('display.width', 300)        # Evita que o texto quebre para a linha de baixo


# ## EDA e Pré Processamento
# ### Carregar Dataframe

# In[ ]:


DATASET_FILE_PATH = "PTD_level_dataset.xlsx"
df = pd.read_excel(DATASET_FILE_PATH)
df.head()


# | # | Propriedade | Tipo | Descrição |
# |---|---|---|---|
# | 1 | Distrito | Categórica | Distrito português onde o PTD está localizado |
# | 2 | Concelho | Categórica | Concelho associado ao PTD |
# | 3 | CodDistritoConcelho | Identificador | Código único que representa a combinação distrito + concelho |
# | 4 | Código de Instalação | Identificador | Identificador único do Posto de Transformação |
# | 5 | Coordenadas Geográficas | Geográfica | Latitude e longitude do PTD |
# | 6 | Potência instalada [kVA] | Numérica | Potência nominal instalada no PTD |
# | 7 | Tipo Construtivo | Categórica | Tipo físico/construtivo do PTD |
# | 8 | Cap_PTD_kVA | Numérica | Capacidade total do PTD em kVA |
# | 9 | Pot_Contratada_kVA | Numérica | Soma da potência contratada pelos clientes ligados ao PTD |
# | 10 | N_Clientes | Inteira | Número total de clientes associados ao PTD |
# | 11 | Pot_Geracao_kW | Numérica | Potência de geração local (produção elétrica distribuída) |
# | 12 | N_Clientes_Produtores | Inteira | Número de clientes produtores de energia |
# | 13 | P_IP_Total | Numérica | Potência total consumida pela iluminação pública |
# | 14 | P_IP_Inef | Numérica | Potência associada à iluminação pública ineficiente |
# | 15 | Rate_Ineficiencia | Numérica | Taxa de ineficiência energética da iluminação pública |
# | 16 | LED_Ratio | Numérica | Percentagem/proporção de luminárias LED |
# | 17 | N_Luminarias | Inteira | Número total de luminárias |
# | 18 | N_Lampadas | Inteira | Número total de lâmpadas |
# | 19 | N_PTDs_Concelho | Inteira | Número de PTD existentes no concelho |
# | 20 | PVE_PTD | Numérica | Potência estimada necessária para veículos elétricos |
# | 21 | D_PTD | Numérica | Saldo de viabilidade energética do PTD |
# | 22 | IP_per_PTD | Numérica | Média da potência de iluminação pública por PTD |
# | 23 | IP_Inef_per_PTD | Numérica | Média da potência ineficiente por PTD |
# | 24 | Ganho_LED_PTD | Numérica | Ganho energético obtido pela substituição por LED |
# | 25 | D_PTD_LED | Numérica | Saldo energético do PTD após modernização LED |
# | 26 | Cap_per_Cliente | Numérica | Capacidade média disponível por cliente |
# | 27 | PContratada_per_Cliente | Numérica | Potência contratada média por cliente |
# | 28 | Geracao_per_Cliente | Numérica | Geração média de energia por cliente |
# | 29 | Clientes_Produtores_Ratio | Numérica | Percentagem/proporção de clientes produtores |
# | 30 | Nível de Utilização [%] | Numérica | Percentagem de utilização da capacidade do PTD |
# | 31 | Util_Decimal | Numérica | Representação decimal do nível de utilização |
# | 32 | PFolga_PTD | Numérica (Target) | Capacidade livre/remanescente do PTD para novas cargas elétricas |

# In[ ]:


# Primeira limpeza
df.drop_duplicates(inplace= True)


# In[ ]:


df.info()


# In[ ]:


df["CodDistritoConcelho"] = df["CodDistritoConcelho"].astype(str).astype('category')


# ### Resumo
# - Tamanho: ~72.000 registos; mix de variáveis categóricas, inteiras e decimais.
# 
# - Nulos: Pot_Contratada_kVA, Pot_Geracao_kW, D_PTD, D_PTD_LED, Geracao_per_Cliente,Util_Decimal, PFolga_PTD; 
# 
# - Dependências: variáveis derivadas dependem de outras (PContratada_per_Cliente ← Pot_Contratada_kVA, Geracao_per_Cliente ← Pot_Geracao_kW).
# 
# - Oportunidades: analisar potência por território, concentração de clientes, ineficiência e diferenças LED/distritos.
# 
# - CodDistritoConcelho tem de ser categorico
# 
# ### Primeiros Passos
# 
# - Tratar nulos: avaliar caso a caso (imputar / manter / remover).
# - Verificar derivadas: confirmar fórmulas e origem dos campos calculados.
# - Converter campos: percentagens → numérico; coordenadas → lat/lon.
# - Análises: agregações por concelho/distrito, mapas e modelos simples se for preciso.

# ### Variáveis categóricas

# In[ ]:


categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
print("Categorical Columns: \n",  categorical_columns)


# In[ ]:


# Unique values for each categorical column
print("Valores únicos de variáveis categóricas")
for column in categorical_columns:
    unique_vals = df[column].unique()

    print(f"\n\n{column} ({len(unique_vals)} valores únicos):\n {unique_vals}")


# - Tipos textuais **Único**: Código de Instalação (ID) pode ser utilizado como index; 
# - Tipos textuais: Coordenadas Geográficas precisa de parsing (lat/lon); 
# - Nível de Utilização [%] tem “%” N/D e tem de ser tratado.

# In[ ]:


# Set index
df.set_index("Código de Instalação", inplace=True)


# In[ ]:


# Split Coordenadas
df[["latitude", "longitude"]] = df["Coordenadas Geográficas"].str.split(",", expand=True)
df.drop(columns="Coordenadas Geográficas", inplace=True)

# Converter em float
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)
df.head()


# In[ ]:


# 1. Filter out columns with > 20 unique values up front
categorical_columns = [
    col
    for col in df.select_dtypes(include=["object", "category", "string"]).columns
    if df[col].nunique() <= 10
]

# 2. Dynamic grid layout calculation
num_cols = len(categorical_columns)
grid_cols = 1  # Adjust this to 3 or 4 if you have many columns
grid_rows = math.ceil(num_cols / grid_cols)

# 3. Create the single figure context
fig, axes = plt.subplots(
    grid_rows, grid_cols, figsize=(16, 14)
)
axes = axes.flatten()  # Flatten to easily loop over them with a single index

# 4. Populate the subplots
for i, column in enumerate(categorical_columns):
    ax = axes[i]

    # Create the sorted count plot on the specific subplot axis (ax=ax)
    sns.countplot(
        data=df,
        x=column,
        order=df[column].value_counts().index,
        legend=False,
        ax=ax,
    )

    # Loop through all containers to label every single bar
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=9, weight="bold")

    # Clean up labels per subplot
    ax.set_title(f"Counts for: {column}", fontsize=12, pad=10, weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)


# 5. Hide any leftover/empty subplot boxes in the grid
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Adjust spacing and display
plt.tight_layout()
plt.show()


# Como N/D é uma classe significativa é melhor considera-la para um modelo final.

# In[ ]:


df_mapa = (
    df.assign(
        lat_round=df["latitude"].round(1),
        lon_round=df["longitude"].round(1)
    )
    .groupby(["lat_round", "lon_round"])
    .size()
    .reset_index(name="quantidade")
)

plt.figure(figsize=(7, 9))

# Plot standard points where color and size reflect "quantidade"
sc = plt.scatter(
    df_mapa["lon_round"], 
    df_mapa["lat_round"], 
    c=df_mapa["quantidade"], 
    cmap="viridis",
    s=df_mapa["quantidade"] / df_mapa["quantidade"].max() * 200, # Variable sizing
    alpha=0.8
)

plt.colorbar(sc, label="Quantidade")
plt.title("Distribuição de Registos")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle="--", alpha=0.3)
plt.show()


# Ao olhar para este mapa de densidade, a primeira coisa que salta à vista é a forte concentração dos  dados ao longo de toda a faixa litoral de Portugal Continental.
# 
# Destacam-se claramente dois grandes "focos" a amarelo (onde há maior volume de registos): um na região da Grande Lisboa e outro na zona do Grande Porto.
# 
# Em contrapartida, nota-se perfeitamente que a zona interior do país está muito mais "vazia", com pontos de densidade muito mais baixos espalhados pelo território. No fundo, a distribuição no mapa acompanha, de forma muito clara, as zonas de maior e menor densidade populacional do país.

# ### Variáveis Numéricas
# 

# In[ ]:


df.describe()


# #### 1. Dimensão e Dados em Falta (Missing Values)
# 
# O dataset contém uma base de 72.027 registos analisados na maioria das colunas.
# Há um grande número de nulos nas variáveis de geração de energia (Pot_Geracao_kW e Geracao_per_Cliente), que possuem apenas 1.836 registos. Isto indica que uma pequena minoria (~2.5%) dos postos/instalações tem registo de produção ativa (como painéis solares na área).
# A coluna de Pot_Contratada_kVA também apresenta falhas, com apenas 50.847 registos válidos (cerca de 30% da base sem dados desta variável). Outras variáveis descritivas (como D_PTD, Util_Decimal) também têm cerca de 3.000 registos em falta.
# 
# #### 2. Assimetria (Outliers Severos / Right-Skewed)
# 
# Existe uma variabilidade extrema em variáveis-chave. Por exemplo:
# N_Clientes: A mediana é 54, a média é 94, mas o máximo atinge valores absurdos de 1.438 clientes num só posto.
# Potência instalada [kVA]: A maioria ronda os 250 kVA (mediana), mas há postos massivos com capacidades até 8.000 kVA. Isto sugere que há um pequeno grupo de PTDs (Postos de Transformação de Distribuição) altamente densos (zonas super urbanas/industriais) perante uma vasta maioria mais "leve" ou rural.
# 
# #### 3. Penetração LED vs Ineficiência
# 
# Adoção LED avançada: O LED_Ratio médio é de cerca de 67%, com a mediana em quase 72% e o percentil 75 já acima dos 91%. Isto demonstra que a atualização da rede de iluminação para LED não só já começou, como está fortemente instalada.
# Margem para melhoria (Ineficiência): Apesar de bons níveis de LED, o Rate_Ineficiencia situa-se nos 28% (média), chegando os casos extremos perto dos 98%. Há, portanto, oportunidades claras de melhoria (por exemplo, ao reduzir P_IP_Inef).
# 
# #### 4. Capacidade e Utilização
# 
# A taxa de utilização média (Util_Decimal) está em torno de 51% (com metade a operar abaixo dos 39%).
# Isto alinha-se perfeitamente com a variável PFolga_PTD (Folga real do PTD), indicando que, na generalidade, a rede de distribuição parece ter boas "gorduras" para evitar sobrecargas extremas.

# In[ ]:


corr_matrix = df.select_dtypes(include=['number']).corr()

plt.figure(figsize=(10, 8))

sns.heatmap(
    corr_matrix, 
    annot=True,
    annot_kws={"size": 6}, # Adjusted annotation size
    cmap='coolwarm',    
    fmt=".2f",           
    vmin=-1, vmax=1      
)

plt.title('Matriz de Correlação de Pearson')
plt.show()


# In[ ]:


# Selecionar variáveis numéricas
numeric_df = df.select_dtypes(include=['number'])

# Criar histogramas para as variáveis numéricas
numeric_df.hist(figsize=(16, 14), bins=30, edgecolor='black')

plt.suptitle('Histogramas das Variáveis Numéricas', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajustar layout para não sobrepor o título
plt.show()


# In[ ]:


# Selecionar variáveis numéricas
numeric_df = df.select_dtypes(include=['number'])

num_cols = len(numeric_df.columns)
cols = 2
rows = math.ceil(num_cols / cols)

# Definir estilo dos outliers (fliers) com transparência e sem borda
# O parametro alpha=0.1 ajuda a visualizar onde há maior concentração de pontos
flierprops = dict(
    marker='o', 
    markerfacecolor='black', 
    markeredgecolor='none', 
    markersize=3, 
    alpha=0.1
)

# Criar boxplots em subplots separados
numeric_df.plot(
    kind='box', 
    subplots=True, 
    layout=(rows, cols), 
    figsize=(20, 36), 
    sharex=False, 
    sharey=False,
    fontsize=8,
    vert=False,
    flierprops=flierprops  # Aplicar a transparência aos outliers
)

plt.suptitle('Boxplots das Variáveis Numéricas', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajustar layout para não sobrepor o título
plt.show()


# #### Tratamento de nulos

# In[ ]:


# 1. Imputação de Zeros para Variáveis de Geração
# O elevado número de nulos nestas colunas (~70k) reflete que a esmagadora maioria dos postos não tem produção injetada. 
# Preencher com 0 é a abordagem lógica.
df['Pot_Geracao_kW'] = df['Pot_Geracao_kW'].fillna(0)
df['Geracao_per_Cliente'] = df['Geracao_per_Cliente'].fillna(0)

# 2. Imputação pela Mediana (Potência Contratada)
# Faltam cerca de 21 mil registos (~30%). Sendo demasiados para eliminar, usamos a Mediana para não criar viés através da Média (que é desvirtuada por outliers mesmo após winsorization limitativo).
median_pot_contratada = df['Pot_Contratada_kVA'].median()
df['Pot_Contratada_kVA'] = df['Pot_Contratada_kVA'].fillna(median_pot_contratada)

median_pcont_per_cliente = df['PContratada_per_Cliente'].median()
df['PContratada_per_Cliente'] = df['PContratada_per_Cliente'].fillna(median_pcont_per_cliente)

# 3. Eliminação de Registos (Elimination / Dropping)
# As restantes variáveis - ['D_PTD', 'D_PTD_LED', 'Util_Decimal', 'PFolga_PTD'] - têm os exatos 3064 nulos em comum (aprox 4.2% dos dados).
# Como são indicadores-chave complexos de calcular que envolvem variáveis técnicas espaciais que provavelmente estão em falta na source, 
# a abordagem mais segura é eliminar as observações afetadas para assegurar a precisão do algoritmo.
cols_to_drop_na = ['D_PTD', 'D_PTD_LED', 'Util_Decimal', 'PFolga_PTD']
df.dropna(subset=cols_to_drop_na, inplace=True)

print(f"Dimensão final do dataset pós-limpeza de nulos: {df.shape}")
missing_info = df.isnull().sum()
print("\\nValores nulos restantes:")
if len(missing_info[missing_info > 0]) == 0:
    print("Nenhum! O dataset está totalmente preenchido.")
else:
    print(missing_info[missing_info > 0])


# In[ ]:


df.info()


# #### Tratamento de outliers

# In[ ]:


# Variáveis que representam "volumes" / quantidades (fortemente enviesadas à direita em zonas urbanas)
# Para estas, o valor ser muito alto é real (e.g., um posto numa zona de alta densidade),
# logo vamos aplicar WINSORIZATION (limitar aos valores de Z-score limiar) para não perder a informação.
cols_to_winsorize = [
    'Potência instalada [kVA]', 'Cap_PTD_kVA', 'Pot_Contratada_kVA', 
    'N_Clientes', 'N_PTDs_Concelho', 'P_IP_Total', 'P_IP_Inef',
    'N_Luminarias', 'N_Lampadas', 'Cap_per_Cliente', 'PContratada_per_Cliente'
]

# Variáveis relacionadas a produção (muitos zeros, alguns outliers enormes)
# Winsorization é útil aqui para abafar instalações que parecem centrais inteiras
cols_prod = [
    'Pot_Geracao_kW', 'N_Clientes_Produtores', 'Geracao_per_Cliente'
]

# Variáveis que são Rácios, Índices ou Percentagens. 
# Valores extremos podem ser erros de cálculo na base de dados original.
# Nesses casos, a imputação (por exemplo com a mediana) pode ser mais segura se os identificarmos como outliers.
cols_to_impute = [
    'Rate_Ineficiencia', 'LED_Ratio', 'Util_Decimal', 'PFolga_PTD', 
    'Clientes_Produtores_Ratio', 'IP_per_PTD', 'IP_Inef_per_PTD', 
    'Ganho_LED_PTD', 'D_PTD', 'D_PTD_LED', 'PVE_PTD'
]

z_thresh = 3

print("--- WINSORIZATION ---")
for col in cols_to_winsorize + cols_prod:
    if col not in df.columns: continue

    mean_val = df[col].mean()
    std_val = df[col].std()

    lower_bound = mean_val - z_thresh * std_val
    upper_bound = mean_val + z_thresh * std_val

    # As quantidades devem ser positivas
    if lower_bound < 0:
        lower_bound = 0

    outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    outliers_count = outliers_mask.sum()

    if outliers_count > 0:
        df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        print(f"[{col}] {outliers_count} outliers winsorizados.")

print("\n\n--- IMPUTATION (SUBSTITUIR POR MEDIANA) ---")
for col in cols_to_impute:
    if col not in df.columns: continue

    mean_val = df[col].mean()
    std_val = df[col].std()

    lower_bound = mean_val - z_thresh * std_val
    upper_bound = mean_val + z_thresh * std_val

    outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    outliers_count = outliers_mask.sum()

    if outliers_count > 0:
        median_val = df[col].median()
        # Imputar outliers com a mediana
        df.loc[outliers_mask, col] = median_val
        print(f"[{col}] {outliers_count} outliers imputados com a mediana ({median_val:.3f}).")

# Verificar se existem variáveis com valores muito absurdos fisicamente que precisemos remover (Trimming)
# ex: valores negativos de distâncias, ou taxas de utilização negativas
# Para taxas e ratios, elas deveriam estar entre 0 e 1 (ou 100%).
invalid_mask = pd.Series(False, index=df.index)


# #### Testes de Independencia ANOVA (PFolga_PTD)

# In[ ]:


target_var = 'PFolga_PTD'
alpha = 0.05

print(f"--- ANÁLISE DE INDEPENDÊNCIA COM A TARGET: {target_var} ---\n")

# Para armazenar resultados
results = []
vars_to_keep = []

# Separar numéricas (correlação de Pearson/Spearman) e categóricas (ANOVA/Kruskal)
num_cols_test = df.select_dtypes(include=['number']).columns.drop(target_var)
cat_cols_test = df.select_dtypes(include=['object', 'category']).columns

# 1. TESTE PARA VARIÁVEIS NUMÉRICAS (Correlação de Spearman - mais robuso que Pearson)
for col in num_cols_test:
    # Retirar nulos (se houver algum extra) para o teste
    valid_data = df[[col, target_var]].dropna()

    if len(valid_data) > 1:
        corr, p_value = stats.spearmanr(valid_data[col], valid_data[target_var])
        keep = 'Yes' if p_value < alpha else 'No'
        if keep == 'Yes': vars_to_keep.append(col)

        results.append({
            'Variável': col,
            'Tipo': 'Numérica',
            'Teste': 'Spearman Correlation',
            'Estatística (Corr/F)': corr,
            'P-Value': p_value,
            'Manter (p < 0.05)': keep
        })

# 2. TESTES PARA VARIÁVEIS CATEGÓRICAS (ANOVA)
for col in cat_cols_test:
    valid_data = df[[col, target_var]].dropna()
    groups = [group[target_var].values for name, group in valid_data.groupby(col)]

    # Executar ANOVA apenas se tivermos mais que um grupo e dados suficientes
    if len(groups) > 1:
        f_stat, p_value = stats.f_oneway(*groups)
        keep = 'Yes' if p_value < alpha else 'No'
        if keep == 'Yes': vars_to_keep.append(col)

        results.append({
            'Variável': col,
            'Tipo': 'Categórica',
            'Teste': 'ANOVA (F-oneway)',
            'Estatística (Corr/F)': f_stat,
            'P-Value': p_value,
            'Manter (p < 0.05)': keep
        })

# 3. EXIBIR TABELA
results_df = pd.DataFrame(results)

# Formatar para exibição limpa
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: f'{x:.5f}')
print(results_df.sort_values(by='P-Value').to_string(index=False))

print("\n--- CONCLUSÃO ---")
print(f"Número total de variáveis testadas: {len(results_df)}")
print(f"Número de variáveis sugeridas a MANTER (associadas à target): {len(vars_to_keep)}")
print(f"Variáveis a DESCARTAR (Independentes da target, p >= 0.05): \n{results_df[results_df['Manter (p < 0.05)'] == 'No']['Variável'].tolist()}")


# In[ ]:


df.drop(columns="PVE_PTD", inplace=True)


# ### Drop IDs
# 
# Eliminar variáveis 

# # 4.2 Modelos de Regressão

# In[ ]:


# 
def show_correlations(df, variavel_alvo, title = "Antes da remoção de variáveis diretamente correlacionadas com PFolga_PTD" ):
    # Calcular as ligações
    num_df = df.select_dtypes(include=['number'])

    correlacao = num_df.corr()

    # Isolar a variável desejada e ordená-la
    corr_alvo = correlacao[variavel_alvo].drop(variavel_alvo).sort_values(ascending=False)

    # Criar o gráfico
    plt.figure(figsize=(8, 4))
    sns.barplot(x=corr_alvo.values, y=corr_alvo.index, palette='viridis')

    # Textos do gráfico ajustados automaticamente ao nome da variável
    plt.title(title)
    plt.suptitle(f'Como as outras variáveis afetam: {variavel_alvo}')
    plt.xlabel('Força da Ligação (-1 a 1)')
    plt.ylabel('Características')
    plt.tight_layout()
    plt.show()


show_correlations(df, "PFolga_PTD")



# In[ ]:


# 1. Definir o limiar e o alvo
threshold = 0.95
target_var = 'PFolga_PTD'

print("--- REMOÇÃO DE VARIÁVEIS ALTAMENTE CORRELACIONADAS COM O ALVO ---")

# 2. Selecionar APENAS as colunas com números da tabela
num_df = df.select_dtypes(include=['number'])

# 2. Calcular a força da ligação de todas as variáveis APENAS com o alvo
corr_com_alvo = num_df.corr()[target_var].abs()

# 3. Escolher as que passam dos 0.95 (excluindo o próprio alvo, que é 1.0)
to_drop = corr_com_alvo[(corr_com_alvo > threshold) & (corr_com_alvo.index != target_var)].index.tolist()

print(f"Variáveis a remover ({threshold}): {to_drop}")

# 4. Remover da tabela
df.drop(columns=to_drop, inplace=True)

print(f"Dimensão final: {df.shape}")


# In[ ]:


show_correlations(df, "PFolga_PTD")


# In[ ]:


df.head()


# ## Regressão Linear Simples 

# In[ ]:


# ---------------------------------------------------------
# JUSTIFICAÇÃO E ESCOLHA DA VARIÁVEL
# ---------------------------------------------------------
alvo = 'PFolga_PTD'

# Analisa apenas os números e escolhe a variável com a ligação mais forte
df_numerico = df.select_dtypes(include=['number'])
correlacoes = df_numerico.corr()[alvo].abs().drop(alvo)
melhor_var = correlacoes.idxmax()

print(f"JUSTIFICAÇÃO: Escolheu-se a variável '{melhor_var}' pois apresenta a correlação mais forte ({correlacoes[melhor_var]:.4f}) com a {alvo}, sendo a melhor candidata para explicar o seu comportamento.\n")

X = df[[melhor_var]]
y = df[alvo]
modelo = LinearRegression()

# ---------------------------------------------------------
# c) CALCULAR ERROS COM K-FOLD (5 fatias)
# ---------------------------------------------------------
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_resultados = cross_validate(modelo, X, y, cv=kf, scoring=('neg_mean_absolute_error', 'neg_root_mean_squared_error'))

mae_kfold = -cv_resultados['test_neg_mean_absolute_error'].mean()
rmse_kfold = -cv_resultados['test_neg_root_mean_squared_error'].mean()

print("--- c) MÉTRICAS DE ERRO (K-Fold) ---")
print(f"MAE  (Média da margem de erro): {mae_kfold:.4f}")
print(f"RMSE (Penaliza erros grandes):  {rmse_kfold:.4f}\n")

# ---------------------------------------------------------
# a) APRESENTAR A FUNÇÃO LINEAR RESULTANTE
# ---------------------------------------------------------
# Treinamos com tudo para ter a reta oficial
modelo.fit(X, y)
inclinacao = modelo.coef_[0]
intersecao = modelo.intercept_

print("--- a) FUNÇÃO LINEAR RESULTANTE ---")
print(f"{alvo} = ({inclinacao:.4f} * {melhor_var}) + {intersecao:.4f}\n")

# ---------------------------------------------------------
# b) VISUALIZAR A RETA E O DIAGRAMA DE DISPERSÃO
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))

# Os pontos soltos (diagrama de dispersão)
plt.scatter(X, y, color='blue', alpha=0.5, label='Dados Reais')

# A linha de previsão (reta de regressão)
plt.plot(X, modelo.predict(X), color='red', linewidth=2, label='Reta de Previsão')

plt.title(f'Relação entre {melhor_var} e {alvo}')
plt.xlabel(melhor_var)
plt.ylabel(alvo)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()


# ## Regressão linear Múltipla

# In[ ]:


alvo = 'PFolga_PTD'
X = df.drop(columns=[alvo])
y = df[alvo]


# In[ ]:


#=====================================================
# 1. DETECT COLUMN TYPES
# =====================================================

numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
categorical_cols = X.select_dtypes(exclude=['number']).columns.tolist()

ordinal_cols = ['Nível de Utilização [%]']
categorical_cols = [c for c in categorical_cols if c not in ordinal_cols]

# =====================================================
# 2. PREPROCESSOR
# =====================================================

preprocessor = ColumnTransformer(
    transformers=[
        ('numeros', RobustScaler(), numeric_cols),
        ('ordinais', OrdinalEncoder(), ordinal_cols),
        ('texto', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
    ]
)

# =====================================================
# 3. PIPELINE (MODEL)
# =====================================================

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# =====================================================
# 4. TRAIN / TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# =====================================================
# 5. TRAIN MODEL
# =====================================================

model.fit(X_train, y_train)

# =====================================================
# 6. EXTRACT MODEL PARAMETERS
# =====================================================

reg = model.named_steps['regressor']
coefs = reg.coef_
intercept = reg.intercept_

# Feature names after preprocessing
feature_names = model.named_steps['preprocessor'].get_feature_names_out()

# =====================================================
# 7. FEATURE IMPORTANCE TABLE
# =====================================================

importance_df = pd.DataFrame({
    "feature": feature_names,
    "coefficient": coefs
})

importance_df["abs_coefficient"] = importance_df["coefficient"].abs()
importance_df = importance_df.sort_values("abs_coefficient", ascending=False)

print("\nTOP 20 FEATURES:")
print(importance_df.head(20))

# =====================================================
# 8. FULL LINEAR FORMULA
# =====================================================

terms = [
    f"({c:.4f} * {f})"
    for c, f in zip(coefs, feature_names)
]

formula = "y = " + f"{intercept:.4f} + " + " + ".join(terms)

print("\nLINEAR REGRESSION FORMULA:\n")
print(formula)

# =====================================================
# 9. MODEL EVALUATION (OPTIONAL)
# =====================================================

from sklearn.metrics import mean_squared_error, mean_absolute_error

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)

print("\nEVALUATION:")
print(f"MSE:  {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE:  {mae:.4f}")


# In[ ]:


# ==========================================
# 2. Decision Tree (Good Defaults)
# ==========================================
# Defaults: max_depth=5 and min_samples_split=10 prevent the tree from overfitting.
pipeline_tree = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', DecisionTreeRegressor(max_depth=5, min_samples_split=10, min_samples_leaf=5, random_state=42))
])

cv_tree = cross_validate(pipeline_tree, X, y, cv=kf, scoring='neg_mean_absolute_error')
mae_tree = -cv_tree['test_score'].mean()
print(f"Decision Tree MAE: {mae_tree:.4f}\n")

# Plot the tree
pipeline_tree.fit(X, y)
feature_names_out = pipeline_tree.named_steps['preprocessor'].get_feature_names_out()

plt.figure(figsize=(16, 6))
plot_tree(pipeline_tree.named_steps['model'], feature_names=feature_names_out, filled=True, fontsize=9)
plt.title("Decision Tree Regressor (Max Depth = 5)")
plt.show()


# In[ ]:


# =============================================================
# 4.2.3d — REDE NEURONAL PARA REGRESSÃO (MLPRegressor sklearn)
# 3 configurações: Simples, Profunda, Regularizada
# =============================================================
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

X_preprocessed = preprocessor.fit_transform(X, y)

# Split: 80% treino / 20% teste
X_train, X_test, y_train, y_test = train_test_split(
    X_preprocessed, y,
    test_size=0.2, random_state=42
)
# Validação a partir do treino (80% de 80% = 64% total)
X_train_final, X_val, y_train_final, y_val = train_test_split(
    X_train, y_train,
    test_size=0.2, random_state=42
)

print(f"Treino: {X_train_final.shape} | Validação: {X_val.shape} | Teste: {X_test.shape}")

# 3 Configurações de MLP
configs_nn = {
    'Simples':      MLPRegressor(hidden_layer_sizes=(32,),            max_iter=150, random_state=42, early_stopping=True, validation_fraction=0.2, learning_rate_init=0.001),
    'Profundo':     MLPRegressor(hidden_layer_sizes=(128, 64, 32),    max_iter=150, random_state=42, early_stopping=True, validation_fraction=0.2, learning_rate_init=0.001),
    'Regularizado': MLPRegressor(hidden_layer_sizes=(128, 64, 32),    max_iter=150, random_state=42, early_stopping=True, validation_fraction=0.2, learning_rate_init=0.001, alpha=0.01),
}

histories_nn = {}
models_nn    = {}
results_nn   = []

for nome, model_nn in configs_nn.items():
    print(f"\nA treinar: {nome}")
    model_nn.fit(X_train_final, y_train_final)
    histories_nn[nome] = model_nn.loss_curve_
    models_nn[nome]    = model_nn
    y_pred_test = model_nn.predict(X_test)
    mae_nn_  = mean_absolute_error(y_test, y_pred_test)
    rmse_nn_ = np.sqrt(mean_squared_error(y_test, y_pred_test))
    results_nn.append({'Modelo': nome, 'MAE': round(mae_nn_, 4), 'RMSE': round(rmse_nn_, 4)})
    print(f"  MAE={mae_nn_:.4f}  RMSE={rmse_nn_:.4f}  Épocas={model_nn.n_iter_}")

results_nn_df = pd.DataFrame(results_nn).sort_values('MAE')
print("\nResultados Rede Neuronal Regressão:")
print(results_nn_df.to_string(index=False))

# Curvas de Loss (treino)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, (nome, loss_curve) in zip(axes, histories_nn.items()):
    ax.plot(loss_curve, color='#2980b9', label='Treino (MSE)')
    ax.set_title(f'Loss — {nome}', fontweight='bold')
    ax.set_xlabel('Épocas'); ax.set_ylabel('MSE Loss')
    ax.legend(); ax.grid(True, alpha=0.3)
plt.suptitle('Curvas de Loss — Rede Neuronal (Regressão)', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

best_nn_reg_name = results_nn_df.iloc[0]['Modelo']
print(f"\nMelhor configuração: {best_nn_reg_name}")

# Guardar MAE/RMSE para a tabela comparativa
nn_mae_reg  = results_nn_df.iloc[0]['MAE']
nn_rmse_reg = results_nn_df.iloc[0]['RMSE']


# In[ ]:


# =============================================================
# Avaliação final NN regressão — já feita na célula anterior
# =============================================================
print("Resumo NN Regressão:")
print(results_nn_df.to_string(index=False))


# In[ ]:


# ==========================================
# c) SVM (Grid Search Setup)
# ==========================================
svm_pipeline = Pipeline(steps=[
    ('prep', preprocessor), 
    ('model', SVR(verbose=False, max_iter=10000, cache_size=2000, tol=0.01))
    ])

svm_params = {
    'model__kernel': ['linear', 'rbf'],
}

# Using a dictionary for cleaner output names
scoring_metrics = {
    'mae': 'neg_mean_absolute_error',
    'rmse': 'neg_root_mean_squared_error'
}

svm_grid = GridSearchCV(
    svm_pipeline, 
    svm_params, 
    cv=kf, 
    scoring=scoring_metrics,
    refit='mae',
    n_jobs=-1,
    verbose=1
)

svm_grid.fit(X, y)

# We need to find the index of the winning model to get both of its scores
best_idx = svm_grid.best_index_
best_mae = -svm_grid.cv_results_['mean_test_mae'][best_idx]
best_rmse = -svm_grid.cv_results_['mean_test_rmse'][best_idx]

print(f"Best SVM Parameters: {svm_grid.best_params_}")
print(f"SVM MAE: {best_mae:.4f}")
print(f"SVM RMSE: {best_rmse:.4f}")


# ## 4.2.4 — Comparação Final dos Modelos de Regressão
# 
# Nesta secção comparamos todos os modelos de regressão desenvolvidos usando MAE (erro médio absoluto) e RMSE (raiz quadrada do erro médio).

# In[ ]:


# =============================================================
# 4.2.4 — TABELA COMPARATIVA DE TODOS OS MODELOS DE REGRESSÃO
# =============================================================
# Os resultados individuais foram obtidos nos passos anteriores.
# Aqui consolidamos tudo numa única tabela e gráfico comparativo.

# --- Regressão Linear Simples (k-fold) ---
alvo = 'PFolga_PTD'
X_reg = df.drop(columns=[alvo])
y_reg = df[alvo]

kf5 = KFold(n_splits=5, shuffle=True, random_state=42)

# Regressão Linear Simples
df_numerico_reg = df.select_dtypes(include=['number'])
corrs_reg = df_numerico_reg.corr()[alvo].abs().drop(alvo)
best_var = corrs_reg.idxmax()
X_simples = df[[best_var]]
cv_ls = cross_validate(LinearRegression(), X_simples, y_reg, cv=kf5,
                       scoring=['neg_mean_absolute_error', 'neg_root_mean_squared_error'])
mae_ls  = -cv_ls['test_neg_mean_absolute_error'].mean()
rmse_ls = -cv_ls['test_neg_root_mean_squared_error'].mean()

# Regressão Linear Múltipla (k-fold com pipeline)
numeric_cols_reg = X_reg.select_dtypes(include=['number']).columns.tolist()
categorical_cols_reg = X_reg.select_dtypes(exclude=['number']).columns.tolist()
ordinal_cols_reg = ['Nível de Utilização [%]']
categorical_cols_reg = [c for c in categorical_cols_reg if c not in ordinal_cols_reg]

preprocessor_reg = ColumnTransformer(transformers=[
    ('numeros', RobustScaler(), numeric_cols_reg),
    ('ordinais', OrdinalEncoder(), ordinal_cols_reg),
    ('texto', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols_reg)
])

pipe_lm = Pipeline([('prep', preprocessor_reg), ('model', LinearRegression())])
cv_lm = cross_validate(pipe_lm, X_reg, y_reg, cv=kf5,
                       scoring=['neg_mean_absolute_error', 'neg_root_mean_squared_error'])
mae_lm  = -cv_lm['test_neg_mean_absolute_error'].mean()
rmse_lm = -cv_lm['test_neg_root_mean_squared_error'].mean()

# Árvore de Regressão (k-fold)
pipe_tree = Pipeline([('prep', preprocessor_reg),
                      ('model', DecisionTreeRegressor(max_depth=5, min_samples_split=10,
                                                       min_samples_leaf=5, random_state=42))])
cv_tree_r = cross_validate(pipe_tree, X_reg, y_reg, cv=kf5,
                           scoring=['neg_mean_absolute_error', 'neg_root_mean_squared_error'])
mae_tree_r  = -cv_tree_r['test_neg_mean_absolute_error'].mean()
rmse_tree_r = -cv_tree_r['test_neg_root_mean_squared_error'].mean()

# Rede Neuronal (melhor config 'Profundo') — métricas do teste
# Nota: a NN foi avaliada num split fixo (não k-fold) pelo custo computacional.
# Os valores abaixo são do conjunto de teste (80/20 split).
nn_mae  = nn_mae_reg   # melhor config NN regressão
nn_rmse = nn_rmse_reg  # melhor config NN regressão

# SVM (melhor kernel do GridSearch, calculado na célula anterior)
svm_mae  = best_mae   # SVM — MAE k-fold (svm_grid)
svm_rmse = best_rmse  # SVM — RMSE k-fold (svm_grid)

# --- TABELA COMPARATIVA ---
comparison_df = pd.DataFrame([
    {'Modelo': 'Reg. Linear Simples',  'MAE': mae_ls,   'RMSE': rmse_ls},
    {'Modelo': 'Reg. Linear Múltipla', 'MAE': mae_lm,   'RMSE': rmse_lm},
    {'Modelo': 'Árvore de Regressão',  'MAE': mae_tree_r, 'RMSE': rmse_tree_r},
    {'Modelo': 'Rede Neuronal (Profunda)', 'MAE': nn_mae, 'RMSE': nn_rmse},
    {'Modelo': f'SVM ({svm_grid.best_params_["model__kernel"]})', 'MAE': svm_mae,  'RMSE': svm_rmse},
])

comparison_df = comparison_df.sort_values('MAE').reset_index(drop=True)
print('=' * 60)
print('COMPARAÇÃO FINAL — MODELOS DE REGRESSÃO')
print('=' * 60)
print(comparison_df.to_string(index=False))
print()
print(f'Melhor modelo (menor MAE): {comparison_df.iloc[0]["Modelo"]}')
print(f'Pior modelo  (maior MAE): {comparison_df.iloc[-1]["Modelo"]}')

# --- GRÁFICO COMPARATIVO ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

cores = ['#2ecc71' if i == 0 else '#e74c3c' if i == len(comparison_df)-1 else '#3498db'
         for i in range(len(comparison_df))]

axes[0].barh(comparison_df['Modelo'], comparison_df['MAE'], color=cores)
axes[0].set_title('MAE por Modelo (menor é melhor)', fontweight='bold')
axes[0].set_xlabel('MAE')
for i, v in enumerate(comparison_df['MAE']):
    axes[0].text(v + 0.5, i, f'{v:.2f}', va='center', fontsize=9)

axes[1].barh(comparison_df['Modelo'], comparison_df['RMSE'], color=cores)
axes[1].set_title('RMSE por Modelo (menor é melhor)', fontweight='bold')
axes[1].set_xlabel('RMSE')
for i, v in enumerate(comparison_df['RMSE']):
    axes[1].text(v + 0.5, i, f'{v:.2f}', va='center', fontsize=9)

plt.suptitle('Comparação de Desempenho — Modelos de Regressão', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

# --- VARIÁVEIS MAIS RELEVANTES (Regressão Linear Múltipla) ---
print('\n--- VARIÁVEIS MAIS RELEVANTES (Reg. Linear Múltipla) ---')
pipe_lm.fit(X_reg, y_reg)
feature_names_out = pipe_lm.named_steps['prep'].get_feature_names_out()
coefs = pipe_lm.named_steps['model'].coef_
feat_imp = pd.DataFrame({'Feature': feature_names_out, 'Coef': coefs})
feat_imp['Abs'] = feat_imp['Coef'].abs()
feat_imp = feat_imp.sort_values('Abs', ascending=False).head(10)
print(feat_imp[['Feature', 'Coef']].to_string(index=False))


# ## 4.2.5 — Curvas de Aprendizagem dos 2 Melhores Modelos de Regressão
# 
# As curvas de aprendizagem (*training score* vs *validation score*) permitem diagnosticar situações de **overfitting** (modelo memoriza os dados de treino) ou **underfitting** (modelo demasiado simples). Apresentamos as curvas para os dois modelos com melhor desempenho.

# In[ ]:


# =============================================================
# 4.2.5 — CURVAS DE APRENDIZAGEM DOS 2 MELHORES MODELOS
# =============================================================
from sklearn.model_selection import learning_curve

# Os 2 melhores modelos (por MAE k-fold): Rede Neuronal (Profunda) e Árvore.
# Como a NN não é sklearn-compatível para learning_curve nativo,
# usamos sklearn.model_selection.learning_curve nos modelos sklearn.
# Para a NN, as curvas de treino/validação já foram produzidas nas células anteriores.

# --- 2 melhores modelos sklearn ---
melhores = [
    ('Árvore de Regressão', pipe_tree),
    ('Reg. Linear Múltipla', pipe_lm),
]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, (nome, pipeline) in zip(axes, melhores):
    train_sizes, train_scores, val_scores = learning_curve(
        pipeline, X_reg, y_reg,
        cv=kf5,
        scoring='neg_mean_absolute_error',
        train_sizes=np.linspace(0.1, 1.0, 8),
        n_jobs=-1
    )
    train_mean = -train_scores.mean(axis=1)
    train_std  = train_scores.std(axis=1)
    val_mean   = -val_scores.mean(axis=1)
    val_std    = val_scores.std(axis=1)

    ax.plot(train_sizes, train_mean, 'o-', color='#2980b9', label='Treino')
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15, color='#2980b9')
    ax.plot(train_sizes, val_mean, 's-', color='#e74c3c', label='Validação')
    ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.15, color='#e74c3c')
    ax.set_title(f'Curva de Aprendizagem\n{nome}', fontweight='bold')
    ax.set_xlabel('Tamanho do Conjunto de Treino')
    ax.set_ylabel('MAE')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.suptitle('Curvas de Aprendizagem — 2 Melhores Modelos de Regressão', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

print('INTERPRETAÇÃO:')
print('- Se treino e validação convergem → treino eficiente, sem over/underfitting.')
print('- Se validação >> treino → overfitting (modelo memoriza, não generaliza).')
print('- Se ambas elevadas e próximas → underfitting (modelo demasiado simples).')


# ## 4.2.6 — Testes Estatísticos de Regressão (α = 5%)
# 
# Para verificar se a diferença de desempenho entre os dois melhores modelos é **estatisticamente significativa**, utilizamos o **teste de Wilcoxon signed-rank** (teste não paramétrico para amostras emparelhadas). Este teste é adequado pois os erros de k-fold são dependentes (partilham dados).

# In[ ]:


# =============================================================
# 4.2.6 — TESTES ESTATÍSTICOS (WILCOXON) — REGRESSÃO
# =============================================================
from scipy.stats import wilcoxon

alpha = 0.05

# Obter MAE por fold para os 2 melhores modelos
cv_tree_mae  = cross_validate(pipe_tree, X_reg, y_reg, cv=kf5,
                              scoring='neg_mean_absolute_error')['test_score']
cv_lm_mae    = cross_validate(pipe_lm,   X_reg, y_reg, cv=kf5,
                              scoring='neg_mean_absolute_error')['test_score']

mae_folds_tree = -cv_tree_mae
mae_folds_lm   = -cv_lm_mae

print('=' * 65)
print('TESTE DE WILCOXON SIGNED-RANK — Árvore vs Reg. Linear Múltipla')
print('=' * 65)
print(f'MAE por fold (Árvore):       {[round(v,4) for v in mae_folds_tree]}')
print(f'MAE por fold (Reg. Múltipla):{[round(v,4) for v in mae_folds_lm]}')
print()

stat, p_value = wilcoxon(mae_folds_tree, mae_folds_lm)

print(f'Estatística W: {stat:.4f}')
print(f'P-value:       {p_value:.6f}')
print()

if p_value < alpha:
    melhor = 'Árvore de Regressão' if mae_folds_tree.mean() < mae_folds_lm.mean() else 'Reg. Linear Múltipla'
    print(f'CONCLUSÃO: A diferença é ESTATISTICAMENTE SIGNIFICATIVA (p={p_value:.4f} < α={alpha}).')
    print(f'           O modelo com melhor desempenho é: {melhor}.')
else:
    print(f'CONCLUSÃO: A diferença NÃO é estatisticamente significativa (p={p_value:.4f} >= α={alpha}).')
    print('           Não se pode afirmar que um modelo é superior ao outro.')

# Gráfico de distribuição MAE por fold
fig, ax = plt.subplots(figsize=(8, 5))
x_pos = np.arange(1, kf5.n_splits + 1)
ax.plot(x_pos, mae_folds_tree, 'o-', label='Árvore de Regressão', color='#2980b9')
ax.plot(x_pos, mae_folds_lm,   's-', label='Reg. Linear Múltipla', color='#e74c3c')
ax.set_xlabel('Fold')
ax.set_ylabel('MAE')
ax.set_title('MAE por Fold — Comparação dos 2 Melhores Modelos', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# ---
# # 4.3 — Modelos de Classificação
# 
# Nesta secção o objetivo é **prever o nível de ocupação da rede** para cada PTD.
# Com base na variável `Util_Decimal`, criamos um novo atributo `utilizRede` com três classes: **baixo**, **médio** e **alto**.

# ## 4.3.0 — Criação da variável `utilizRede`
# 
# A discretização é feita com base em **quantis** (terços), garantindo classes equilibradas (~33% cada), o que é essencial para evitar desequilíbrio de classes (*class imbalance*) que penaliza os modelos de classificação.

# In[ ]:


# =============================================================
# 4.3.0 — CRIAR VARIÁVEL utilizRede
# =============================================================
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, classification_report, confusion_matrix,
                             ConfusionMatrixDisplay)
from scipy.stats import wilcoxon

# --- Verificar a distribuição de Util_Decimal ---
print('Descrição de Util_Decimal:')
print(df['Util_Decimal'].describe())
print()

# --- Discretização por quantis (terços) ---
q33 = df['Util_Decimal'].quantile(0.333)
q67 = df['Util_Decimal'].quantile(0.667)

print(f'Limiar baixo  (Q33): {q33:.4f}')
print(f'Limiar alto   (Q67): {q67:.4f}')

def classifica_rede(val):
    if val <= q33:
        return 'baixo'
    elif val <= q67:
        return 'médio'
    else:
        return 'alto'

df['utilizRede'] = df['Util_Decimal'].apply(classifica_rede)

print('Distribuição de utilizRede:')
print(df['utilizRede'].value_counts())
print()
print('Proporções:')
print(df['utilizRede'].value_counts(normalize=True).round(4))

# Gráfico
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

df['Util_Decimal'].hist(bins=50, ax=axes[0], color='#3498db', edgecolor='white')
axes[0].axvline(q33, color='#e67e22', linestyle='--', label=f'Q33={q33:.3f}')
axes[0].axvline(q67, color='#e74c3c', linestyle='--', label=f'Q67={q67:.3f}')
axes[0].set_title('Distribuição de Util_Decimal', fontweight='bold')
axes[0].set_xlabel('Util_Decimal')
axes[0].legend()

counts = df['utilizRede'].value_counts().reindex(['baixo', 'médio', 'alto'])
cores_classes = ['#2ecc71', '#f39c12', '#e74c3c']
axes[1].bar(counts.index, counts.values, color=cores_classes, edgecolor='white')
axes[1].set_title('Distribuição de utilizRede', fontweight='bold')
axes[1].set_xlabel('Classe')
axes[1].set_ylabel('Nº de PTDs')
for i, v in enumerate(counts.values):
    axes[1].text(i, v + 100, str(v), ha='center', fontweight='bold')

plt.suptitle('Discretização de Util_Decimal → utilizRede', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()


# In[ ]:


# =============================================================
# PREPARAR X e y PARA CLASSIFICAÇÃO
# =============================================================
# Definir target e features
alvo_clf = 'utilizRede'
cols_excluir = [alvo_clf, 'Util_Decimal', 'PFolga_PTD']  # remover o target e correlatas
# Remover também as outras colunas diretamente derivadas do target para evitar data leakage
leak_cols = [c for c in ['Nível de Utilização [%]'] if c in df.columns]
cols_excluir += leak_cols
cols_excluir = [c for c in cols_excluir if c in df.columns]

X_clf = df.drop(columns=cols_excluir)
y_clf = df[alvo_clf]

# Codificar o target como inteiro ordenado
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_clf_enc = le.fit_transform(y_clf)
print('Classes:', le.classes_)
print('y_clf_enc distribuição:', pd.Series(y_clf_enc).value_counts().sort_index().to_dict())

# Preprocessor para classificação (igual ao de regressão mas sobre X_clf)
num_cols_clf = X_clf.select_dtypes(include=['number']).columns.tolist()
cat_cols_clf = X_clf.select_dtypes(exclude=['number']).columns.tolist()
ord_cols_clf = [c for c in ['Nível de Utilização [%]'] if c in cat_cols_clf]
cat_cols_clf = [c for c in cat_cols_clf if c not in ord_cols_clf]

preprocessor_clf = ColumnTransformer(transformers=[
    ('numeros', RobustScaler(), num_cols_clf),
    ('texto',   OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols_clf)
], remainder='drop')

kf_clf = KFold(n_splits=5, shuffle=True, random_state=42)
print('Preprocessor pronto.')
print(f'X_clf shape: {X_clf.shape}')


# ## 4.3.1a — Árvore de Decisão

# In[ ]:


# =============================================================
# 4.3.1a — ÁRVORE DE DECISÃO (K-FOLD)
# =============================================================
from sklearn.tree import DecisionTreeClassifier, plot_tree

pipe_dt = Pipeline([
    ('prep', preprocessor_clf),
    ('model', DecisionTreeClassifier(max_depth=6, min_samples_leaf=10,
                                     class_weight='balanced', random_state=42))
])

scoring_clf = {
    'accuracy':  'accuracy',
    'precision': 'precision_weighted',
    'recall':    'recall_weighted',
    'f1':        'f1_weighted'
}

cv_dt = cross_validate(pipe_dt, X_clf, y_clf_enc, cv=kf_clf, scoring=scoring_clf, return_train_score=True)

print('=' * 55)
print('ÁRVORE DE DECISÃO — RESULTADOS K-FOLD (5 folds)')
print('=' * 55)
print(f'Accuracy  — Média: {cv_dt["test_accuracy"].mean():.4f}  DP: {cv_dt["test_accuracy"].std():.4f}')
print(f'Precision — Média: {cv_dt["test_precision"].mean():.4f}  DP: {cv_dt["test_precision"].std():.4f}')
print(f'Recall    — Média: {cv_dt["test_recall"].mean():.4f}  DP: {cv_dt["test_recall"].std():.4f}')
print(f'F1-score  — Média: {cv_dt["test_f1"].mean():.4f}  DP: {cv_dt["test_f1"].std():.4f}')

# Treinar para visualizar a árvore
pipe_dt.fit(X_clf, y_clf_enc)
feat_names_dt = pipe_dt.named_steps['prep'].get_feature_names_out()

plt.figure(figsize=(20, 8))
plot_tree(pipe_dt.named_steps['model'], feature_names=feat_names_dt,
          class_names=le.classes_, filled=True, fontsize=7, max_depth=3)
plt.title('Árvore de Decisão (max_depth=6, visualização até depth=3)', fontweight='bold')
plt.tight_layout()
plt.show()


# ## 4.3.1b — Rede Neuronal (Classificação)

# In[ ]:


# =============================================================
# 4.3.1b — REDE NEURONAL PARA CLASSIFICAÇÃO (MLPClassifier sklearn)
# 3 configurações + curvas de loss + análise early stopping
# =============================================================
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

X_clf_pp = preprocessor_clf.fit_transform(X_clf)

# Split estratificado
X_tr, X_te, y_tr, y_te = train_test_split(
    X_clf_pp, y_clf_enc,
    test_size=0.2, random_state=42, stratify=y_clf_enc
)
X_tr_f, X_val_f, y_tr_f, y_val_f = train_test_split(
    X_tr, y_tr,
    test_size=0.2, random_state=42, stratify=y_tr
)
print(f"Treino: {X_tr_f.shape} | Validação: {X_val_f.shape} | Teste: {X_te.shape}")

configs_clf_nn = {
    'Simples':      MLPClassifier(hidden_layer_sizes=(64,),           max_iter=100, random_state=42, early_stopping=True, validation_fraction=0.2, learning_rate_init=0.001),
    'Profundo':     MLPClassifier(hidden_layer_sizes=(256, 128, 64),  max_iter=100, random_state=42, early_stopping=True, validation_fraction=0.2, learning_rate_init=0.001),
    'Regularizado': MLPClassifier(hidden_layer_sizes=(128, 64),       max_iter=100, random_state=42, early_stopping=True, validation_fraction=0.2, learning_rate_init=0.001, alpha=0.001),
}

histories_clf = {}
models_clf    = {}
results_clf_nn = []

for nome, m in configs_clf_nn.items():
    print(f"\nA treinar NN clf: {nome}")
    m.fit(X_tr_f, y_tr_f)
    histories_clf[nome] = m.loss_curve_
    models_clf[nome]    = m
    preds = m.predict(X_te)
    acc  = accuracy_score(y_te, preds)
    f1_w = f1_score(y_te, preds, average='weighted', zero_division=0)
    results_clf_nn.append({'Config': nome, 'Accuracy': round(acc,4), 'F1-weighted': round(f1_w,4), 'Épocas': m.n_iter_})
    print(f"  Acc={acc:.4f}  F1={f1_w:.4f}  Épocas={m.n_iter_}")

nn_results_df = pd.DataFrame(results_clf_nn).sort_values('F1-weighted', ascending=False)
print("\nResumo NN Classificação:")
print(nn_results_df.to_string(index=False))

# Curvas de Loss
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, (nome, lc) in zip(axes, histories_clf.items()):
    ax.plot(lc, color='#2980b9', label='Treino Loss')
    ax.set_title(f'Loss — {nome}', fontweight='bold')
    ax.set_xlabel('Épocas'); ax.set_ylabel('Loss')
    ax.legend(); ax.grid(True, alpha=0.3)
plt.suptitle('Curvas de Loss — Rede Neuronal (Classificação)', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

best_nn_clf = nn_results_df.iloc[0]['Config']
best_nn_acc = nn_results_df.iloc[0]['Accuracy']
print(f"\nMelhor config NN: {best_nn_clf}  Acc={best_nn_acc:.4f}")

# Guardar para métricas comparativas (4.3.2)
best_nn_preds = models_clf[best_nn_clf].predict(X_te)


# ## 4.3.1c — SVM (Classificação)

# In[ ]:


# =============================================================
# 4.3.1c — SVM PARA CLASSIFICAÇÃO (OTIMIZAÇÃO DE KERNEL)
# =============================================================
from sklearn.svm import SVC

pipe_svc = Pipeline([
    ('prep', preprocessor_clf),
    ('model', SVC(probability=False, cache_size=2000, max_iter=5000, random_state=42))
])

svc_params = {'model__kernel': ['linear', 'rbf']}

svc_scoring = {
    'accuracy':  'accuracy',
    'f1':        'f1_weighted'
}

svc_grid = GridSearchCV(pipe_svc, svc_params, cv=kf_clf,
                        scoring=svc_scoring, refit='f1',
                        n_jobs=-1, verbose=1)
svc_grid.fit(X_clf, y_clf_enc)

best_idx_svc = svc_grid.best_index_
svc_f1  = svc_grid.cv_results_['mean_test_f1'][best_idx_svc]
svc_acc = svc_grid.cv_results_['mean_test_accuracy'][best_idx_svc]

print('='*55)
print('SVM CLASSIFICAÇÃO — RESULTADOS')
print('='*55)
print(f'Melhor kernel: {svc_grid.best_params_}')
print(f'F1-weighted (k-fold): {svc_f1:.4f}')
print(f'Accuracy    (k-fold): {svc_acc:.4f}')

# Guardar scores por fold para testes estatísticos
best_svc_pipe = svc_grid.best_estimator_
cv_svc_final = cross_validate(best_svc_pipe, X_clf, y_clf_enc, cv=kf_clf,
                              scoring=scoring_clf, return_train_score=True)
print(f'Precision — Média: {cv_svc_final["test_precision"].mean():.4f}  DP: {cv_svc_final["test_precision"].std():.4f}')
print(f'Recall    — Média: {cv_svc_final["test_recall"].mean():.4f}  DP: {cv_svc_final["test_recall"].std():.4f}')
print(f'F1-score  — Média: {cv_svc_final["test_f1"].mean():.4f}  DP: {cv_svc_final["test_f1"].std():.4f}')


# ## 4.3.1d — KNN — K-Vizinhos-Mais-Próximos

# In[ ]:


# =============================================================
# 4.3.1d — KNN (OTIMIZAÇÃO DO PARÂMETRO K)
# =============================================================
from sklearn.neighbors import KNeighborsClassifier

k_values = [3, 5, 7, 11, 15, 21]
knn_results = []

for k in k_values:
    pipe_knn = Pipeline([
        ('prep', preprocessor_clf),
        ('model', KNeighborsClassifier(n_neighbors=k, n_jobs=-1))
    ])
    cv_k = cross_validate(pipe_knn, X_clf, y_clf_enc, cv=kf_clf, scoring=scoring_clf)
    knn_results.append({
        'K': k,
        'Accuracy':  round(cv_k['test_accuracy'].mean(), 4),
        'Precision': round(cv_k['test_precision'].mean(), 4),
        'Recall':    round(cv_k['test_recall'].mean(), 4),
        'F1':        round(cv_k['test_f1'].mean(), 4),
    })
    print(f'K={k:2d}  Acc={cv_k["test_accuracy"].mean():.4f}  F1={cv_k["test_f1"].mean():.4f}')

knn_df = pd.DataFrame(knn_results)
best_k = knn_df.sort_values('F1', ascending=False).iloc[0]['K']
print(f'\nMelhor K: {int(best_k)}')

# Gráfico K vs métricas
plt.figure(figsize=(10, 5))
plt.plot(knn_df['K'], knn_df['Accuracy'],  'o-', label='Accuracy',  color='#2980b9')
plt.plot(knn_df['K'], knn_df['F1'],        's-', label='F1-score',  color='#e74c3c')
plt.plot(knn_df['K'], knn_df['Precision'], '^-', label='Precision', color='#27ae60')
plt.plot(knn_df['K'], knn_df['Recall'],    'D-', label='Recall',    color='#f39c12')
plt.axvline(best_k, color='grey', linestyle='--', alpha=0.7, label=f'Melhor K={int(best_k)}')
plt.title('KNN — Desempenho por Valor de K', fontweight='bold')
plt.xlabel('K'); plt.ylabel('Métrica')
plt.legend(); plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()

# Treinar modelo final com melhor K
pipe_knn_best = Pipeline([
    ('prep', preprocessor_clf),
    ('model', KNeighborsClassifier(n_neighbors=int(best_k), n_jobs=-1))
])
cv_knn_best = cross_validate(pipe_knn_best, X_clf, y_clf_enc, cv=kf_clf,
                             scoring=scoring_clf, return_train_score=True)
print(f'KNN (K={int(best_k)}) — Accuracy: {cv_knn_best["test_accuracy"].mean():.4f}')
print(f'KNN (K={int(best_k)}) — F1:       {cv_knn_best["test_f1"].mean():.4f}')


# ## 4.3.2 — Comparação de Métricas por Modelo
# 
# Média e desvio padrão de **Accuracy**, **Precision**, **Recall** e **F1-score** (ponderados por classe) para todos os modelos.

# In[ ]:


# =============================================================
# 4.3.2 — TABELA COMPARATIVA DE MÉTRICAS (CLASSIFICAÇÃO)
# =============================================================

# Recolher métricas k-fold para todos os modelos
# (Árvore de Decisão, SVM, KNN já calculados acima)
# Rede Neuronal: avaliação no conjunto de teste

def get_cv_stats(cv_results, prefix='test_'):
    return {
        'Accuracy':  (cv_results[f'{prefix}accuracy'].mean(),  cv_results[f'{prefix}accuracy'].std()),
        'Precision': (cv_results[f'{prefix}precision'].mean(), cv_results[f'{prefix}precision'].std()),
        'Recall':    (cv_results[f'{prefix}recall'].mean(),    cv_results[f'{prefix}recall'].std()),
        'F1':        (cv_results[f'{prefix}f1'].mean(),        cv_results[f'{prefix}f1'].std()),
    }

stats_dt  = get_cv_stats(cv_dt)
stats_svc = get_cv_stats(cv_svc_final)
stats_knn = get_cv_stats(cv_knn_best)

# NN: do conjunto de teste (melhor config)
# (best_nn_preds já foi calculado na célula anterior com models_clf[best_nn_clf].predict(X_te))
stats_nn = {
    'Accuracy':  (accuracy_score(y_te, best_nn_preds), 0.0),
    'Precision': (precision_score(y_te, best_nn_preds, average='weighted', zero_division=0), 0.0),
    'Recall':    (recall_score(y_te, best_nn_preds, average='weighted', zero_division=0), 0.0),
    'F1':        (f1_score(y_te, best_nn_preds, average='weighted', zero_division=0), 0.0),
}

modelos_dict = {
    'Árvore de Decisão': stats_dt,
    f'Rede Neuronal ({best_nn_clf})': stats_nn,
    'SVM': stats_svc,
    f'KNN (K={int(best_k)})': stats_knn,
}

rows = []
for nome, stats in modelos_dict.items():
    rows.append({
        'Modelo': nome,
        'Acc μ':  f'{stats["Accuracy"][0]:.4f}',  'Acc σ':  f'{stats["Accuracy"][1]:.4f}',
        'Prec μ': f'{stats["Precision"][0]:.4f}', 'Prec σ': f'{stats["Precision"][1]:.4f}',
        'Rec μ':  f'{stats["Recall"][0]:.4f}',    'Rec σ':  f'{stats["Recall"][1]:.4f}',
        'F1 μ':   f'{stats["F1"][0]:.4f}',        'F1 σ':   f'{stats["F1"][1]:.4f}',
    })

metrics_df = pd.DataFrame(rows)
print('=' * 90)
print('COMPARAÇÃO FINAL — MODELOS DE CLASSIFICAÇÃO (μ=média, σ=desvio padrão)')
print('=' * 90)
print(metrics_df.to_string(index=False))

# Gráfico de barras comparativo
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
metricas = ['Accuracy', 'Precision', 'Recall', 'F1']
cores_mod = ['#3498db', '#e74c3c', '#27ae60', '#f39c12']
nomes_mod = list(modelos_dict.keys())

for ax, metrica in zip(axes.flatten(), metricas):
    valores = [modelos_dict[n][metrica][0] for n in nomes_mod]
    erros   = [modelos_dict[n][metrica][1] for n in nomes_mod]
    bars = ax.bar(nomes_mod, valores, yerr=erros, capsize=5, color=cores_mod, alpha=0.85, edgecolor='white')
    ax.set_title(metrica, fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.set_ylabel(metrica)
    ax.tick_params(axis='x', rotation=20)
    for bar, v in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.02, f'{v:.3f}', ha='center', fontsize=9)

plt.suptitle('Comparação de Métricas — Modelos de Classificação', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()


# ## 4.3.3 — Importância de Features (Árvore de Decisão)
# 
# Apresentamos as features mais relevantes identificadas pela Árvore de Decisão e comparamos com as correlações identificadas na secção 4.1.

# In[ ]:


# =============================================================
# 4.3.3 — FEATURE IMPORTANCE DA ÁRVORE DE DECISÃO
# =============================================================
feat_names_clf_dt = pipe_dt.named_steps['prep'].get_feature_names_out()
importances_dt = pipe_dt.named_steps['model'].feature_importances_

fi_df = pd.DataFrame({'Feature': feat_names_clf_dt, 'Importância': importances_dt})
fi_df = fi_df.sort_values('Importância', ascending=False).reset_index(drop=True)

top_n = 15
print(f'TOP {top_n} FEATURES — Árvore de Decisão (Classificação):')
print(fi_df.head(top_n).to_string(index=False))

# Gráfico de importância
fig, ax = plt.subplots(figsize=(10, 7))
top_fi = fi_df.head(top_n)
ax.barh(top_fi['Feature'][::-1], top_fi['Importância'][::-1], color='#3498db', edgecolor='white')
ax.set_title(f'Top {top_n} Features — Árvore de Decisão (utilizRede)', fontweight='bold')
ax.set_xlabel('Importância (Gini)')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

# Comparação com correlações
print('\n--- CORRELAÇÕES COM Util_Decimal (EDA) ---')
corrs_util = df.select_dtypes(include='number').corr()['Util_Decimal'].abs().drop('Util_Decimal')
print(corrs_util.sort_values(ascending=False).head(10).to_string())
print()
print('DISCUSSÃO:')
print('As variáveis com maior importância na árvore devem, em geral, corresponder')
print('às variáveis com maior correlação com Util_Decimal identificadas na EDA.')
print('Divergências podem indicar interações não lineares captadas pela árvore.')


# ## 4.3.4 — Testes Estatísticos (Classificação, α = 5%)
# 
# Comparamos os dois modelos com melhor desempenho usando o **teste de Wilcoxon signed-rank** sobre os F1-scores de cada fold.

# In[ ]:


# =============================================================
# 4.3.4 — TESTES ESTATÍSTICOS (DOIS MELHORES MODELOS)
# =============================================================
from scipy.stats import wilcoxon

alpha = 0.05

# F1 por fold: Árvore vs SVM vs KNN
f1_dt  = cv_dt['test_f1']
f1_svc = cv_svc_final['test_f1']
f1_knn = cv_knn_best['test_f1']

# Determinar os 2 melhores (por média de F1)
ranking = sorted([
    ('Árvore de Decisão', f1_dt.mean(), f1_dt),
    ('SVM', f1_svc.mean(), f1_svc),
    (f'KNN (K={int(best_k)})', f1_knn.mean(), f1_knn)
], key=lambda x: -x[1])

nome1, media1, scores1 = ranking[0]
nome2, media2, scores2 = ranking[1]

print('=' * 65)
print(f'TESTE DE WILCOXON: {nome1} vs {nome2}')
print('=' * 65)
print(f'F1 médio {nome1}: {media1:.4f}  {[round(v,4) for v in scores1]}')
print(f'F1 médio {nome2}: {media2:.4f}  {[round(v,4) for v in scores2]}')

try:
    stat, p_value = wilcoxon(scores1, scores2)
    print(f'\nEstatística W: {stat:.4f}')
    print(f'P-value:       {p_value:.6f}')
    if p_value < alpha:
        print(f'\nCONCLUSÃO: Diferença SIGNIFICATIVA (p={p_value:.4f} < α={alpha}).')
        print(f'           Melhor modelo: {nome1}')
    else:
        print(f'\nCONCLUSÃO: Diferença NÃO significativa (p={p_value:.4f} >= α={alpha}).')
        print('           Não se pode afirmar que um é superior ao outro.')
except ValueError as e:
    print(f'Aviso: {e}')
    print('Os scores são idênticos — o teste não é aplicável.')

# Gráfico de boxplot por fold
fig, ax = plt.subplots(figsize=(8, 5))
data_box = [scores1, scores2]
ax.boxplot(data_box, tick_labels=[nome1, nome2], patch_artist=True,
           boxprops=dict(facecolor='#3498db', alpha=0.7),
           medianprops=dict(color='#e74c3c', linewidth=2))
ax.set_ylabel('F1-score (por fold)')
ax.set_title(f'Distribuição F1 por Fold — {nome1} vs {nome2}', fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout(); plt.show()


# ## 4.3.5 — Curvas de Aprendizagem (Melhor e Pior Modelo)
# 
# As curvas de aprendizagem permitem avaliar a eficiência do treino e diagnosticar overfitting/underfitting.

# In[ ]:


# =============================================================
# 4.3.5 — CURVAS DE APRENDIZAGEM (MELHOR E PIOR)
# =============================================================
from sklearn.model_selection import learning_curve

# Identificar melhor e pior (excluindo NN por incompatibilidade com learning_curve)
sk_ranking = sorted([
    ('Árvore de Decisão', f1_dt.mean(), pipe_dt),
    ('SVM', f1_svc.mean(), best_svc_pipe),
    (f'KNN (K={int(best_k)})', f1_knn.mean(), pipe_knn_best)
], key=lambda x: -x[1])

melhor_nome, melhor_score, melhor_pipe = sk_ranking[0]
pior_nome,   pior_score,   pior_pipe   = sk_ranking[-1]

print(f'Melhor modelo: {melhor_nome} (F1={melhor_score:.4f})')
print(f'Pior modelo:   {pior_nome}   (F1={pior_score:.4f})')

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, (nome, pipe) in zip(axes, [(melhor_nome, melhor_pipe), (pior_nome, pior_pipe)]):
    train_sizes, train_scores, val_scores = learning_curve(
        pipe, X_clf, y_clf_enc,
        cv=kf_clf, scoring='f1_weighted',
        train_sizes=np.linspace(0.1, 1.0, 8),
        n_jobs=-1
    )
    tr_mean = train_scores.mean(axis=1)
    tr_std  = train_scores.std(axis=1)
    vl_mean = val_scores.mean(axis=1)
    vl_std  = val_scores.std(axis=1)

    ax.plot(train_sizes, tr_mean, 'o-', color='#2980b9', label='Treino')
    ax.fill_between(train_sizes, tr_mean-tr_std, tr_mean+tr_std, alpha=0.15, color='#2980b9')
    ax.plot(train_sizes, vl_mean, 's-', color='#e74c3c', label='Validação')
    ax.fill_between(train_sizes, vl_mean-vl_std, vl_mean+vl_std, alpha=0.15, color='#e74c3c')
    ax.set_title(f'Curva de Aprendizagem\n{nome}', fontweight='bold')
    ax.set_xlabel('Tamanho do Conjunto de Treino')
    ax.set_ylabel('F1-score')
    ax.legend(); ax.grid(True, alpha=0.3)

plt.suptitle('Curvas de Aprendizagem — Classificação (Melhor vs Pior)', fontsize=13, fontweight='bold')
plt.tight_layout(); plt.show()

# Matriz de confusão do melhor modelo
melhor_pipe.fit(X_clf, y_clf_enc)
X_tr2, X_te2, y_tr2, y_te2 = train_test_split(X_clf, y_clf_enc,
                                                test_size=0.2, random_state=42, stratify=y_clf_enc)
melhor_pipe.fit(X_tr2, y_tr2)
y_pred_best = melhor_pipe.predict(X_te2)

print(f'\nRelatório de Classificação — {melhor_nome}:')
print(classification_report(y_te2, y_pred_best, target_names=le.classes_))

cm = confusion_matrix(y_te2, y_pred_best)
disp = ConfusionMatrixDisplay(cm, display_labels=le.classes_)
fig, ax = plt.subplots(figsize=(7, 6))
disp.plot(ax=ax, colorbar=True, cmap='Blues')
ax.set_title(f'Matriz de Confusão — {melhor_nome}', fontweight='bold')
plt.show()


# ## 4.3.6 — Limitações e Estratégias de Melhoria
# 
# Com base nos resultados obtidos, identificam-se as principais limitações e propõem-se estratégias para melhorar o desempenho dos modelos:
# 
# ### Limitações dos Dados
# 1. **Desequilíbrio geográfico**: A concentração de PTDs no litoral pode enviesar os modelos para padrões urbanos, com pior generalização em zonas rurais.
# 2. **Ausência de dados temporais**: O dataset é estático — não captura variações sazonais (ex: pico de consumo no verão vs inverno).
# 3. **Valores estimados**: Variáveis derivadas (PFolga, D_PTD) dependem de pressupostos e introduzem erro de medição.
# 
# ### Limitações dos Modelos
# 1. **SVM com convergência lenta**: O SVR/SVC com datasets de 70k+ registos exige muita memória e tempo de computação, limitando a otimização dos hiperparâmetros.
# 2. **Rede Neuronal sem k-fold nativo**: A avaliação da NN baseia-se num split fixo, o que pode introduzir variância na estimativa do desempenho.
# 3. **Features de alta dimensionalidade**: O one-hot encoding de variáveis categóricas (Tipo Construtivo, Distrito) gera centenas de colunas esparsas.
# 
# ### Estratégias de Melhoria
# 1. **Engenharia de features**: Criar variáveis de densidade de PTDs por concelho ou índice de urbanização para capturar contexto geográfico.
# 2. **Ensemble methods**: Testar Random Forest ou Gradient Boosting (XGBoost) que geralmente superam árvores simples e SVM em datasets tabulares.
# 3. **Oversampling/SMOTE**: Para mitigar eventuais desequilíbrios de classes na classificação.
# 4. **Dados temporais**: Incorporar séries temporais de consumo para capturar padrões sazonais.
# 5. **Redução de dimensionalidade**: Aplicar PCA sobre as features one-hot antes de SVM para reduzir o espaço de features e acelerar o treino.
# 
