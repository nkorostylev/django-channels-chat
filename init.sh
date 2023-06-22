#!/bin/bash

python manage.py collectstatic --noinput
#
python manage.py migrate --run-syncdb

#python manage.py test
#python manage.py flush

echo "from core.models import CustomUser; CustomUser.objects.get(username='admin', is_superuser=True).delete()" | python manage.py shell 2> /dev/null
echo "from core.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin', 'admin', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
password=$(openssl rand -base64 12)
echo password: $password
echo "from core.models import CustomUser; CustomUser.objects.get(username='test', is_superuser=False).delete()" | python manage.py shell 2> /dev/null
echo "from core.models import CustomUser; CustomUser.objects.create_user('test', 'test@example.com', 'test', 'test', '$password')" | python manage.py shell
python manage.py runserver 0.0.0.0:8000