FROM python:3.12-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./src /app

COPY ./migrations /app/migrations
COPY ./alembic.ini /app/alembic.ini
COPY ./entry.sh /app/entry.sh
RUN chmod +x /app/entry.sh

ENTRYPOINT [ "./entry.sh" ]