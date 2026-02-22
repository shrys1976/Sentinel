from csv import unregister_dialect
from fastapi import Header
from typing import Optional
import uuid

class RequestContext:

    def __init__(

        self,
        user_id: Optional[str],
        session_id:str
    ):

        self.user_id = user_id
        self.session_id = session_id

def get_request_context(

    x_session_id : Optional[str] = Header(default=None),
):

    user_id = None
    if not x_session_id:

        x_session_id = str(uuid.uuid4())

    return RequestContext(

        user_id  = user_id,
        session_id = x_session_id

    )        
