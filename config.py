from pathlib import Path
import os
import dotenv

BASE_DIR = Path(__file__).parent.resolve()

dotenv_file = os.path.join(BASE_DIR, '.env')

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

#API's

MAILCHIMP_API_KEY = os.environ['MAILCHIMP_SECRET_KEY']
MAILCHIMP_SERVER_PREFIX = "us14"
MAILCHIMP_AUDIENCE_ID = "39b91bfe2d"

STRIPE_PUBLISHABLE_KEY = 'pk_test_51Ot6RcP3PWsPMy1XKoc5BRUC4z4ebbGJpJn0FRRcHGtj1Cvw3KdU1jKzYqdN4lk0xn3h8VXmN1KUjSleR4bdqpaP00q9Mj9BsF'
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']

SHIPPO_API_KEY = os.environ['SHIPPO_SECRET_KEY']

#CELERY

#celery -A your_project_name worker --loglevel=info
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

#JWT

#openssl rsa -in private.key -aes256 -out private_encrypted.key
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

#openssl rsa -in private_encrypted.key -out private.key
JWT_PUBLIC_KEY = """MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0XfbwnAICqX2XYVUNyDR
                    nip5K+16Veb+sS9lBkKb7QgWfft6cucaC1XLq5FwLuD8N3ZjL/XFw6BFgLAQlgez
                    PMZ+FHA76NTR6LqFjR1IfmjK/9azQWE1mXiP3epDwWPeHRsF4D0jzbIlKJlNFFym
                    f0KI4wA31GEnmzmnqE5MkYCpznsOJGguKX39G2qdz6jA0JsPym80hNHLVn+ER2VS
                    rBTygv8woveKZB36WaNI+8HhmNNPwU1pHgmOKTgauZQRCkTn1phZwqcmWuJk63xj
                    W+R6TL6AZdkMyo4veUEyqokxUKOu6NHRdc0xDSz/cKvdBag5Fm599yrQHP/Wzp6N
                    LwIDAQAB"""

#set expiry of json web tokens by mins
ACCESS_JWTOKEN_EXPIRY = 15
REFRESH_JWTOKEN_EXPIRY = 600