import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

SMTP_HOST = os.environ.get('EMAIL_HOST')
SMTP_USER = os.environ.get('EMAIL_HOST_USER')
SMTP_USERNAME = SMTP_USER.split('@')[0]
SMTP_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SMTP_PORT = os.environ.get('EMAIL_PORT')
