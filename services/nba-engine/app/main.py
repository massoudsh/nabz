"""نبض — Next-Best-Action API. اجرا: uvicorn app.main:app --reload"""

from fastapi import FastAPI

from app.engine import decide
from app.models import Customer, Decision

app = FastAPI(
    title="نبض — Nabz Next-Best-Action Engine",
    description="برای هر مشتری، بهترین اقدام بعدی (چه کسی، چه زمانی، چه کانالی، چه پیشنهادی) را تصمیم می‌گیرد.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/decide", response_model=Decision)
def decide_endpoint(customer: Customer) -> Decision:
    return decide(customer)
