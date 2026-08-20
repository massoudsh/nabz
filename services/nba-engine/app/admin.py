"""پنل مدیریتی حداقلی فروشنده — issue #3.

MVP فاز ۱: لیست تصمیم‌های ثبت‌شده (decision_store) با امکان تایید/رد.
مدیریت کامل مشتریان و رابط پیشرفته‌تر خارج از این MVP و برای تکرار بعدی
گذاشته شده (docs/PRD.md بخش ۷/۸).
"""

from __future__ import annotations

import pathlib

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import decision_store
from app.auth import require_api_key

router = APIRouter()
_templates_dir = pathlib.Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(_templates_dir))


@router.get("/admin", response_class=HTMLResponse, dependencies=[Depends(require_api_key)])
def admin_dashboard(
    request: Request,
    status: str | None = None,
    api_key: str | None = Query(default=None),
) -> HTMLResponse:
    decisions = decision_store.list_decisions(status=status or None)
    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "decisions": decisions,
            "status_filter": status or "",
            "api_key": api_key or "",
        },
    )


@router.post("/admin/decisions/{decision_id}/{action}", dependencies=[Depends(require_api_key)])
def admin_update_decision(
    decision_id: str,
    action: str,
    api_key: str | None = Query(default=None),
) -> RedirectResponse:
    if action not in ("approve", "reject"):
        raise HTTPException(status_code=400, detail="عملیات نامعتبر (approve یا reject)")
    found = decision_store.set_status(decision_id, "approved" if action == "approve" else "rejected")
    if not found:
        raise HTTPException(status_code=404, detail="تصمیم یافت نشد")
    redirect_url = f"/admin?api_key={api_key}" if api_key else "/admin"
    return RedirectResponse(url=redirect_url, status_code=303)
