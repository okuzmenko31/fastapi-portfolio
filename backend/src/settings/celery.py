import asyncio

from celery import Celery
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jinja2 import Environment, PackageLoader, select_autoescape

from .config import *

app = Celery(__name__)
app.config_from_object('src.settings.config', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def send_auth_token_mail(subject: str, template: str, recipient: str, url: str):
    env = Environment(
        loader=PackageLoader('src.settings', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    conf = ConnectionConfig(
        MAIL_USERNAME=SMTP_USERNAME,
        MAIL_PASSWORD=SMTP_PASSWORD,
        MAIL_FROM=SMTP_USER,
        MAIL_PORT=SMTP_PORT,
        MAIL_SERVER=SMTP_HOST,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

    template = env.get_template(f'{template}.html')

    html = template.render(
        username=recipient,
        url=url,
        subject=subject
    )

    fm = FastMail(conf)
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=html,
        subtype="html"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fm.send_message(message))
