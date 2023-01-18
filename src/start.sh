#!/usr/bin/env bash

alembic revision --autogenerate
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000 --reload