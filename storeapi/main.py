import logging
from contextlib import asynccontextmanager

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler

from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.posts import router as posts_router
from storeapi.routers.upload import router as uploads_router
from storeapi.routers.users import router as users_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(posts_router, prefix="/posts")
app.include_router(users_router, prefix="/users")
app.include_router(uploads_router, prefix="/uploads")


@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request: Request, exception: HTTPException):
    logger.error(f"HTTPException: {exception.status_code} {exception.detail}")

    return await http_exception_handler(request, exception)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
