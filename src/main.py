from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.client import smtp_server
from src.config import ALLOWED_CORS_ORIGINS, ALLOWED_CORS_HEADERS
from src.router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGINS,
    allow_methods=("GET", "POST"),
    allow_headers=ALLOWED_CORS_HEADERS,
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    await smtp_server.configure()


@app.on_event("shutdown")
async def shutdown():
    await smtp_server.quit()
