from fastapi import APIRouter
from starlette import status

from src.client import smtp_server
from src.schemas import EmailData

router = APIRouter()


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@router.post(
    "/send_email",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def send_email(email_data: EmailData):
    await smtp_server.send_email(email_data)
