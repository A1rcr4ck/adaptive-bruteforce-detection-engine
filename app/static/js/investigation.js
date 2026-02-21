async function loadAlerts() {
    const response = await fetch('/api/alerts?status=OPEN');
    const alerts = await response.json();

    const alertList = document.getElementById("alertList");
    alertList.innerHTML = "";

    alerts.forEach(alert => {
        const item = document.createElement("li");
        item.className = "list-group-item bg-dark text-light";
        item.style.cursor = "pointer";
        item.innerText = `#${alert.id} - ${alert.attack_type}`;
        item.onclick = () => loadInvestigation(alert.id);
        alertList.appendChild(item);
    });
}

async function loadInvestigation(alertId) {
    const response = await fetch(`/api/investigation/${alertId}`);
    const data = await response.json();
    const timestamps = data.recent_events.map(e => e.timestamp);
    const activity = data.recent_events.map((_, i) => i + 1);
    const severityColor = data.alert.severity === "High" ? "bg-danger"
                     : data.alert.severity === "Medium" ? "bg-warning"
                     : "bg-info";
    // renderRiskGauge(data.ip_profile.risk_score);

    document.getElementById("alertDetails").innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <p><strong>Attack Type:</strong> ${data.alert.attack_type}</p>
                <p><strong>IP Address:</strong> ${data.alert.ip}</p>
                <p><strong>MITRE:</strong> ${data.alert.mitre_mapping}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Severity:</strong> 
                    <span class="badge ${severityColor}">${data.alert.severity}</span>
                    
                </p>
                <p><strong>Confidence:</strong> ${data.alert.confidence}</p>
                <p><strong>Risk Score:</strong> ${data.alert.risk_score}</p>
            </div>
        </div>
        <button class="btn btn-danger mt-3" onclick="resolveAlert(${alertId})">
            Mark as Resolved
        </button>
    `;
    new Chart(document.getElementById("ipTimelineChart"), {
    type: 'line',
    data: {
            labels: timestamps.reverse(),
            datasets: [{
                label: 'IP Activity',
                data: activity.reverse(),
                borderColor: '#22d3ee',
                tension: 0.4,
                fill: false
            }]
        }
    });

    document.getElementById("ipProfile").innerHTML = `
        <p><strong>Total Attempts:</strong> ${data.ip_profile.total_attempts}</p>
        <p><strong>Failed Attempts:</strong> ${data.ip_profile.failed_attempts}</p>
        <p><strong>Unique Users:</strong> ${data.ip_profile.unique_users}</p>
        <p><strong>Risk Score:</strong> ${data.ip_profile.risk_score}</p>
    `;

    const table = document.getElementById("eventTable");
    table.innerHTML = "";

    data.recent_events.forEach(event => {
        table.innerHTML += `
            <tr>
                <td>${event.timestamp}</td>
                <td>${event.username}</td>
                <td>${event.status}</td>
                <td>${event.service}</td>
            </tr>
        `;
    });
}

async function resolveAlert(alertId) {
    await fetch(`/api/resolve/${alertId}`, { method: "POST" });
    loadAlerts();
    document.getElementById("alertDetails").innerHTML = "";
    document.getElementById("ipProfile").innerHTML = "";
    document.getElementById("eventTable").innerHTML = "";
}

loadAlerts();

// function renderRiskGauge(score) {
//     const ctx = document.getElementById("riskGauge").getContext("2d");

//     const color = score > 70 ? "#ef4444"
//                 : score > 40 ? "#facc15"
//                 : "#22c55e";

//     new Chart(ctx, {
//         type: 'doughnut',
//         data: {
//             datasets: [{
//                 data: [score, 100 - score],
//                 backgroundColor: [color, "#1e293b"],
//                 borderWidth: 0
//             }]
//         },
//         options: {
//             responsive: true,
//             maintainAspectRatio: false,
//             cutout: "75%",
//             animation: {
//                 animateRotate: true,
//                 duration: 1200
//             },
//             plugins: {
//                 tooltip: { enabled: false },
//                 legend: { display: false }
//             }
//         },
//         plugins: [{
//             id: 'centerText',
//             beforeDraw(chart) {
//                 const { width } = chart;
//                 const { height } = chart;
//                 const ctx = chart.ctx;
//                 ctx.restore();
//                 ctx.font = "bold 28px -apple-system";
//                 ctx.fillStyle = color;
//                 ctx.textBaseline = "middle";
//                 ctx.textAlign = "center";
//                 ctx.fillText(score, width / 2, height / 2);
//                 ctx.save();
//             }
//         }]
//     });
// }