import os
import django
from django.conf import settings
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comments.settings')

django.setup()

with connection.cursor() as cursor:
    tables = connection.introspection.table_names()
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")

print("База данных очищена. Можно продолжить миграцию.")