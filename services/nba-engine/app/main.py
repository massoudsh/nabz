"""نبض — Next-Best-Action API. اجرا: uvicorn app.main:app --reload"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from app import decision_store, feedback_store
from app.admin import router as admin_router
from app.auth import require_api_key
from app.db import init_db
from app.engine import decide
from app.models import CampaignFeedback, Customer, Decision


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="نبض — Nabz Next-Best-Action Engine",
    description="برای هر مشتری، بهترین اقدام بعدی (چه کسی، چه زمانی، چه کانالی، چه پیشنهادی) را تصمیم می‌گیرد.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(admin_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/decide", response_model=Decision, dependencies=[Depends(require_api_key)])
def decide_endpoint(customer: Customer) -> Decision:
    decision = decide(customer)
    decision_store.log_decision(decision)
    return decision


@app.post("/decide/batch", response_model=list[Decision], dependencies=[Depends(require_api_key)])
def decide_batch_endpoint(customers: list[Customer]) -> list[Decision]:
    """تصمیم دسته‌ای برای چند صد/هزار مشتری یکجا — issue #8، آماده‌سازی اتصال فاز ۱."""
    decisions = [decide(customer) for customer in customers]
    for decision in decisions:
        decision_store.log_decision(decision)
    return decisions


@app.post("/feedback", response_model=CampaignFeedback, dependencies=[Depends(require_api_key)])
def record_feedback(feedback: CampaignFeedback) -> CampaignFeedback:
    """ثبت نتیجه‌ی واقعی یک اقدام (باز شد/خرید شد) — پایپلاین PRD بخش ۵.۲ گام ۷."""
    return feedback_store.record(feedback)


@app.get("/feedback/{customer_id}", response_model=list[CampaignFeedback], dependencies=[Depends(require_api_key)])
def get_feedback(customer_id: str) -> list[CampaignFeedback]:
    history = feedback_store.list_for_customer(customer_id)
    if not history:
        raise HTTPException(status_code=404, detail="بازخوردی برای این مشتری ثبت نشده")
    return history
