import time
from collections import defaultdict, deque
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rules: dict[str, tuple[int, float]]):
        
        #rules: mapping from path-prefix to (max_calls, period_seconds)
        
        super().__init__(app)
        self.rules = rules
        self.history: dict[tuple[str,str], deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        now = time.monotonic()
        client_ip = request.client.host or "anon"
        path = request.url.path

        for prefix, (max_calls, period) in self.rules.items():
            if path.startswith(prefix):
                key = (client_ip, prefix)
                q = self.history[key]

                # remove timestamps older than window
                while q and q[0] <= now - period:
                    q.popleft()

                # if over the limit, reject
                if len(q) >= max_calls:
                    return JSONResponse(
                        {"detail": "Too many requests"},
                        status_code=429
                    )

                # record this call
                q.append(now)
                break  # only apply the first matching rule

        return await call_next(request)
