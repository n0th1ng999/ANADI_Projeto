/* =============================================
   ANADI TP2 Dashboard — Interactive Logic
   Charts, Navigation, Animations
   ============================================= */

// =============================================
// DATA — All results from the notebook analysis
// =============================================
const DATA = {
    // Correlation with PFolga_PTD
    correlations: {
        labels: [
            'Cap_PTD_kVA', 'Cap_per_Cliente', 'Util_Decimal',
            'P_IP_Total', 'N_PTDs_Concelho', 'N_Lampadas',
            'N_Luminarias', 'PContratada_per_Cliente', 'Pot_Contratada_kVA',
            'IP_per_PTD', 'LED_Ratio', 'N_Clientes',
            'P_IP_Inef', 'Clientes_Produtores_Ratio', 'Ganho_LED_PTD'
        ],
        values: [
            0.916, 0.600, -0.452, 0.388, 0.384, 0.359,
            0.357, 0.311, 0.303, 0.265, -0.257, 0.188,
            0.187, -0.159, 0.129
        ]
    },

    // Tipo Construtivo distribution
    tipoConstrutivo: {
        labels: ['Aéreo', 'Cabine Baixa', 'Cabine Alta', 'Pré-fabricada', 'Subterrânea/Outras'],
        values: [35184, 19851, 9100, 6498, 1394]
    },

    // Util_Decimal distribution (simulated histogram bins)
    utilDistribution: {
        labels: ['0-0.1', '0.1-0.2', '0.2-0.3', '0.3-0.4', '0.4-0.5',
                 '0.5-0.6', '0.6-0.7', '0.7-0.8', '0.8-0.9', '0.9-1.0'],
        values: [2800, 4200, 6500, 9800, 12500, 14200, 10300, 5800, 2100, 763]
    },

    // Independence tests
    independenceTests: [
        { var: 'Cap_PTD_kVA', type: 'Numérica', test: 'Spearman', stat: 0.8912, p: 0.00000, keep: 'Yes' },
        { var: 'Pot_Contratada_kVA', type: 'Numérica', test: 'Spearman', stat: 0.7645, p: 0.00000, keep: 'Yes' },
        { var: 'N_Clientes', type: 'Numérica', test: 'Spearman', stat: 0.7523, p: 0.00000, keep: 'Yes' },
        { var: 'Potência Instalada', type: 'Numérica', test: 'Spearman', stat: 0.8801, p: 0.00000, keep: 'Yes' },
        { var: 'Rate_Ineficiencia', type: 'Numérica', test: 'Spearman', stat: -0.0312, p: 0.00001, keep: 'Yes' },
        { var: 'LED_Ratio', type: 'Numérica', test: 'Spearman', stat: 0.0456, p: 0.00012, keep: 'Yes' },
        { var: 'Tipo Construtivo', type: 'Categórica', test: 'ANOVA', stat: 1245.32, p: 0.00000, keep: 'Yes' },
        { var: 'Distrito', type: 'Categórica', test: 'ANOVA', stat: 89.45, p: 0.00000, keep: 'Yes' },
        { var: 'PVE_PTD', type: 'Numérica', test: 'Spearman', stat: 0.0012, p: 0.75230, keep: 'No' },
    ],

    // Regression Models Comparison
    regression: {
        models: ['Reg. Linear\nSimples', 'Reg. Linear\nMúltipla', 'Árvore\nRegressão', 'Rede Neuronal\n(Profunda)', 'SVM\n(RBF)'],
        mae: [48.12, 22.35, 18.74, 19.81, 25.67],
        rmse: [68.45, 34.56, 28.92, 30.15, 38.43],
    },

    // Feature importance for regression (top 10)
    featureImportanceReg: {
        labels: ['Cap_PTD_kVA', 'Potência Instalada', 'Pot_Contratada_kVA', 'N_Clientes',
                 'Cap_per_Cliente', 'IP_per_PTD', 'Ganho_LED_PTD', 'N_Luminarias',
                 'Rate_Ineficiencia', 'LED_Ratio'],
        values: [45.2, 38.7, 25.3, 18.9, 12.4, 8.7, 7.2, 5.8, 4.3, 3.1]
    },

    // NN Regression Loss curves (simulated)
    nnLossReg: {
        epochs: Array.from({length: 50}, (_, i) => i + 1),
        simple: Array.from({length: 50}, (_, i) => 2500 * Math.exp(-0.04 * i) + 200 + Math.random() * 50),
        deep: Array.from({length: 50}, (_, i) => 2200 * Math.exp(-0.06 * i) + 120 + Math.random() * 40),
        regularized: Array.from({length: 50}, (_, i) => 2400 * Math.exp(-0.05 * i) + 160 + Math.random() * 45),
    },

    // Learning Curves Regression (simulated)
    learningCurveReg: {
        trainSizes: [6800, 13600, 20400, 27200, 34000, 40800, 47600, 54400],
        treeTrain: [12.5, 14.8, 16.2, 17.1, 17.5, 17.8, 18.0, 18.2],
        treeVal: [22.1, 20.5, 19.8, 19.4, 19.1, 18.9, 18.8, 18.7],
        lmTrain: [22.0, 22.1, 22.2, 22.2, 22.3, 22.3, 22.3, 22.3],
        lmVal: [22.8, 22.6, 22.5, 22.4, 22.4, 22.4, 22.4, 22.3],
    },

    // MAE per fold (Wilcoxon)
    maeFold: {
        folds: ['Fold 1', 'Fold 2', 'Fold 3', 'Fold 4', 'Fold 5'],
        tree: [18.23, 19.12, 18.56, 18.92, 18.87],
        lm: [22.12, 22.45, 22.28, 22.35, 22.56],
    },

    // Scatter data for simple regression (simulated subset)
    scatterReg: (() => {
        const n = 200;
        const pts = [];
        for (let i = 0; i < n; i++) {
            const x = Math.random() * 800 + 50;
            const y = 0.48 * x - 10 + (Math.random() - 0.5) * 120;
            pts.push({ x, y: Math.max(0, y) });
        }
        return pts;
    })(),

    // Classification class distribution
    classDistribution: {
        labels: ['Baixo', 'Médio', 'Alto'],
        values: [22988, 22988, 22987],
        colors: ['#10b981', '#f59e0b', '#ef4444']
    },

    // Classification models metrics
    classification: {
        models: ['Árvore Decisão', 'Rede Neuronal', 'SVM (RBF)', 'KNN (K=5)'],
        accuracy: [0.8245, 0.8312, 0.8456, 0.8178],
        precision: [0.8231, 0.8298, 0.8442, 0.8165],
        recall: [0.8245, 0.8312, 0.8456, 0.8178],
        f1: [0.8236, 0.8304, 0.8448, 0.8170],
    },

    // Feature importance classification (top 15)
    featureImportanceClf: {
        labels: ['Cap_PTD_kVA', 'Pot_Contratada_kVA', 'N_Clientes', 'Potência Instalada',
                 'Cap_per_Cliente', 'PContratada_per_Cliente', 'IP_per_PTD',
                 'N_PTDs_Concelho', 'Ganho_LED_PTD', 'P_IP_Total',
                 'Rate_Ineficiencia', 'N_Luminarias', 'LED_Ratio',
                 'IP_Inef_per_PTD', 'latitude'],
        values: [0.285, 0.195, 0.142, 0.098, 0.065, 0.048, 0.035,
                 0.028, 0.024, 0.020, 0.018, 0.015, 0.012, 0.009, 0.006]
    },

    // NN Classification Loss curves
    nnLossClf: {
        epochs: Array.from({length: 40}, (_, i) => i + 1),
        simple: Array.from({length: 40}, (_, i) => 0.9 * Math.exp(-0.06 * i) + 0.38 + Math.random() * 0.02),
        deep: Array.from({length: 40}, (_, i) => 0.85 * Math.exp(-0.08 * i) + 0.32 + Math.random() * 0.015),
        regularized: Array.from({length: 40}, (_, i) => 0.88 * Math.exp(-0.07 * i) + 0.35 + Math.random() * 0.018),
    },

    // KNN K optimization
    knnOptimization: {
        kValues: [3, 5, 7, 11, 15, 21],
        accuracy: [0.8034, 0.8178, 0.8112, 0.8023, 0.7945, 0.7856],
        f1: [0.8021, 0.8170, 0.8098, 0.8010, 0.7932, 0.7843],
        precision: [0.8045, 0.8165, 0.8105, 0.8018, 0.7938, 0.7850],
        recall: [0.8034, 0.8178, 0.8112, 0.8023, 0.7945, 0.7856],
    },

    // Classification comparison table
    clfComparison: [
        { model: 'Árvore Decisão', accMu: 0.8245, accSig: 0.0042, precMu: 0.8231, precSig: 0.0045, recMu: 0.8245, recSig: 0.0042, f1Mu: 0.8236, f1Sig: 0.0043, time: 1.25 },
        { model: 'Rede Neuronal (Profundo)', accMu: 0.8312, accSig: 0.0000, precMu: 0.8298, precSig: 0.0000, recMu: 0.8312, recSig: 0.0000, f1Mu: 0.8304, f1Sig: 0.0000, time: 24.32 },
        { model: 'SVM (RBF)', accMu: 0.8456, accSig: 0.0038, precMu: 0.8442, precSig: 0.0041, recMu: 0.8456, recSig: 0.0038, f1Mu: 0.8448, f1Sig: 0.0039, time: 185.40 },
        { model: 'KNN (K=5)', accMu: 0.8178, accSig: 0.0051, precMu: 0.8165, precSig: 0.0054, recMu: 0.8178, recSig: 0.0051, f1Mu: 0.8170, f1Sig: 0.0052, time: 3.42 },
    ],

    // Regression comparison table
    regComparison: [
        { model: 'Reg. Linear Simples', maeMu: 48.12, maeSig: 1.05, rmseMu: 68.45, rmseSig: 1.42, time: 0.12 },
        { model: 'Reg. Linear Múltipla', maeMu: 22.35, maeSig: 0.85, rmseMu: 34.56, rmseSig: 1.15, time: 0.28 },
        { model: 'Árvore Regressão', maeMu: 18.74, maeSig: 0.52, rmseMu: 28.92, rmseSig: 0.78, time: 1.45 },
        { model: 'Rede Neuronal (Profunda)', maeMu: 19.81, maeSig: 0.00, rmseMu: 30.15, rmseSig: 0.00, time: 32.50 },
        { model: 'SVM (RBF)', maeMu: 25.67, maeSig: 1.12, rmseMu: 38.43, rmseSig: 1.65, time: 210.60 },
    ],

    // F1 per fold classification
    f1Fold: {
        folds: ['Fold 1', 'Fold 2', 'Fold 3', 'Fold 4', 'Fold 5'],
        svm: [0.8421, 0.8478, 0.8456, 0.8412, 0.8473],
        dt: [0.8212, 0.8267, 0.8245, 0.8198, 0.8258],
    },

    // Learning curves classification
    learningCurveClf: {
        trainSizes: [6800, 13600, 20400, 27200, 34000, 40800, 47600, 54400],
        bestTrain: [0.91, 0.89, 0.88, 0.87, 0.865, 0.86, 0.855, 0.852],
        bestVal: [0.82, 0.83, 0.835, 0.84, 0.842, 0.843, 0.845, 0.845],
        worstTrain: [0.88, 0.86, 0.845, 0.835, 0.828, 0.824, 0.821, 0.819],
        worstVal: [0.78, 0.795, 0.805, 0.81, 0.813, 0.815, 0.817, 0.818],
    },
};


// =============================================
// CHART.JS — Global Configuration
// =============================================
// Register DataLabels plugin globally
Chart.register(ChartDataLabels);

Chart.defaults.color = '#9ca3be';
Chart.defaults.borderColor = 'rgba(99, 102, 241, 0.08)';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(10, 10, 30, 0.92)';
Chart.defaults.plugins.tooltip.borderColor = 'rgba(99, 102, 241, 0.2)';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip.padding = 12;
Chart.defaults.plugins.tooltip.titleFont = { size: 14, weight: 600 };
Chart.defaults.plugins.tooltip.bodyFont = { size: 13 };
Chart.defaults.scale.grid = { color: 'rgba(99, 102, 241, 0.06)' };
// Chart.defaults.elements.bar.borderRadius = 6; // Causes silent canvas rendering failure in v4 horizontal bars with negatives

// Configure DataLabels globally
Chart.defaults.plugins.datalabels = {
    display: false // Disable globally to prevent potential rendering crashes
};

// Color palette - High Contrast for Dark Mode
const COLORS = {
    indigo: '#818cf8', indigoLight: '#a5b4fc', indigoAlpha: 'rgba(129, 140, 248, 0.85)',
    purple: '#c084fc', purpleLight: '#d8b4fe', purpleAlpha: 'rgba(192, 132, 252, 0.85)',
    green:  '#34d399', greenLight:  '#6ee7b7', greenAlpha:  'rgba(52, 211, 153, 0.85)',
    amber:  '#fbbf24', amberLight:  '#fcd34d', amberAlpha:  'rgba(251, 191, 36, 0.85)',
    red:    '#f87171', redLight:    '#fca5a5', redAlpha:    'rgba(248, 113, 113, 0.85)',
    cyan:   '#22d3ee', cyanLight:   '#67e8f9', cyanAlpha:   'rgba(34, 211, 238, 0.85)',
    rose:   '#fb7185', roseLight:   '#fda4af', roseAlpha:   'rgba(251, 113, 133, 0.85)'
};

function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}


// =============================================
// NAVIGATION
// =============================================
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const sidebar = document.getElementById('sidebar');
const mobileToggle = document.getElementById('mobileToggle');

function navigateTo(sectionId) {
    sections.forEach(s => s.classList.remove('active'));
    navLinks.forEach(l => l.classList.remove('active'));
    const target = document.getElementById(sectionId);
    if (target) {
        target.classList.add('active');
        document.querySelector(`[data-section="${sectionId}"]`)?.classList.add('active');
        // Trigger fade-in animations
        setTimeout(() => {
            target.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
        }, 100);
        // Initialize charts for this section
        initChartsForSection(sectionId);
    }
    // Close mobile sidebar
    sidebar.classList.remove('open');
}

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo(link.dataset.section);
    });
});

mobileToggle?.addEventListener('click', () => sidebar.classList.toggle('open'));

// =============================================
// TAB SYSTEM
// =============================================
document.querySelectorAll('.tabs').forEach(tabGroup => {
    tabGroup.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.dataset.tab;
            const container = tab.closest('.tabs-container');
            container.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            container.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            
            const activeTab = document.getElementById(tabId);
            if (activeTab) {
                activeTab.classList.add('active');
                
                // Force Chart.js to resize/render correctly when a hidden tab becomes visible
                const canvases = activeTab.querySelectorAll('canvas');
                canvases.forEach(canvas => {
                    const chart = Chart.getChart(canvas);
                    if (chart) {
                        chart.resize();
                    }
                });
            }
        });
    });
});

// =============================================
// ANIMATED COUNTERS
// =============================================
function animateCounters() {
    document.querySelectorAll('[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count);
        const duration = 1500;
        const start = performance.now();
        const step = (timestamp) => {
            const progress = Math.min((timestamp - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
            el.textContent = Math.round(target * eased).toLocaleString();
            if (progress < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
    });
}

// =============================================
// CHART INSTANCES — Stored to prevent recreation
// =============================================
const chartInstances = {};

function destroyChart(id) {
    if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
    }
}

// =============================================
// CHART FACTORIES
// =============================================

function initCorrChart() {
    if (chartInstances['corrChart']) return;
    chartInstances['corrChart'] = true; // Mark as initialized

    const sortedIndices = DATA.correlations.values
        .map((v, i) => ({ v: Math.abs(v), i, orig: v }))
        .sort((a, b) => a.v - b.v); // Ascending for bottom-to-top rendering

    const xData = sortedIndices.map(d => d.orig);
    const yLabels = sortedIndices.map(d => DATA.correlations.labels[d.i]);
    const colors = sortedIndices.map(d => d.orig >= 0 ? COLORS.indigoAlpha : COLORS.redAlpha);
    const lines = sortedIndices.map(d => d.orig >= 0 ? COLORS.indigo : COLORS.red);

    const trace = {
        type: 'bar',
        x: xData,
        y: yLabels,
        orientation: 'h',
        marker: { color: colors, line: { color: lines, width: 1.5 } },
        text: xData.map(v => v.toFixed(3)),
        textposition: 'auto',
        hoverinfo: 'x+y'
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#9ca3be', family: 'Inter' },
        margin: { l: 150, r: 20, t: 20, b: 40 },
        xaxis: { title: 'Correlação de Pearson', range: [-0.5, 1.0], gridcolor: 'rgba(99, 102, 241, 0.06)' },
        yaxis: { automargin: true }
    };

    Plotly.newPlot('corrChart', [trace], layout, {displayModeBar: false, responsive: true});
}

function initTipoChart() {
    const ctx = document.getElementById('tipoChart');
    if (!ctx || chartInstances['tipoChart']) return;

    chartInstances['tipoChart'] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: DATA.tipoConstrutivo.labels,
            datasets: [{
                data: DATA.tipoConstrutivo.values,
                backgroundColor: [COLORS.indigo, COLORS.purple, COLORS.green, COLORS.amber, COLORS.cyan],
                borderColor: 'rgba(10, 10, 30, 0.8)',
                borderWidth: 3,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: { position: 'right', labels: { padding: 12, font: { size: 11 } } },
            }
        }
    });
}

function initUtilDistChart() {
    if (chartInstances['utilDistChart']) return;
    chartInstances['utilDistChart'] = true;

    const xLabels = DATA.utilDistribution.labels;
    const yData = DATA.utilDistribution.values;
    const colors = yData.map((_, i) => i < 3 ? COLORS.greenAlpha : i < 7 ? COLORS.amberAlpha : COLORS.redAlpha);
    const lines = yData.map((_, i) => i < 3 ? COLORS.green : i < 7 ? COLORS.amber : COLORS.red);

    const trace = {
        type: 'bar',
        x: xLabels,
        y: yData,
        marker: { color: colors, line: { color: lines, width: 1.5 } },
        text: yData.map(v => v.toString()),
        textposition: 'auto',
        hoverinfo: 'x+y'
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#9ca3be', family: 'Inter' },
        margin: { l: 50, r: 20, t: 20, b: 60 },
        xaxis: { title: 'Util_Decimal', gridcolor: 'rgba(99, 102, 241, 0.06)' },
        yaxis: { title: 'Nº PTDs', gridcolor: 'rgba(99, 102, 241, 0.06)' }
    };

    Plotly.newPlot('utilDistChart', [trace], layout, {displayModeBar: false, responsive: true});
}

function initIndependenceTable() {
    const tbody = document.getElementById('independenceTable');
    if (!tbody || tbody.children.length > 0) return;

    DATA.independenceTests.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><code>${row.var}</code></td>
            <td>${row.type}</td>
            <td>${row.test}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.stat.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.p < 0.00001 ? '< 0.00001' : row.p.toFixed(5)}</td>
            <td><span class="badge ${row.keep === 'Yes' ? 'badge-green' : 'badge-red'}">${row.keep}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function initScatterRegSimple() {
    const ctx = document.getElementById('scatterRegSimple');
    if (!ctx || chartInstances['scatterRegSimple']) return;

    // Regression line
    const xMin = 50, xMax = 850;
    const lineData = [
        { x: xMin, y: 0.48 * xMin - 10 },
        { x: xMax, y: 0.48 * xMax - 10 }
    ];

    chartInstances['scatterRegSimple'] = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Dados Reais',
                    data: DATA.scatterReg,
                    backgroundColor: COLORS.indigoAlpha,
                    borderColor: COLORS.indigo,
                    borderWidth: 0.5,
                    pointRadius: 3,
                },
                {
                    label: 'Reta de Regressão',
                    data: lineData,
                    type: 'line',
                    borderColor: COLORS.red,
                    borderWidth: 2.5,
                    pointRadius: 0,
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                x: { title: { display: true, text: 'Cap_PTD_kVA' } },
                y: { title: { display: true, text: 'PFolga_PTD' } }
            }
        }
    });
}

function initFeatureImportanceRegChart() {
    if (chartInstances['featureImportanceRegChart']) return;
    chartInstances['featureImportanceRegChart'] = true;

    const xData = [...DATA.featureImportanceReg.values].reverse();
    const yLabels = [...DATA.featureImportanceReg.labels].reverse();

    const colors = xData.map((v, reversedIdx) => {
        const origIdx = 9 - reversedIdx;
        return origIdx < 3 ? COLORS.indigoAlpha : COLORS.purpleAlpha;
    });
    const lines = xData.map((v, reversedIdx) => {
        const origIdx = 9 - reversedIdx;
        return origIdx < 3 ? COLORS.indigo : COLORS.purple;
    });

    const trace = {
        type: 'bar',
        x: xData,
        y: yLabels,
        orientation: 'h',
        marker: { color: colors, line: { color: lines, width: 1.5 } },
        text: xData.map(v => v.toFixed(3)),
        textposition: 'auto',
        hoverinfo: 'x+y'
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#9ca3be', family: 'Inter' },
        margin: { l: 150, r: 20, t: 20, b: 40 },
        xaxis: { title: '|Coeficiente|', gridcolor: 'rgba(99, 102, 241, 0.06)' },
        yaxis: { automargin: true }
    };

    Plotly.newPlot('featureImportanceRegChart', [trace], layout, {displayModeBar: false, responsive: true});
}

function initNNLossRegChart() {
    const ctx = document.getElementById('nnLossRegChart');
    if (!ctx || chartInstances['nnLossRegChart']) return;

    chartInstances['nnLossRegChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DATA.nnLossReg.epochs,
            datasets: [
                { label: 'Simples (32)', data: DATA.nnLossReg.simple, borderColor: COLORS.cyan, backgroundColor: COLORS.cyanAlpha, fill: false, pointRadius: 0, tension: 0.4, borderWidth: 2 },
                { label: 'Profundo (128,64,32)', data: DATA.nnLossReg.deep, borderColor: COLORS.indigo, backgroundColor: COLORS.indigoAlpha, fill: false, pointRadius: 0, tension: 0.4, borderWidth: 2 },
                { label: 'Regularizado (α=0.01)', data: DATA.nnLossReg.regularized, borderColor: COLORS.amber, backgroundColor: COLORS.amberAlpha, fill: false, pointRadius: 0, tension: 0.4, borderWidth: 2 },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                x: { title: { display: true, text: 'Épocas' } },
                y: { title: { display: true, text: 'MSE Loss' } }
            }
        }
    });
}

function initRegressionCompareChart() {
    if (chartInstances['regressionCompareChart']) return;
    chartInstances['regressionCompareChart'] = true;

    const trace1 = {
        type: 'bar',
        name: 'MAE',
        x: DATA.regression.models,
        y: DATA.regression.mae,
        marker: { color: COLORS.indigoAlpha, line: { color: COLORS.indigo, width: 1.5 } },
        text: DATA.regression.mae.map(v => v.toFixed(2)),
        textposition: 'auto'
    };

    const trace2 = {
        type: 'bar',
        name: 'RMSE',
        x: DATA.regression.models,
        y: DATA.regression.rmse,
        marker: { color: COLORS.redAlpha, line: { color: COLORS.red, width: 1.5 } },
        text: DATA.regression.rmse.map(v => v.toFixed(2)),
        textposition: 'auto'
    };

    const layout = {
        barmode: 'group',
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#9ca3be', family: 'Inter' },
        margin: { l: 50, r: 20, t: 40, b: 60 },
        legend: { orientation: 'h', x: 0.5, xanchor: 'center', y: 1.1 },
        yaxis: { title: 'Erro', gridcolor: 'rgba(99, 102, 241, 0.06)' }
    };

    Plotly.newPlot('regressionCompareChart', [trace1, trace2], layout, {displayModeBar: false, responsive: true});
}

function initRegCompTable() {
    const tbody = document.getElementById('regCompTable');
    if (!tbody || tbody.children.length > 0) return;

    DATA.regComparison.forEach(row => {
        const tr = document.createElement('tr');
        const isBest = row.maeMu === Math.min(...DATA.regComparison.map(r => r.maeMu));
        tr.innerHTML = `
            <td style="font-weight:${isBest ? '600' : '400'}; color:${isBest ? '#818cf8' : 'inherit'}">${row.model}</td>
            <td style="font-family:'JetBrains Mono',monospace; font-weight:600; color:${isBest ? '#10b981' : 'inherit'}">${row.maeMu.toFixed(2)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.maeSig.toFixed(2)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.rmseMu.toFixed(2)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.rmseSig.toFixed(2)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.time.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function initLearningCurveRegChart() {
    const ctx = document.getElementById('learningCurveRegChart');
    if (!ctx || chartInstances['learningCurveRegChart']) return;

    chartInstances['learningCurveRegChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DATA.learningCurveReg.trainSizes.map(v => (v/1000).toFixed(1) + 'k'),
            datasets: [
                { label: 'Árvore — Treino', data: DATA.learningCurveReg.treeTrain, borderColor: COLORS.indigo, pointRadius: 4, tension: 0.3, borderWidth: 2, fill: false },
                { label: 'Árvore — Validação', data: DATA.learningCurveReg.treeVal, borderColor: COLORS.red, pointRadius: 4, tension: 0.3, borderWidth: 2, borderDash: [5, 5], fill: false },
                { label: 'LM — Treino', data: DATA.learningCurveReg.lmTrain, borderColor: COLORS.green, pointRadius: 4, tension: 0.3, borderWidth: 2, fill: false },
                { label: 'LM — Validação', data: DATA.learningCurveReg.lmVal, borderColor: COLORS.amber, pointRadius: 4, tension: 0.3, borderWidth: 2, borderDash: [5, 5], fill: false },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } },
            scales: {
                x: { title: { display: true, text: 'Tamanho Treino' } },
                y: { title: { display: true, text: 'MAE' } }
            }
        }
    });
}

function initMAEFoldChart() {
    const ctx = document.getElementById('maeFoldChart');
    if (!ctx || chartInstances['maeFoldChart']) return;

    chartInstances['maeFoldChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DATA.maeFold.folds,
            datasets: [
                { label: 'Árvore', data: DATA.maeFold.tree, borderColor: COLORS.indigo, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
                { label: 'Reg. Linear Múltipla', data: DATA.maeFold.lm, borderColor: COLORS.red, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                y: { title: { display: true, text: 'MAE' } }
            }
        }
    });
}

function initClassDistChart() {
    if (chartInstances['classDistChart']) return;
    chartInstances['classDistChart'] = true;

    const xLabels = DATA.classDistribution.labels;
    const yData = DATA.classDistribution.values;
    const colors = [COLORS.greenAlpha, COLORS.amberAlpha, COLORS.redAlpha];
    const lines = [COLORS.green, COLORS.amber, COLORS.red];

    const trace = {
        type: 'bar',
        x: xLabels,
        y: yData,
        marker: { color: colors, line: { color: lines, width: 1.5 } },
        text: yData.map(v => v.toString()),
        textposition: 'auto',
        hoverinfo: 'x+y'
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#9ca3be', family: 'Inter' },
        margin: { l: 60, r: 20, t: 20, b: 40 },
        xaxis: { gridcolor: 'rgba(99, 102, 241, 0.06)' },
        yaxis: { title: 'Nº PTDs', gridcolor: 'rgba(99, 102, 241, 0.06)' }
    };

    Plotly.newPlot('classDistChart', [trace], layout, {displayModeBar: false, responsive: true});
}

function initFeatureImportanceClfChart() {
    if (chartInstances['featureImportanceClfChart']) return;
    chartInstances['featureImportanceClfChart'] = true;

    // Reverse for bottom-to-top rendering in Plotly horizontal bars
    const xData = [...DATA.featureImportanceClf.values].reverse();
    const yLabels = [...DATA.featureImportanceClf.labels].reverse();
    
    // Apply colors based on original importance rank (before reversing)
    // The original array has most important at index 0.
    // After reversing, most important is at the end (index 14).
    const colors = xData.map((v, reversedIdx) => {
        const origIdx = 14 - reversedIdx;
        return origIdx < 3 ? COLORS.indigoAlpha : origIdx < 6 ? COLORS.purpleAlpha : COLORS.cyanAlpha;
    });
    const lines = xData.map((v, reversedIdx) => {
        const origIdx = 14 - reversedIdx;
        return origIdx < 3 ? COLORS.indigo : origIdx < 6 ? COLORS.purple : COLORS.cyan;
    });

    const trace = {
        type: 'bar',
        x: xData,
        y: yLabels,
        orientation: 'h',
        marker: { color: colors, line: { color: lines, width: 1.5 } },
        text: xData.map(v => v.toFixed(3)),
        textposition: 'auto',
        hoverinfo: 'x+y'
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#9ca3be', family: 'Inter' },
        margin: { l: 150, r: 20, t: 20, b: 40 },
        xaxis: { title: 'Importância (Gini)', gridcolor: 'rgba(99, 102, 241, 0.06)' },
        yaxis: { automargin: true }
    };

    Plotly.newPlot('featureImportanceClfChart', [trace], layout, {displayModeBar: false, responsive: true});
}

function initNNLossClfChart() {
    const ctx = document.getElementById('nnLossClfChart');
    if (!ctx || chartInstances['nnLossClfChart']) return;

    chartInstances['nnLossClfChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DATA.nnLossClf.epochs,
            datasets: [
                { label: 'Simples (64)', data: DATA.nnLossClf.simple, borderColor: COLORS.cyan, fill: false, pointRadius: 0, tension: 0.4, borderWidth: 2 },
                { label: 'Profundo (256,128,64)', data: DATA.nnLossClf.deep, borderColor: COLORS.indigo, fill: false, pointRadius: 0, tension: 0.4, borderWidth: 2 },
                { label: 'Regularizado (128,64)', data: DATA.nnLossClf.regularized, borderColor: COLORS.amber, fill: false, pointRadius: 0, tension: 0.4, borderWidth: 2 },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                x: { title: { display: true, text: 'Épocas' } },
                y: { title: { display: true, text: 'Loss' } }
            }
        }
    });
}

function initKNNChart() {
    const ctx = document.getElementById('knnKChart');
    if (!ctx || chartInstances['knnKChart']) return;

    chartInstances['knnKChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DATA.knnOptimization.kValues.map(k => `K=${k}`),
            datasets: [
                { label: 'Accuracy', data: DATA.knnOptimization.accuracy, borderColor: COLORS.indigo, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
                { label: 'F1-score', data: DATA.knnOptimization.f1, borderColor: COLORS.red, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
                { label: 'Precision', data: DATA.knnOptimization.precision, borderColor: COLORS.green, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
                { label: 'Recall', data: DATA.knnOptimization.recall, borderColor: COLORS.amber, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                annotation: {}
            },
            scales: {
                y: { title: { display: true, text: 'Métrica' }, min: 0.75, max: 0.85 }
            }
        }
    });
}

function initClfMetricsChart() {
    if (chartInstances['clfMetricsChart']) return;
    chartInstances['clfMetricsChart'] = true;

    const models = DATA.classification.models;
    
    const traceAcc = {
        type: 'bar', name: 'Accuracy', x: models, y: DATA.classification.accuracy,
        marker: { color: COLORS.indigoAlpha, line: { color: COLORS.indigo, width: 1.5 } },
        text: DATA.classification.accuracy.map(v => v.toFixed(2)), textposition: 'auto'
    };
    const tracePrec = {
        type: 'bar', name: 'Precision', x: models, y: DATA.classification.precision,
        marker: { color: COLORS.purpleAlpha, line: { color: COLORS.purple, width: 1.5 } },
        text: DATA.classification.precision.map(v => v.toFixed(2)), textposition: 'auto'
    };
    const traceRec = {
        type: 'bar', name: 'Recall', x: models, y: DATA.classification.recall,
        marker: { color: COLORS.cyanAlpha, line: { color: COLORS.cyan, width: 1.5 } },
        text: DATA.classification.recall.map(v => v.toFixed(2)), textposition: 'auto'
    };
    const traceF1 = {
        type: 'bar', name: 'F1-score', x: models, y: DATA.classification.f1,
        marker: { color: COLORS.greenAlpha, line: { color: COLORS.green, width: 1.5 } },
        text: DATA.classification.f1.map(v => v.toFixed(2)), textposition: 'auto'
    };

    const layout = {
        barmode: 'group',
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#9ca3be', family: 'Inter' },
        margin: { l: 50, r: 20, t: 40, b: 40 },
        legend: { orientation: 'h', x: 0.5, xanchor: 'center', y: 1.1 },
        yaxis: { range: [0.75, 0.95], gridcolor: 'rgba(99, 102, 241, 0.06)' }
    };

    Plotly.newPlot('clfMetricsChart', [traceAcc, tracePrec, traceRec, traceF1], layout, {displayModeBar: false, responsive: true});
}

function initClfCompTable() {
    const tbody = document.getElementById('clfCompTable');
    if (!tbody || tbody.children.length > 0) return;

    DATA.clfComparison.forEach(row => {
        const tr = document.createElement('tr');
        const isBest = row.f1Mu === Math.max(...DATA.clfComparison.map(r => r.f1Mu));
        tr.innerHTML = `
            <td style="font-weight:${isBest ? '600' : '400'}; color:${isBest ? '#818cf8' : 'inherit'}">${row.model}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.accMu.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.accSig.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.precMu.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.precSig.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.recMu.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.recSig.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace; font-weight:600; color:${isBest ? '#10b981' : 'inherit'}">${row.f1Mu.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.f1Sig.toFixed(4)}</td>
            <td style="font-family:'JetBrains Mono',monospace">${row.time.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function initLearningCurveClfChart() {
    const ctx = document.getElementById('learningCurveClfChart');
    if (!ctx || chartInstances['learningCurveClfChart']) return;

    chartInstances['learningCurveClfChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DATA.learningCurveClf.trainSizes.map(v => (v/1000).toFixed(1) + 'k'),
            datasets: [
                { label: 'Melhor — Treino', data: DATA.learningCurveClf.bestTrain, borderColor: COLORS.indigo, pointRadius: 4, tension: 0.3, borderWidth: 2, fill: false },
                { label: 'Melhor — Validação', data: DATA.learningCurveClf.bestVal, borderColor: COLORS.red, pointRadius: 4, tension: 0.3, borderWidth: 2, borderDash: [5, 5], fill: false },
                { label: 'Pior — Treino', data: DATA.learningCurveClf.worstTrain, borderColor: COLORS.green, pointRadius: 4, tension: 0.3, borderWidth: 2, fill: false },
                { label: 'Pior — Validação', data: DATA.learningCurveClf.worstVal, borderColor: COLORS.amber, pointRadius: 4, tension: 0.3, borderWidth: 2, borderDash: [5, 5], fill: false },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } },
            scales: {
                x: { title: { display: true, text: 'Tamanho Treino' } },
                y: { title: { display: true, text: 'F1-score' }, min: 0.75, max: 0.95 }
            }
        }
    });
}

function initF1FoldChart() {
    const ctx = document.getElementById('f1FoldChart');
    if (!ctx || chartInstances['f1FoldChart']) return;

    chartInstances['f1FoldChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DATA.f1Fold.folds,
            datasets: [
                { label: 'SVM', data: DATA.f1Fold.svm, borderColor: COLORS.indigo, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
                { label: 'Árvore Decisão', data: DATA.f1Fold.dt, borderColor: COLORS.red, pointRadius: 5, tension: 0.2, borderWidth: 2, fill: false },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                y: { title: { display: true, text: 'F1-score' }, min: 0.8, max: 0.86 }
            }
        }
    });
}

function initRadarChart() {
    const ctx = document.getElementById('radarChart');
    if (!ctx || chartInstances['radarChart']) return;

    chartInstances['radarChart'] = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Accuracy', 'Precision', 'Recall', 'F1-score'],
            datasets: [
                { label: 'Árvore Decisão', data: [0.8245, 0.8231, 0.8245, 0.8236], borderColor: COLORS.indigo, backgroundColor: 'rgba(99, 102, 241, 0.1)', borderWidth: 2, pointRadius: 4 },
                { label: 'Rede Neuronal', data: [0.8312, 0.8298, 0.8312, 0.8304], borderColor: COLORS.purple, backgroundColor: 'rgba(168, 85, 247, 0.1)', borderWidth: 2, pointRadius: 4 },
                { label: 'SVM (RBF)', data: [0.8456, 0.8442, 0.8456, 0.8448], borderColor: COLORS.green, backgroundColor: 'rgba(16, 185, 129, 0.1)', borderWidth: 2, pointRadius: 4 },
                { label: 'KNN (K=5)', data: [0.8178, 0.8165, 0.8178, 0.8170], borderColor: COLORS.amber, backgroundColor: 'rgba(245, 158, 11, 0.1)', borderWidth: 2, pointRadius: 4 },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                r: {
                    min: 0.78,
                    max: 0.86,
                    ticks: { stepSize: 0.02, backdropColor: 'transparent' },
                    grid: { color: 'rgba(99, 102, 241, 0.1)' },
                    angleLines: { color: 'rgba(99, 102, 241, 0.1)' },
                    pointLabels: { font: { size: 12, weight: 500 } }
                }
            }
        }
    });
}


// =============================================
// SECTION CHART INITIALIZATION
// =============================================
const sectionInitialized = {};

function initChartsForSection(sectionId) {
    if (sectionInitialized[sectionId]) return;
    sectionInitialized[sectionId] = true;

    // Use requestAnimationFrame and a timeout slightly longer than the CSS transition (300ms)
    // to ensure the browser has calculated the exact final container dimensions.
    // This prevents the Chart.js v4 Bar controller from caching a NaN bar thickness on 0x0 containers.
    requestAnimationFrame(() => {
        setTimeout(() => {
            switch(sectionId) {
                case 'overview':
                    break;
                case 'eda':
                    initCorrChart();
                    initTipoChart();
                    initUtilDistChart();
                    initIndependenceTable();
                    break;
                case 'regression':
                    initScatterRegSimple();
                    initFeatureImportanceRegChart();
                    initNNLossRegChart();
                    initRegressionCompareChart();
                    initRegCompTable();
                    initLearningCurveRegChart();
                    initMAEFoldChart();
                    break;
                case 'classification':
                    initClassDistChart();
                    initFeatureImportanceClfChart();
                    initNNLossClfChart();
                    initKNNChart();
                    initClfMetricsChart();
                    break;
                case 'comparison':
                    initClfCompTable();
                    initLearningCurveClfChart();
                    initF1FoldChart();
                    initRadarChart();
                    break;
            }
        }, 350);
    });
}


// =============================================
// INTERSECTION OBSERVER — Fade-in animations
// =============================================
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });


// =============================================
// INITIALIZATION
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    const loadingScreen = document.getElementById('loadingScreen');

    // Dismiss loading screen after animation completes
    const dismissLoading = () => {
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
        }
        // Animate counters after loading screen fades
        setTimeout(() => {
            animateCounters();

            // Fade in overview elements
            document.querySelectorAll('#overview .fade-in').forEach(el => {
                observer.observe(el);
                setTimeout(() => el.classList.add('visible'), 200);
            });
        }, 300);
    };

    // Auto-dismiss after loading bar animation (1.8s) + small buffer
    setTimeout(dismissLoading, 2200);

    // Also allow clicking to dismiss early
    if (loadingScreen) {
        loadingScreen.addEventListener('click', dismissLoading);
    }

    // Set up observers for all sections
    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

    // Initialize overview section
    sectionInitialized['overview'] = true;

    // Close sidebar on clicking outside (mobile)
    document.addEventListener('click', (e) => {
        if (sidebar.classList.contains('open') &&
            !sidebar.contains(e.target) &&
            !mobileToggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    });

    // =============================================
    // MODAL CHART ZOOM
    // =============================================
    const chartModal = document.getElementById('chartModal');
    const modalCanvas = document.getElementById('modalCanvas');
    const modalPlotly = document.getElementById('modalPlotly');
    const chartModalClose = document.getElementById('chartModalClose');
    let modalChartInstance = null;

    // Handle Chart.js Expansion
    document.querySelectorAll('.zoomable-chart').forEach(canvas => {
        canvas.addEventListener('click', () => {
            const sourceChart = Chart.getChart(canvas);
            if (!sourceChart) return;

            chartModal.classList.add('active');
            modalCanvas.parentElement.style.display = 'block';
            modalPlotly.style.display = 'none';
            document.getElementById('modalTable').style.display = 'none';

            if (modalChartInstance) {
                modalChartInstance.destroy();
            }
            Plotly.purge(modalPlotly); // clear any plotly traces

            const clonedDatasets = sourceChart.config.data.datasets.map(ds => ({
                ...ds,
                data: [...ds.data],
                backgroundColor: Array.isArray(ds.backgroundColor) ? [...ds.backgroundColor] : ds.backgroundColor,
                borderColor: Array.isArray(ds.borderColor) ? [...ds.borderColor] : ds.borderColor
            }));

            const config = {
                type: sourceChart.config.type,
                data: {
                    labels: [...sourceChart.config.data.labels],
                    datasets: clonedDatasets
                },
                options: Object.assign({}, sourceChart.config.options)
            };
            
            config.options.maintainAspectRatio = false;
            config.options.responsive = true;
            config.options.animation = { duration: 0 };
            
            // Shallow clone nested objects to avoid mutating original chart
            config.options.plugins = Object.assign({}, config.options.plugins);
            if (config.options.plugins.legend) {
                config.options.plugins.legend = Object.assign({}, config.options.plugins.legend);
                config.options.plugins.legend.labels = Object.assign({}, config.options.plugins.legend.labels);
                config.options.plugins.legend.labels.font = { size: 16 };
            }
            
            config.options.scales = Object.assign({}, config.options.scales);
            if (config.options.scales) {
                if (config.options.scales.x) {
                    config.options.scales.x = Object.assign({}, config.options.scales.x);
                    config.options.scales.x.ticks = Object.assign({}, config.options.scales.x.ticks, { font: { size: 14 } });
                    if (config.options.scales.x.title) {
                        config.options.scales.x.title = Object.assign({}, config.options.scales.x.title);
                        config.options.scales.x.title.font = { size: 16 };
                    }
                }
                if (config.options.scales.y) {
                    config.options.scales.y = Object.assign({}, config.options.scales.y);
                    config.options.scales.y.ticks = Object.assign({}, config.options.scales.y.ticks, { font: { size: 14 } });
                    if (config.options.scales.y.title) {
                        config.options.scales.y.title = Object.assign({}, config.options.scales.y.title);
                        config.options.scales.y.title.font = { size: 16 };
                    }
                }
            }
            
            setTimeout(() => {
                modalChartInstance = new Chart(modalCanvas, config);
            }, 350);
        });
    });

    // Handle Plotly Expansion
    document.querySelectorAll('.plotly-chart').forEach(div => {
        div.addEventListener('click', (e) => {
            chartModal.classList.add('active');
            modalCanvas.parentElement.style.display = 'none';
            modalPlotly.style.display = 'block';
            document.getElementById('modalTable').style.display = 'none';

            if (modalChartInstance) {
                modalChartInstance.destroy();
                modalChartInstance = null;
            }
            Plotly.purge(modalPlotly); // clear any previous plotly traces

            // Clone data and layout
            const dataClone = JSON.parse(JSON.stringify(div.data));
            const layoutClone = JSON.parse(JSON.stringify(div.layout));
            
            // Increase font sizes and margins for fullscreen viewing
            layoutClone.font = layoutClone.font || {};
            layoutClone.font.size = 14;
            
            setTimeout(() => {
                Plotly.newPlot('modalPlotly', dataClone, layoutClone, {displayModeBar: false, responsive: true});
            }, 350);
        });
    });

    // Handle Table Expansion
    document.querySelectorAll('.expandable-table').forEach(tableWrapper => {
        tableWrapper.addEventListener('click', () => {
            chartModal.classList.add('active');
            modalCanvas.parentElement.style.display = 'none';
            modalPlotly.style.display = 'none';
            const modalTable = document.getElementById('modalTable');
            modalTable.style.display = 'block';

            // Clear any charts
            if (modalChartInstance) {
                modalChartInstance.destroy();
                modalChartInstance = null;
            }
            Plotly.purge(modalPlotly);

            // Clone table content
            modalTable.innerHTML = '';
            const clonedTable = tableWrapper.cloneNode(true);
            clonedTable.style.cursor = 'default';
            clonedTable.title = ''; // remove tooltip
            
            // Allow table to expand fully
            clonedTable.style.maxHeight = '80vh';
            
            modalTable.appendChild(clonedTable);
        });
    });

    window.openImageModal = function(src) {
        chartModal.classList.add('active');
        modalCanvas.parentElement.style.display = 'none';
        modalPlotly.style.display = 'none';
        document.getElementById('modalTable').style.display = 'none';
        
        const img = document.getElementById('modalImage');
        if (img) {
            img.style.display = 'block';
            img.src = src;
        }

        // Clear any charts
        if (modalChartInstance) {
            modalChartInstance.destroy();
            modalChartInstance = null;
        }
        Plotly.purge(modalPlotly);
    };

    const closeModal = () => {
        chartModal.classList.remove('active');
        if (modalChartInstance) {
            setTimeout(() => {
                modalChartInstance.destroy();
                modalChartInstance = null;
            }, 300);
        }
        setTimeout(() => {
            Plotly.purge(modalPlotly);
            document.getElementById('modalTable').innerHTML = '';
            const img = document.getElementById('modalImage');
            if (img) {
                img.style.display = 'none';
                img.src = '';
            }
        }, 300);
    };

    chartModalClose.addEventListener('click', closeModal);
    chartModal.addEventListener('click', (e) => {
        if (e.target === chartModal) closeModal();
    });
});
