# Djanglavel

* Project manager : <cyberj@arcagenis.org>
* Developpers : <cyberj@arcagenis.org>
* Repository : https://github.com/cyberj/djanglavel.git
* Tracker :
* Django version : 1.8.3
* Python version : 3.4

This is just a personal test to compare [Laravel](http://laravel.com/) framework with [Django](http://djangoproject.com) framework

## Manual install

Do:

```sh
virtualenv vtenv
source ./vtenv/bin/activate
pip install -Mr requirements.txt
```

Create a file `djanglavel/local_settings.py` with:

```python
SECRET_KEY = 's8j796v@y&6jb6v7=3!mz+@539h)oza!@6)y69a#tcpncvdkh'
DATABASES = {}

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.dat',
}
```

Then:

```sh
./manage.py migrate
./manage.py test
./manage.py runserver
```
