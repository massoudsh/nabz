"""نبض — Next-Best-Action API. اجرا: uvicorn app.main:app --reload"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from app import decision_store, feedback_store, integration_store
from app.admin import router as admin_router
from app.auth import require_api_key
from app.db import init_db
from app.engine import decide
from app.models import (
    CampaignFeedback,
    CampaignReport,
    ConversationIngest,
    Customer,
    CustomerSnapshot,
    Decision,
    StorefrontCartIngest,
    StorefrontOrderIngest,
)


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


@app.post("/integrations/conversations", response_model=ConversationIngest, dependencies=[Depends(require_api_key)])
def ingest_conversation(event: ConversationIngest) -> ConversationIngest:
    return integration_store.record_conversation(event)


@app.post("/integrations/storefront/orders", response_model=StorefrontOrderIngest, dependencies=[Depends(require_api_key)])
def ingest_storefront_order(event: StorefrontOrderIngest) -> StorefrontOrderIngest:
    return integration_store.record_order(event)


@app.post("/integrations/storefront/cart", response_model=StorefrontCartIngest, dependencies=[Depends(require_api_key)])
def ingest_storefront_cart(event: StorefrontCartIngest) -> StorefrontCartIngest:
    return integration_store.record_cart(event)


@app.get("/integrations/customers/{customer_id}", response_model=CustomerSnapshot, dependencies=[Depends(require_api_key)])
def get_customer_snapshot(customer_id: str) -> CustomerSnapshot:
    snapshot = integration_store.get_customer_snapshot(customer_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="مشتری در داده‌های همگام‌شده پیدا نشد")
    return snapshot


@app.post("/integrations/customers/{customer_id}/decide", response_model=Decision, dependencies=[Depends(require_api_key)])
def decide_from_integrations(customer_id: str) -> Decision:
    snapshot = integration_store.get_customer_snapshot(customer_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="مشتری در داده‌های همگام‌شده پیدا نشد")
    decision = decide(snapshot.customer)
    decision_store.log_decision(decision)
    return decision


@app.get("/reports/campaigns", response_model=CampaignReport, dependencies=[Depends(require_api_key)])
def campaign_report() -> CampaignReport:
    decisions = decision_store.status_counts()
    feedback = feedback_store.summary()
    return CampaignReport(
        total_decisions=decisions["total"],
        approved_decisions=decisions["approved"],
        rejected_decisions=decisions["rejected"],
        pending_decisions=decisions["pending"],
        feedback_count=feedback["feedback_count"],
        opened_count=feedback["opened_count"],
        purchased_count=feedback["purchased_count"],
        purchase_rate=feedback["purchase_rate"],
    )
