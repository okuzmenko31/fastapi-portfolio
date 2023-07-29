#!/bin/sh

sleep 10

alembic upgrade head

cd /portfolio/backend

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload
