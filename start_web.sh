#!/usr/bin/env bash
set -e

export DJANGO_SETTINGS_MODULE=ERROR_PROOFING.settings

cd CONTROL_HELADERAS
python manage.py collectstatic --noinput
python manage.py migrate --noinput
exec daphne -b 0.0.0.0 -p "$PORT" ERROR_PROOFING.asgi:application
