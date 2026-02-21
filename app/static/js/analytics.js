async function loadAnalytics() {

    const textColor = "#e2e8f0";
    const gridColor = "rgba(255,255,255,0.08)";

    // ======================
    // Attack Distribution
    // ======================
    const attackRes = await fetch('/api/attack-distribution');
    const attackData = await attackRes.json();

    new Chart(document.getElementById("attackPie"), {
        type: 'doughnut',
        data: {
            labels: attackData.map(a => a.attack_type),
            datasets: [{
                data: attackData.map(a => a.count),
                backgroundColor: ["#ef4444", "#facc15", "#22d3ee"],
                borderWidth: 0
            }]
        },
        options: {
            cutout: "65%",
            animation: { duration: 1200 },
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            }
        }
    });

    // ======================
    // Top Targeted Users
    // ======================
    const usersRes = await fetch('/api/top-users');
    const usersData = await usersRes.json();

    new Chart(document.getElementById("topUsersChart"), {
        type: 'bar',
        data: {
            labels: usersData.map(u => u.username),
            datasets: [{
                label: 'Failed Attempts',
                data: usersData.map(u => u.attempts),
                backgroundColor: "#f97316",
                borderRadius: 8
            }]
        },
        options: {
            animation: { duration: 1200 },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                }
            },
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            }
        }
    });

    // ======================
    // Top Attacking IPs
    // ======================
    const ipRes = await fetch('/api/top-ips');
    const ipData = await ipRes.json();

    new Chart(document.getElementById("topIpsAnalytics"), {
        type: 'bar',
        data: {
            labels: ipData.map(ip => ip.ip),
            datasets: [{
                label: 'Failed Attempts',
                data: ipData.map(ip => ip.failed_attempts),
                backgroundColor: "#22d3ee",
                borderRadius: 8
            }]
        },
        options: {
            animation: { duration: 1200 },
            scales: {
                x: {
                    ticks: { color: "#e2e8f0" },
                    grid: { color: "rgba(255,255,255,0.08)" }
                },
                y: {
                    ticks: { color: "#e2e8f0" },
                    grid: { color: "rgba(255,255,255,0.08)" }
                }
            },
            plugins: {
                legend: {
                    labels: { color: "#e2e8f0" }
                }
            }
        }
    });

    // ======================
    // Timeline
    // ======================
    const trendRes = await fetch('/api/failed-trend');
    const trendData = await trendRes.json();

    new Chart(document.getElementById("timelineChart"), {
        type: 'line',
        data: {
            labels: trendData.map(t => t.hour),
            datasets: [{
                label: 'Failed Attempts',
                data: trendData.map(t => t.failed_attempts),
                borderColor: "#ef4444",
                backgroundColor: "rgba(239, 68, 68, 0.2)",
                fill: true,
                tension: 0.4,
                pointRadius: 4
            }]
        },
        options: {
            animation: { duration: 1500 },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                }
            },
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            }
        }
    });
}

loadAnalytics();