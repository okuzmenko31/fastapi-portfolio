FROM python:3.9

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /portfolio/backend
COPY . .

RUN pip install "poetry"

COPY start.sh /portfolio/start.sh
COPY celery.sh /portfolio/celery.sh
COPY poetry.lock /portfolio/backend

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
RUN chmod +x /portfolio/start.sh
RUN chmod +x /portfolio/celery.sh

EXPOSE 8000

CMD ["/portfolio/start.sh"]
