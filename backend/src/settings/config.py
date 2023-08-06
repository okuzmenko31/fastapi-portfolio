import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

# SECRET KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

# JWT TOKENS
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE', '30'))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")

# SMTP HOST CONNECTION
SMTP_HOST = os.environ.get('EMAIL_HOST')
SMTP_USER = os.environ.get('EMAIL_HOST_USER')
SMTP_USERNAME = SMTP_USER.split('@')[0]
SMTP_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SMTP_PORT = os.environ.get('EMAIL_PORT')

# CELERY
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq//'
CELERY_BACKEND_URL = 'amqp://guest:guest@rabbitmq//'

# API KEY
api_key = os.getenv('API_KEY')

# DEBUG MODE
DEBUG = os.getenv('DEBUG', True)

if DEBUG == 'True':
    DEBUG = True
elif DEBUG == 'False':
    DEBUG = False
