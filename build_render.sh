#!/usr/bin/env bash
set -e

pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=ERROR_PROOFING.settings

cd CONTROL_HELADERAS
python manage.py collectstatic --noinput
