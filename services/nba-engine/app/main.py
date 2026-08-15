"""نبض — Next-Best-Action API. اجرا: uvicorn app.main:app --reload"""

from fastapi import FastAPI, HTTPException

from app import feedback_store
from app.engine import decide
from app.models import CampaignFeedback, Customer, Decision

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


@app.post("/feedback", response_model=CampaignFeedback)
def record_feedback(feedback: CampaignFeedback) -> CampaignFeedback:
    """ثبت نتیجه‌ی واقعی یک اقدام (باز شد/خرید شد) — پایپلاین PRD بخش ۵.۲ گام ۷."""
    return feedback_store.record(feedback)


@app.get("/feedback/{customer_id}", response_model=list[CampaignFeedback])
def get_feedback(customer_id: str) -> list[CampaignFeedback]:
    history = feedback_store.list_for_customer(customer_id)
    if not history:
        raise HTTPException(status_code=404, detail="بازخوردی برای این مشتری ثبت نشده")
    return history
