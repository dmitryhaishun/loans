from fastapi import FastAPI

from app.api.api import api
from app.db.session import dispose_engine, get_or_create_engine
from app.logging import start_logging

app = FastAPI(
    title="Loans",
    description="On this page you can get the loans.",
    version="v0.0.1",
)


@app.on_event("startup")
async def startup():
    get_or_create_engine()
    start_logging()


@app.on_event("shutdown")
async def shutdown():
    await dispose_engine()


app.include_router(api)
