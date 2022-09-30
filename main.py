from Any import Callable
from fastapi import FastAPI, Request
from middleware_handler import add_middleware_handler

app = FastAPI()

def create_test_middleware(str: string) -> Callable:
    async def middleware_lambda(request: Request, call_next) -> Response:
        print(str)
        return await call_next(request)
    return middleware_lambda

application.middleware("http")(middleware.handle)
middleware_handler = add_middleware_handler(app)
