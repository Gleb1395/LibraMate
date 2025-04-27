#!/bin/bash

cd src

python manage.py migrate
python manage.py check
python manage.py runserver 0:8000 & python -m services.send_telegram_notifications

