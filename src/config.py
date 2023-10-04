from starlette.config import Config

config = Config(".env")

ALLOWED_CORS_ORIGINS = config(
    "ALLOWED_CORS_ORIGINS",
    cast=lambda x: x.split(",")
)
ALLOWED_CORS_HEADERS = config(
    "ALLOWED_CORS_HEADERS",
    cast=lambda x: x.split(",")
)

SMTP_SERVER = config("SMTP_SERVER")
SMTP_PORT = config("SMTP_PORT")
SMTP_TLS = config("SMTP_TLS", default=False)
SMTP_LOGIN = config("SMTP_LOGIN")
SMTP_PASSWORD = config("SMTP_PASSWORD")
SENDER_EMAIL = config("SENDER_EMAIL")
