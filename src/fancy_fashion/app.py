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
from google.cloud import storage

app = FastAPI()

storage_client = storage.Client()
file_data = 'pipelines/1035892568606/fancy-fashion-joost-20220609121407/train_1001263666764447744/model/model.pkl'
bucket_name = 'gdd-vertex-fashion-artifacts'
temp_file_name = 'model.pkl'
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.get_blob(file_data)
blob.download_to_filename(temp_file_name)

model = joblib.load("./model.pkl")

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Time spent processing request in seconds",
    labelnames=["model_version"],
)

REQUEST_COUNT = Counter(
    "request_count", "Total number of requests", labelnames=["model_version"]
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
    REQUEST_COUNT.labels(model_version="random").inc()
    name = image_data.filename
    raw_image_data = image_data.file.read()
    img = io.BytesIO(raw_image_data)
    confidence = generate_prediction(model, img)[0]
    prediction = confidence.argmax(axis=0)
    prediction_txt = LABEL_MAPPING.get(prediction)
    confidence_scores = {LABEL_MAPPING.get(i): float(confidence[i]) for i in range(confidence.shape[0])}

    return {name: {"best_match": prediction_txt, "confidence": confidence_scores}}
