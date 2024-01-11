cd /app

env >> /etc/environment
cron
python manage.py makemigrations
python manage.py migrate
python manage.py installtasks
python manage.py collectstatic --noinput

cp main.js static/jazzmin/js/main.js
cp django.po /usr/local/lib/python3.11/site-packages/django/contrib/admin/locale/uz/LC_MESSAGES/
cp django.mo /usr/local/lib/python3.11/site-packages/django/contrib/admin/locale/uz/LC_MESSAGES/

python manage.py runserver 0.0.0.0:8000