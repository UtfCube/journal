#!/bin/sh
source venv/bin/activate
flask db upgrade
exec gunicorn -b :8000 journal:app