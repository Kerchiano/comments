python clear_db.py
python manage.py makemigrations  --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8000 comments.asgi:application