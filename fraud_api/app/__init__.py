from fastapi import FastAPI
from mongoengine import connect
from starlette.testclient import TestClient

from app.routers import alerts

app = FastAPI()

mongodb = connect('mongodb', host='mongodb://mongo1:27017/fraud_database', maxPoolSize=10)
client = TestClient(app)

app.include_router(alerts.router, prefix="/alerts", tags=["Alert Docs"], )