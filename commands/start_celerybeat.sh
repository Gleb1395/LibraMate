#!/bin/bash

celery -A config worker -l ${CELERY_LOG_LEVEL} -c ${CELERY_WORKERS_NUMBER} --beat --scheduler django