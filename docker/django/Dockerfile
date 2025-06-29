FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BOUNDED_CONTEXTS "shop_management,user_management,cart_management,review_management,notification_management,order_management,payment_management"

WORKDIR /app

COPY ../modular_monolith /app
RUN pip install --upgrade pip && pip install -r requirements.txt

