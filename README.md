# Djanglavel

* Author : <cyberj@arcagenis.org>
* Repository : https://github.com/cyberj/djanglavel.git
* Django version : 1.8.3
* Python version : 3.4

This is just a personal test to compare [Laravel](http://laravel.com/) framework with [Django](http://djangoproject.com) framework.

* [Laravgo](https://github.com/cyberj/laravgo) for Laravel
* [Djanglavel](https://github.com/cyberj/djanglavel) for Django

## Manual install

Do:

```sh
virtualenv vtenv
source ./vtenv/bin/activate
pip install -Mr requirements.txt
```

You can customize some params by creating a file like  `djanglavel/local_settings.py` with:

```python
SECRET_KEY = 's8j796v@y&6jb6v7=3!mz+@539h)oza!@6)y69a#tcpncvdkh'
DATABASES = {}

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3',
}
```

Then:

```sh
./manage.py migrate
./manage.py test
./manage.py runserver
```
