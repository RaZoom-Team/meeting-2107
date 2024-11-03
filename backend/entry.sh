#!/bin/bash
alembic upgrade head
gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --workers 2 --bind "0.0.0.0:80" --access-logfile -