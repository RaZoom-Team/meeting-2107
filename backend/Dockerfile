FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get -y update; apt-get -y install curl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN chmod +x entry.sh
ENTRYPOINT [ "sh", "entry.sh" ]