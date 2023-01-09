from typing import Callable
from fastapi import FastAPI, Request, Response
from middleware_handler import add_middleware_handler
import string

app = FastAPI()

def create_test_middleware(str: string) -> Callable:
    async def middleware_lambda(request: Request, call_next) -> Response:
        print(str)
        return await call_next(request)
    return middleware_lambda

# create your middleware handler
middleware_handler = add_middleware_handler(app)


# add your middlewares and path
middleware_handler.add_middleware(create_test_middleware("middle one")) # no URI path means over whole application
middleware_handler.add_middleware(create_test_middleware("middle two"), "/this/path")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/this/path")
async def root():
    return {"message": "Hello World Again"}