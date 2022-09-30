from typing import Callable
from urllib.parse import urlparse
from fastapi import Request, Response
from prometheus_client import Counter


def add_middleware_handler(application):
    middleware = MiddlewareHandler()
    application.middleware("http")(middleware.handle)
    return middleware


class MiddlewareHandler:
    def __init__(self):
        self.middleware_requests_metric = Counter(
            "middleware_handler_requests_total",
            "Requests processed by the middleware",
            ["middleware"],
        )
        self.middlewares = []
        self.index = 0
        self.length = 0
        self.path = ""
        self.final_call_next = None

    def add_middleware(self, middleware: Callable, route='/'):
        self.middlewares.insert(0, (route, middleware))

    async def call_next(self, request: Request) -> Response:
        while self.index < self.length:
            route, middleware = self.middlewares[self.index]
            self.index += 1
            if self.path.startswith(route):
                self.middleware_requests_metric.labels(middleware.__name__)\
                    .inc()
                return await middleware(request, self.call_next)
        return await self.final_call_next(request)

    async def handle(self, request: Request, call_next) -> Response:
        self.index = 0
        self.length = len(self.middlewares)
        self.path = urlparse(str(request.url)).path
        self.final_call_next = call_next
        return await self.call_next(request)
