from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
import os

from database import create_tables, insert_alert, get_recent_alerts
from detector import analyze_url

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Ensure database tables exist ----------------
create_tables()

# ---------------- Serve Frontend ----------------
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")  # For JS/CSS files

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# ---------------- Alerts ----------------
@app.get("/alerts")
def get_alerts():
    rows = get_recent_alerts()
    formatted = []
    for row in rows:
        formatted.append({
            "timestamp": row[1],
            "source_ip": row[2],
            "destination_ip": row[3],
            "bytes": row[4],
            "type": row[5],
            "severity": row[6],
            "details": row[7]
        })
    return {"alerts": formatted}

# ---------------- Analyze URL ----------------
@app.post("/analyze")
def analyze(data: dict):
    test_url = data.get("url", "")
    if not test_url:
        return {"error": "No URL provided"}
    return analyze_url(test_url)

# ---------------- Train Model ----------------
@app.post("/train")
async def train(file: UploadFile = File(...)):
    filename = file.filename
    # Placeholder for ML training logic
    return {"message": f"Training started with file: {filename}"}

@app.post("/scan")
async def scan(file: UploadFile = File(...)):
    filename = file.filename
    content = (await file.read()).decode("utf-8", errors="ignore")

    # Simple rule-based detection (NO pandas)
    HIGH_KEYWORDS = ["malware", "ddos", "exploit", "attack", "trojan"]
    MEDIUM_KEYWORDS = ["suspicious", "unusual", "warning", "probe"]
    SAFE_KEYWORDS = ["normal", "ok", "safe"]

    risk_level = "Safe"
    details = "No threats found"

    content_lower = content.lower()

    # High risk detection
    if any(keyword in content_lower for keyword in HIGH_KEYWORDS):
        risk_level = "High"
        details = "High-Risk Indicators Found"
    # Medium risk detection
    elif any(keyword in content_lower for keyword in MEDIUM_KEYWORDS):
        risk_level = "Medium"
        details = "Suspicious Activity Detected"
    # Safe detection
    elif any(keyword in content_lower for keyword in SAFE_KEYWORDS):
        risk_level = "Safe"
        details = "File appears safe"
    else:
        details = "No clear indicators"

    # Insert alert into DB
    insert_alert(
        src_ip="192.168.1.10",
        dst_ip="10.0.0.5",
        bytes_val=len(content),
        attack_type="File Scan",
        risk_level=risk_level,
        details=f"{details} | File: {filename}"
    )

    return {
        "message": f"Scan completed for file: {filename}",
        "file": filename,
        "risk": risk_level,
        "details": details
    }