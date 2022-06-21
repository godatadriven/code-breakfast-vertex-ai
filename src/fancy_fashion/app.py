import asyncio
import io
import json

import joblib
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_async.aio import time
from prometheus_client import Counter, Histogram, generate_latest

from src.fancy_fashion.dataset import LABEL_MAPPING
from src.fancy_fashion.model import generate_prediction

app = FastAPI()
model = joblib.load("./model.pkl")

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Time spent processing request in seconds",
    labelnames=["model_version"],
)

PREDICTION_CONFIDENCE = Histogram(
    "prediction_confidence",
    "Confidence score of best label match.",
    labelnames=["model_version", "predicted_label"],
    buckets=[0, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 0.75, 0.8, 0.9, 0.95, 0.975, 0.99, 1]
)

REQUEST_COUNT = Counter(
    "request_count", "Total number of requests", labelnames=["model_version", "predicted_label"]
)


@app.get("/ping", response_class=PlainTextResponse)
def ping():
    """Heartbeat endpoint."""
    return "pong", 200


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()


@app.post("/predict", response_class=JSONResponse)
@time(REQUEST_LATENCY.labels(model_version="random"))  # async time functionality
async def predict(image_data: UploadFile):
    """Predict endpoint, which produces prediction for a given image."""
    name = image_data.filename
    raw_image_data = image_data.file.read()
    img = io.BytesIO(raw_image_data)
    confidence = generate_prediction(model, img)[0]
    prediction = confidence.argmax(axis=0)
    pred_confidence = confidence.max(axis=0)
    prediction_txt = LABEL_MAPPING.get(prediction)
    confidence_scores = {LABEL_MAPPING.get(i): float(confidence[i]) for i in range(confidence.shape[0])}

    REQUEST_COUNT.labels(model_version="random", predicted_label=prediction_txt).inc()
    PREDICTION_CONFIDENCE.labels(model_version="random", predicted_label=prediction_txt).observe(pred_confidence)

    return {name: {"best_match": prediction_txt, "confidence": confidence_scores}}
