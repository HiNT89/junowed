import hashlib
import hmac

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import APIError
from app.db.models import Entitlement, Order, Payment, PaymentWebhookEvent
from app.db.session import get_db

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/webhooks/{provider}")
async def payment_webhook(
    provider: str,
    request: Request,
    signature: str | None = Header(default=None, alias="X-Webhook-Signature"),
    db: Session = Depends(get_db),
) -> dict:
    body = await request.body()
    expected = hmac.new(
        get_settings().payment_webhook_secret.encode(), body, hashlib.sha256
    ).hexdigest()
    if not signature or not hmac.compare_digest(signature, expected):
        raise APIError(401, "UNAUTHORIZED", "Invalid webhook signature")
    try:
        event = await request.json()
        event_id, order_id = event["eventId"], event["orderId"]
        amount, currency = int(event["amount"]), event["currency"]
    except (KeyError, TypeError, ValueError) as exc:
        raise APIError(422, "INVALID_CONFIG", "Malformed payment event") from exc
    if db.scalar(
        select(PaymentWebhookEvent).where(
            PaymentWebhookEvent.provider == provider, PaymentWebhookEvent.event_id == event_id
        )
    ):
        return {"status": "duplicate"}
    payment = db.scalar(
        select(Payment).where(Payment.order_id == order_id, Payment.provider == provider)
    )
    order = db.get(Order, order_id)
    if not payment or not order or amount != order.amount or currency != order.currency:
        raise APIError(422, "INVALID_CONFIG", "Payment does not match authoritative order")
    db.add(PaymentWebhookEvent(provider=provider, event_id=event_id))
    payment.transaction_id = event.get("transactionId")
    payment.raw_event = event
    if event.get("status") == "SUCCEEDED":
        payment.status, order.status = "SUCCEEDED", "PAID"
        entitlement = db.scalar(
            select(Entitlement).where(
                Entitlement.wedding_id == order.wedding_id, Entitlement.kind == "PUBLISH"
            )
        )
        if entitlement:
            entitlement.active = True
        else:
            db.add(Entitlement(wedding_id=order.wedding_id, kind="PUBLISH", active=True))
    else:
        payment.status = "FAILED"
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate"}
    return {"status": "processed"}
