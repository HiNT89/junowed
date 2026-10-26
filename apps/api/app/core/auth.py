"""Temporary development authentication boundary.

Replace this dependency with session/JWT verification before exposing authenticated
routes publicly.  Tests can override it without involving an identity provider.
"""

from uuid import UUID

from fastapi import Header

from app.core.errors import APIError


def current_user_id(x_user_id: str | None = Header(default=None)) -> str:
    if not x_user_id:
        raise APIError(401, "UNAUTHORIZED", "Missing X-User-Id development header")
    try:
        return str(UUID(x_user_id))
    except ValueError as exc:
        raise APIError(401, "UNAUTHORIZED", "Invalid user identity") from exc
