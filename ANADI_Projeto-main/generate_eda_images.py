import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor, plot_tree
import math

print("Carregando dataset...")
df = pd.read_excel('P2/PTD_level_dataset.xlsx')

# 1. Mapa Geografico
print("Gerando Mapa Geografico...")
df[["latitude", "longitude"]] = df["Coordenadas Geográficas"].str.split(",", expand=True)
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

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
sc = plt.scatter(
    df_mapa["lon_round"], 
    df_mapa["lat_round"], 
    c=df_mapa["quantidade"], 
    cmap="viridis",
    s=df_mapa["quantidade"] / df_mapa["quantidade"].max() * 200,
    alpha=0.8
)
plt.colorbar(sc, label="Quantidade")
plt.title("Distribuição de Registos Geográficos", fontsize=14, pad=15)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig('../dashboard/assets/mapa.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. Boxplots
print("Gerando Boxplots...")
numeric_df = df.select_dtypes(include=['number'])
num_cols = len(numeric_df.columns)
cols = 2
rows = math.ceil(num_cols / cols)
flierprops = dict(marker='o', markerfacecolor='black', markeredgecolor='none', markersize=3, alpha=0.1)

plt.figure(figsize=(16, 24))
for i, col in enumerate(numeric_df.columns):
    plt.subplot(rows, cols, i + 1)
    numeric_df[col].plot(kind='box', vert=False, flierprops=flierprops, fontsize=8)
    plt.title(f"Boxplot: {col}", fontsize=10)
plt.tight_layout()
plt.savefig('../dashboard/assets/boxplots.png', dpi=100, bbox_inches='tight')
plt.close()

# 3. Heatmap
print("Gerando Heatmap...")
plt.figure(figsize=(12, 10))
sns.heatmap(
    numeric_df.corr(), 
    annot=True,
    annot_kws={"size": 6},
    cmap='coolwarm',    
    fmt=".2f",           
    vmin=-1, vmax=1      
)
plt.title('Matriz de Correlação de Pearson', fontsize=14, pad=15)
plt.tight_layout()
plt.savefig('../dashboard/assets/heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# 4. Arvore de Decisao
print("Gerando Arvore de Decisao...")
# Quick pre-processing just to fit the tree
df['Pot_Geracao_kW'] = df['Pot_Geracao_kW'].fillna(0)
df['Geracao_per_Cliente'] = df['Geracao_per_Cliente'].fillna(0)
median_pot = df['Pot_Contratada_kVA'].median()
df['Pot_Contratada_kVA'] = df['Pot_Contratada_kVA'].fillna(median_pot)
df['PContratada_per_Cliente'] = df['PContratada_per_Cliente'].fillna(df['PContratada_per_Cliente'].median())
df.dropna(subset=['D_PTD', 'D_PTD_LED', 'Util_Decimal', 'PFolga_PTD'], inplace=True)

alvo = 'PFolga_PTD'
X = df.select_dtypes(include=['number']).drop(columns=[alvo])
y = df[alvo]

dt = DecisionTreeRegressor(max_depth=3, min_samples_split=10, min_samples_leaf=5, random_state=42)
dt.fit(X, y)

plt.figure(figsize=(20, 8))
plot_tree(dt, feature_names=X.columns, filled=True, fontsize=10, rounded=True)
plt.title("Árvore de Regressão (Max Depth = 3)", fontsize=16, pad=15)
plt.tight_layout()
plt.savefig('../dashboard/assets/arvore.png', dpi=200, bbox_inches='tight')
plt.close()

# 5. Histogramas (Distribuicao de Numericas)
print("Gerando Histogramas...")
numeric_df = df.select_dtypes(include=['number'])
numeric_df.hist(figsize=(16, 14), bins=30, edgecolor='black', color='#3498db')
plt.suptitle('Histogramas das Variáveis Numéricas (Deteção de Assimetria)', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('../dashboard/assets/histogramas.png', dpi=150, bbox_inches='tight')
plt.close()

print("Todas as imagens foram geradas com sucesso em dashboard/assets!")
