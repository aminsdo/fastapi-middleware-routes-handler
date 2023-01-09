# FastAPI - middlewares with routes
Run example with `uvicorn example:app --reload`

Does not manage filtering HTTP method, it is advised to handle it in your own middleware.

### Usage : 

create your middleware handler

`middleware_handler = add_middleware_handler(app)`

add your middlewares and path

`middleware_handler.add_middleware(create_test_middleware("middle one")) # no URI path means over whole application`

`middleware_handler.add_middleware(create_test_middleware("middle two"), "/this/path")`
