web: DJANGO_SETTINGS_MODULE=project.settings daphne project.asgi:application --port $PORT --bind 0.0.0.0 -v2
release: bash -c "python manage.py migrate && python manage.py collectstatic --noinput"

