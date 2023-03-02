#!/bin/sh

while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py makemessages -l fa
python manage.py compilemessages

exec "$@"