from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import current_user_id
from app.core.config import get_settings
from app.core.errors import APIError
from app.db.models import Order, Payment, Wedding
from app.db.session import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


class CreateOrderRequest(BaseModel):
    wedding_id: str = Field(alias="weddingId")
    provider: str = Field(default="manual", pattern=r"^[a-z0-9_-]{1,64}$")


def serialize_order(order: Order, payment: Payment | None) -> dict:
    return {
        "id": order.id,
        "weddingId": order.wedding_id,
        "amount": order.amount,
        "currency": order.currency,
        "status": order.status,
        "payment": None
        if not payment
        else {"provider": payment.provider, "status": payment.status},
    }


@router.post("", status_code=201)
def create_order(
    payload: CreateOrderRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    user_id: str = Depends(current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    if not idempotency_key:
        raise APIError(422, "INVALID_CONFIG", "Idempotency-Key is required")
    wedding = db.get(Wedding, payload.wedding_id)
    if not wedding or wedding.owner_id != user_id:
        raise APIError(404, "NOT_FOUND", "Wedding not found")
    existing = db.scalar(
        select(Order).where(Order.user_id == user_id, Order.idempotency_key == idempotency_key)
    )
    if existing:
        return serialize_order(
            existing, db.scalar(select(Payment).where(Payment.order_id == existing.id))
        )
    order = Order(
        user_id=user_id,
        wedding_id=wedding.id,
        amount=get_settings().wedding_publish_price_vnd,
        currency="VND",
        idempotency_key=idempotency_key,
    )
    db.add(order)
    db.flush()
    payment = Payment(order_id=order.id, provider=payload.provider, amount=order.amount)
    db.add(payment)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise APIError(409, "INVALID_CONFIG", "Duplicate order idempotency key") from exc
    return serialize_order(order, payment)


@router.get("/{order_id}")
def get_order(
    order_id: str, user_id: str = Depends(current_user_id), db: Session = Depends(get_db)
) -> dict:
    order = db.scalar(select(Order).where(Order.id == order_id, Order.user_id == user_id))
    if not order:
        raise APIError(404, "NOT_FOUND", "Order not found")
    return serialize_order(order, db.scalar(select(Payment).where(Payment.order_id == order.id)))
