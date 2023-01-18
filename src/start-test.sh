#!/usr/bin/env bash

alembic revision --autogenerate & alembic upgrade head & pytest -s -v tests/*/*.py