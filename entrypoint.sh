#!/bin/bash

cd /usr/src/app

# create database if not exists yet
python - <<EOF
#!/usr/share/env python3
import _mysql
import os
connection = _mysql.connect(os.environ['HPI_QUOTEDB_DB_HOST'],
		os.environ['HPI_QUOTEDB_DB_USER'],
		os.environ['HPI_QUOTEDB_DB_PASSWORD'])
connection.query("CREATE DATABASE IF NOT EXISTS " + os.environ['HPI_QUOTEDB_DB_NAME'])
connection.close()
EOF

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

# create default superadmin if none exists right now
python3 - <<EOF
import django
django.setup()

from django.contrib.auth.models import User

if User.objects.filter(is_superuser=True).count() < 1:
	User.objects.create_superuser('db_admin', 'test@test.de', 'def4ultP@assword')
EOF

/usr/local/bin/gunicorn hpi_quotedb.wsgi:application -w 2 -b :8000

