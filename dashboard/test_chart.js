const { Chart } = require('chart.js');
const { createCanvas } = require('canvas');

const canvas = createCanvas(800, 400);
const ctx = canvas.getContext('2d');

const DATA = {
    featureImportanceClf: {
        labels: ['Cap_PTD_kVA', 'Pot_Contratada_kVA', 'N_Clientes', 'Potência Instalada',
                 'Cap_per_Cliente', 'PContratada_per_Cliente', 'IP_per_PTD',
                 'N_PTDs_Concelho', 'Ganho_LED_PTD', 'P_IP_Total',
                 'Rate_Ineficiencia', 'N_Luminarias', 'LED_Ratio',
                 'IP_Inef_per_PTD', 'latitude'],
        values: [0.285, 0.195, 0.142, 0.098, 0.065, 0.048, 0.035,
                 0.028, 0.024, 0.020, 0.018, 0.015, 0.012, 0.009, 0.006]
    }
};

const COLORS = {
    indigo: '#818cf8', indigoAlpha: 'rgba(129, 140, 248, 0.85)',
    purple: '#c084fc', purpleAlpha: 'rgba(192, 132, 252, 0.85)',
    cyan: '#22d3ee', cyanAlpha: 'rgba(34, 211, 238, 0.85)'
};

try {
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: DATA.featureImportanceClf.labels,
            datasets: [{
                data: DATA.featureImportanceClf.values,
                backgroundColor: DATA.featureImportanceClf.values.map((v, i) =>
                    i < 3 ? COLORS.indigoAlpha : i < 6 ? COLORS.purpleAlpha : COLORS.cyanAlpha
                ),
                borderColor: DATA.featureImportanceClf.values.map((v, i) =>
                    i < 3 ? COLORS.indigo : i < 6 ? COLORS.purple : COLORS.cyan
                ),
                borderWidth: 1.5,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { title: { display: true, text: 'Importância (Gini)' } }
            }
        }
    });

    // Force a render
    chart.update();
    console.log("CHART RENDERED SUCCESSFULLY.");
} catch (err) {
    console.error("CHART THREW ERROR:", err);
}
