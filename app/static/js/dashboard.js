async function loadDashboard() {
    const response = await fetch('/api/overview-detailed');
    const data = await response.json();

    animateValue("total_logins", data.summary.total_logins);
    animateValue("failed_logins", data.summary.failed_logins);
    animateValue("unique_ips", data.summary.unique_ips);
    animateValue("open_alerts", data.summary.open_alerts);
    animateValue("high_severity_alerts", data.summary.high_severity_alerts);

    renderCharts(data);
    loadAlerts();
}

function animateValue(id, endValue) {
    const element = document.getElementById(id);
    let start = 0;
    const duration = 1000;
    const increment = endValue / (duration / 16);

    function updateCounter() {
        start += increment;
        if (start >= endValue) {
            element.innerText = endValue;
        } else {
            element.innerText = Math.floor(start);
            requestAnimationFrame(updateCounter);
        }
    }

    updateCounter();
}

function renderCharts(data) {
    const trendLabels = data.failed_trend.map(item => item.hour);
    const trendData = data.failed_trend.map(item => item.failed_attempts);

    new Chart(document.getElementById("failedTrendChart"), {
        type: 'line',
        data: {
            labels: trendLabels,
            datasets: [{
                label: 'Failed Attempts',
                data: trendData,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            animation: {
                duration: 1500
            }
        }
    });

    const ipLabels = data.top_ips.map(item => item.ip);
    const ipCounts = data.top_ips.map(item => item.failed_attempts);

    new Chart(document.getElementById("topIpsChart"), {
        type: 'bar',
        data: {
            labels: ipLabels,
            datasets: [{
                label: 'Failed Attempts',
                data: ipCounts,
                backgroundColor: '#f59e0b'
            }]
        },
        options: {
            animation: {
                duration: 1500
            }
        }
    });
}

async function loadAlerts() {
    const alertsResponse = await fetch('/api/alerts');
    const alerts = await alertsResponse.json();

    const tableBody = document.getElementById("alertsTable");
    tableBody.innerHTML = "";

    alerts.slice(0, 10).forEach(alert => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${alert.id}</td>
            <td>${alert.attack_type}</td>
            <td>${alert.ip}</td>
            <td><span class="badge bg-danger">${alert.severity}</span></td>
            <td>${alert.status}</td>
        `;
        tableBody.appendChild(row);
    });
}

loadDashboard();