import time
import uuid
from typing import Callable

from fastapi import Request, Response


async def request_id_middleware(request: Request, call_next: Callable) -> Response:
    req_id = str(uuid.uuid4())
    request.state.request_id = req_id
    start = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)
    response.headers["x-request-id"] = req_id
    response.headers["x-response-time-ms"] = str(duration_ms)
    return response


