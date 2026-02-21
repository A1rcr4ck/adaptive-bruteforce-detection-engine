async function searchIP() {
    const ip = document.getElementById("ipInput").value;
    if (!ip) return;

    const response = await fetch(`/api/threat-intel/${ip}`);
    const data = await response.json();

    const container = document.getElementById("intelResult");

    if (data.error) {
        container.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        return;
    }

    const riskLevel = data.profile.risk_score > 70 ? "High"
                     : data.profile.risk_score > 40 ? "Medium"
                     : "Low";

    const riskColor = riskLevel === "High" ? "bg-danger"
                     : riskLevel === "Medium" ? "bg-warning"
                     : "bg-success";

    container.innerHTML = `
        <div class="card p-4 mb-4">
            <h5 class="mb-3">IP Profile</h5>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>IP:</strong> ${data.ip}</p>
                    <p><strong>Total Attempts:</strong> ${data.profile.total_attempts}</p>
                    <p><strong>Failed Attempts:</strong> ${data.profile.failed_attempts}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Unique Users:</strong> ${data.profile.unique_users}</p>
                    <p><strong>First Seen:</strong> ${data.profile.first_seen}</p>
                    <p><strong>Last Seen:</strong> ${data.profile.last_seen}</p>
                    <strong>Risk Level:</strong>
                    <span class="badge ${riskColor}">${riskLevel}</span>
                </div>
            </div>
        </div>

        <div class="card p-3">
            <h5>Alert History</h5>
            <ul class="list-group">
                ${data.alerts.map(a => {

                    const severityColor =
                        a.severity === "High" ? "bg-danger" :
                        a.severity === "Medium" ? "bg-warning" :
                        "bg-success";

                    return `
                        <li class="list-group-item bg-dark text-light">
                            #${a.id} — ${a.attack_type}
                            <span class="badge ${severityColor} float-end">
                                ${a.severity}
                            </span>
                        </li>
                    `;
                }).join("")}
            </ul>
        </div>
    `;
}