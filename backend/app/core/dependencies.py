import uuid
from typing import Optional

from fastapi import Depends, Header

from .auth import get_current_user


class RequestContext:
    def __init__(self, user_id: Optional[str], session_id: str):
        self.user_id = user_id
        self.session_id = session_id


def get_request_context(
    user_id: Optional[str] = Depends(get_current_user),
    x_session_id: Optional[str] = Header(default=None),
) -> RequestContext:
    if not x_session_id:
        x_session_id = str(uuid.uuid4())
    return RequestContext(user_id=user_id, session_id=x_session_id)
