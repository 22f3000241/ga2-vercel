from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Sample telemetry data (replace with real file if provided)
data = [
    {"region": "amer", "latency_ms": 160, "uptime": 99.9},
    {"region": "amer", "latency_ms": 200, "uptime": 99.7},
    {"region": "emea", "latency_ms": 170, "uptime": 99.8},
    {"region": "emea", "latency_ms": 180, "uptime": 99.6}
]

@app.post("/api/latency")
async def analyze_latency(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold = body["threshold_ms"]

    result = {}

    for region in regions:
        region_data = [r for r in data if r["region"] == region]

        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime"] for r in region_data]

        result[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": sum(1 for l in latencies if l > threshold)
        }

    return result
