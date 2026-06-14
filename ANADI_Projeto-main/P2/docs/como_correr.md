# Como Correr o Dashboard Interativo (ANADI - Fase 2)

O dashboard interativo foi desenvolvido para funcionar sem dependências complexas (não requer frameworks pesados como React ou Angular), utilizando apenas HTML, CSS (Vanilla) e JavaScript puro com bibliotecas via CDN (Plotly e Chart.js).

## Pré-requisitos

Não é necessária a instalação de nenhum pacote (npm, pip, etc.) além de um navegador web moderno e uma forma de servir os ficheiros estáticos (HTML/CSS/JS).

### Opção 1: Live Server (Recomendado - VS Code)
Se utilizares o Visual Studio Code:
1. Instala a extensão **Live Server** (do autor Ritwick Dey).
2. Navega até à pasta principal do projeto onde se encontra a sub-pasta `dashboard`.
3. Clica com o botão direito sobre o ficheiro `dashboard/index.html`.
4. Seleciona a opção **"Open with Live Server"**.
5. O navegador abrirá automaticamente em `http://127.0.0.1:5500`.

### Opção 2: Python HTTP Server (Para Windows/Linux/Mac)
Dado que desenvolveste o projeto em Python, podes usar o servidor nativo:
1. Abre o terminal (Prompt de Comando ou PowerShell).
2. Navega para a pasta `dashboard` do projeto:
   ```bash
   cd caminho/para/o/projeto/dashboard
   ```
3. Inicia o servidor HTTP:
   ```bash
   python -m http.server 8080
   ```
4. Abre o teu browser e acede a [http://localhost:8080](http://localhost:8080).

## Navegação no Dashboard
- **Menu Lateral**: Usa o menu da esquerda para navegar pelas secções (Contexto, Análise Exploratória, Modelos de Regressão, Modelos de Classificação, Conclusões).
- **Interatividade (Zoom)**: Todos os Gráficos, Imagens e Tabelas Estatísticas têm capacidade de expansão. Basta **clicares** num elemento e ele abrirá no centro do ecrã com fundo escuro, otimizado para apresentações.
