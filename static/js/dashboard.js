// === Sélecteurs ===
const cpuBar = document.getElementById("cpu-bar");
const ramBar = document.getElementById("ram-bar");
const diskBar = document.getElementById("disk-bar");

const cpuValue = document.getElementById("cpu-value");
const ramValue = document.getElementById("ram-value");
const diskValue = document.getElementById("disk-value");

const cpuCanvas = document.getElementById("cpuChart");
let cpuChart = null;

// === Graphique CPU ===
if (cpuCanvas) {
    const ctx = cpuCanvas.getContext("2d");
    cpuChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'CPU %',
                data: [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16,185,129,0.15)',
                fill: true
            }]
        },
        options: {
            animation: false,
            responsive: true,
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });
}

// === Source des données (locale par défaut) ===
let currentAPI = "/api/stats";
const fetchOpts = { credentials: 'same-origin' };

// === Monitoring distant ===
const connectBtn = document.getElementById("connect-btn");
if (connectBtn) {
    connectBtn.addEventListener("click", () => {
        const ip = document.getElementById("remote-ip").value.trim();
        const status = document.getElementById("remote-status");

        if (!ip) {
            status.textContent = "⚠️ Entrez une adresse IP valide.";
            status.style.color = "#f59e0b";
            return;
        }

        const testURL = `http://${ip}:5000/api/stats`;

        fetch(testURL)
            .then(res => {
                if (!res.ok) throw new Error("Connexion impossible");
                currentAPI = testURL;
                status.textContent = `✅ Connecté à ${ip}`;
                status.style.color = "#10b981";
            })
            .catch(() => {
                status.textContent = "❌ Échec de la connexion. Reconnexion locale.";
                status.style.color = "#ef4444";
                currentAPI = "/api/stats"; // retour local
            });
    });
}

// === Mise à jour Dashboard ===
function updateDashboard() {
    fetch(currentAPI, fetchOpts)
        .then(response => {
            if (!response.ok) throw new Error("Not authorized");
            return response.json();
        })
        .then(data => {
            if (cpuBar) cpuBar.style.width = data.cpu + "%";
            if (ramBar) ramBar.style.width = data.ram_percent + "%";
            if (diskBar) diskBar.style.width = data.disk_percent + "%";

            if (cpuValue) cpuValue.textContent = data.cpu + "%";
            if (ramValue) ramValue.textContent = data.ram_percent + "%";
            if (diskValue) diskValue.textContent = data.disk_percent + "%";

            if (cpuChart) {
                const t = data.timestamp;
                if (cpuChart.data.labels.length >= 20) {
                    cpuChart.data.labels.shift();
                    cpuChart.data.datasets[0].data.shift();
                }
                cpuChart.data.labels.push(t);
                cpuChart.data.datasets[0].data.push(data.cpu);
                cpuChart.update();
            }
        })
        .catch(err => {
            console.warn("Erreur updateDashboard:", err);
            if (err.message === "Not authorized") {
                window.location.href = "/login";
            }
        });
}

// === Mode Dark/Light ===
const currentTheme = localStorage.getItem("theme") || "light";
if (currentTheme === "dark") document.body.classList.add("dark");

const themeToggle = document.getElementById("theme-toggle");
if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        const theme = document.body.classList.contains("dark") ? "dark" : "light";
        localStorage.setItem("theme", theme);
    });
}

// === Lancement auto ===
updateDashboard();
setInterval(updateDashboard, 3000);
