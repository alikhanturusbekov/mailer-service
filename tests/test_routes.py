import aiosmtplib
import httpx
import pytest
from httpx import AsyncClient
from pytest import MonkeyPatch

from starlette import status

from src.config import SENDER_EMAIL
from src.client import smtp_server
from tests.constants import ErrorMessage


@pytest.mark.asyncio
async def test_healthcheck(fake_client: AsyncClient):
    resp = await fake_client.get("/healthcheck")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": "ok"}


@pytest.mark.parametrize(
    "from_email, to_email, subject, body",
    (
            (SENDER_EMAIL, 'receiver@test.com', 'Test Subject', 'Test Content'),
            (SENDER_EMAIL, 'alikhan@gmail.com', 'Alikhan Subject', 'Test Content 2'),
    )
)
@pytest.mark.asyncio
async def test_send_email_valid(
        from_email: str,
        to_email: str,
        subject: str,
        body: str,
        fake_client: AsyncClient,
        fake_smtp_server: aiosmtplib.SMTP,
        monkeypatch: MonkeyPatch,
):
    # Test required mocking AS mailhog does not make tsl connection
    # noinspection PyShadowingNames
    async def mock_sendmail(from_email, to_email, msg):
        await fake_smtp_server.sendmail(from_email, to_email, msg)
        return {}, {'ok': 'Everything is good'}

    monkeypatch.setattr(smtp_server.client, "sendmail", mock_sendmail)

    resp = await fake_client.post(
        "/send_email",
        json={
            "to": to_email,
            "subject": subject,
            "message": body,
        },
    )

    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = httpx.get("http://localhost:8025/api/v2/messages")

    assert resp.status_code == status.HTTP_200_OK

    content = resp.json()["items"][0]["Content"]
    headers = content["Headers"]

    assert headers["From"] == [SENDER_EMAIL]
    assert headers["To"] == [to_email]
    assert headers["Subject"] == [subject]
    assert body in content["Body"]


@pytest.mark.parametrize(
    "to_email, subject, body, error_message",
    (
        ('receiver', 'Test Subject', 'Test Content', ErrorMessage.INVALID_EMAIL_AT),
        ('receiver@test', 'Test', 'Test Content', ErrorMessage.INVALID_EMAIL_DOT),
        ('receiver@test.com', 'Test'*100, 'Test Content', ErrorMessage.MAX_LENGTH_255),
        ('receiver@gmail.com', 'Test', '', ErrorMessage.MIN_LENGTH_1),
    )
)
@pytest.mark.asyncio
async def test_send_email_invalid(
        to_email: str,
        subject: str,
        body: str,
        error_message: str,
        fake_client: AsyncClient,
):
    resp = await fake_client.post(
        "/send_email",
        json={
            "to": to_email,
            "subject": subject,
            "message": body,
        },
    )

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert resp.json()['detail'][0]['msg'] == error_message
