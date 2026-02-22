import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
            duration = time.perf_counter() - start
            logger.info(
                "method=%s path=%s status=%s time=%.3fs",
                method,
                path,
                response.status_code,
                duration,
            )
            return response
        except Exception:
            duration = time.perf_counter() - start
            logger.exception(
                "request failed method=%s path=%s time=%.3fs",
                method,
                path,
                duration,
            )
            raise
