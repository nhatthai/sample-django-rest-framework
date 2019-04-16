# Django and Rest Framework

### Technical stacks
+ Python v3.6
+ Django v2.1
+ Django Rest Framework v3.9.2

### Backend Frameworks
-----------------------
* [Django](https://www.djangoproject.com/)
    - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

* [psycopg2](https://pypi.python.org/pypi/psycopg2)
    - PostgreSQL database adapter for Python.

* [Requests](https://pypi.python.org/pypi/requests/2.11.1)
    - Requests is the only Non-GMO HTTP library for Python, safe for human consumption.

* [Django-Extensions](https://github.com/django-extensions/django-extensions)
    - Django Extensions is a collection of custom extensions for the Django Framework.

* [Djanog Rest Framework](https://www.django-rest-framework.org/)
    - Django REST framework is a powerful and flexible toolkit for building Web APIs.

### Database
-------------
* [PostgresSQL](https://www.postgresql.org/)
    - PostgreSQL is a powerful, open source object-relational database system. It has more than 15 years of active development and a proven architecture that has earned it a strong reputation for reliability, data integrity, and correctness.

### Usage
----------
#### Build mysite django
```
cd backend
docker build -t nhatthai/mysite_django2.1:latest .
```

#### Push to Docker HUb
```
docker push nhatthai/mysite_django2.1:latest
```