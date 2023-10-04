import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic import EmailStr

from src.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_LOGIN,
    SMTP_PASSWORD,
    SENDER_EMAIL,
    SMTP_TLS,
)
from src.schemas import EmailData
from src.logging import logger


class SMTPServer:
    def __init__(
        self,
        login: str = SMTP_LOGIN,
        password: str = SMTP_PASSWORD,
        hostname: str = SMTP_SERVER,
        port: int = SMTP_PORT,
        use_tls: bool = SMTP_TLS,
        sender: EmailStr = SENDER_EMAIL,
    ):
        self.sender = sender
        self.login = login
        self.password = password
        self.client = aiosmtplib.SMTP(
            hostname=hostname,
            port=port,
            use_tls=use_tls,
        )

    async def configure(self):
        logger.info(f"CONNECTING TO SMTP SERVER AT "
                    f"{self.client.hostname}:{self.client.port}...")
        await self.client.connect()

        logger.info("LOGGING TO SMTP SERVER...")
        await self.client.login(self.login, self.password)

        logger.info("SUCCESSFULLY LOGGED IN TO SMTP SERVER")

    async def quit(self):
        logger.info("QUITTING SMTP SERVER...")
        await self.client.quit()

    async def send_email(self, email_data: EmailData) -> None:
        logger.info(f"CONSTRUCTING AN EMAIL WITH SUBJECT: "
                    f"{email_data.subject}...")
        email = self._construct_email(email_data)

        logger.info(f"SENDING AN EMAIL TO {email_data.to}...")
        response = await self.client.sendmail(
            self.sender,
            email_data.to,
            email.as_string()
        )
        logger.info(f"RESPONSE STATUS:MESSAGE ---> {response[1]}")

    def _construct_email(self, email_data: EmailData) -> MIMEMultipart:
        msg = MIMEMultipart()

        msg["From"] = self.sender
        msg["To"] = email_data.to
        msg["Subject"] = email_data.subject
        msg.attach(MIMEText(email_data.message, "plain"))

        return msg


smtp_server = SMTPServer()
