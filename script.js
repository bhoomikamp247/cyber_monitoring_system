const API = "http://127.0.0.1:8000";

// ==================== Train Model ====================
async function trainModel() {
    let file = document.getElementById("trainFile").files[0];
    if (!file) {
        alert("Please select training CSV file!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    try {
        let response = await fetch(API + "/train", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Training failed!");
        let result = await response.json();
        document.getElementById("trainStatus").innerText = "✔ " + result.message;
    } catch (err) {
        console.error(err);
        document.getElementById("trainStatus").innerText = "❌ " + err;
    }
}

// ==================== Scan File ====================
async function scanFile() {
    let file = document.getElementById("scanFile").files[0];
    if (!file) {
        alert("Please select scanning CSV file!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    try {
        let response = await fetch(API + "/scan", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Scan failed!");
        let result = await response.json();
        document.getElementById("scanStatus").innerText = "⚠ " + result.message;

        loadAlerts(); // Refresh alerts after scanning
    } catch (err) {
        console.error(err);
        document.getElementById("scanStatus").innerText = "❌ " + err;
    }
}

// ==================== Load Alerts ====================
async function loadAlerts() {
    try {
        let response = await fetch(API + "/alerts");
        if (!response.ok) throw new Error("Failed to load alerts");
        let data = await response.json();

        let tbody = document.querySelector("#alertTable tbody");
        tbody.innerHTML = "";

        let high = 0, medium = 0, safe = 0;

        data.alerts.forEach(a => {
            let row = `<tr>
                <td>${a.timestamp}</td>
                <td>${a.source_ip}</td>
                <td>${a.destination_ip}</td>
                <td>${a.bytes}</td>
                <td>${a.type}</td>
                <td>${a.severity}</td>
            </tr>`;
            tbody.innerHTML += row;

            if (a.severity === "High") high++;
            else if (a.severity === "Medium") medium++;
            else safe++;
        });

        // Update stats
        document.querySelector("#totalAlerts p").innerText = data.alerts.length;
        document.querySelector("#highRisk p").innerText = high;
        document.querySelector("#mediumRisk p").innerText = medium;
        document.querySelector("#safeScans p").innerText = safe;

        updateChart(high, medium, safe);
    } catch (err) {
        console.error(err);
    }
}

// ==================== Chart ==================

