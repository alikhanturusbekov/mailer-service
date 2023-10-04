import aiosmtplib
import pytest_asyncio
from httpx import AsyncClient

from src.main import app


@pytest_asyncio.fixture
async def fake_smtp_server():
    async with aiosmtplib.SMTP("localhost", 1025) as server:
        yield server


@pytest_asyncio.fixture
async def fake_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
