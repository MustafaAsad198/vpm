# Vendor Management System

### Tech-Stack used:
* Python
* Django Rest Framework

Purchase orders, vendor performance data, and vendor profiles will all be managed by this system.

## Command to create and run this project

### clone the repository

```
git clone https://github.com/MustafaAsad198/vpm
```

### install requirements

```
pip install django
```
```
pip install djangorestframework
```
```
pip install django-cors-headers
```

### run migration to register models in admin
```
python manage.py makemigrations
python manage.py migrate
```

### create a super user for admin panel
```
python manage.py createsuperuser
```

### to run django server on your localhost
```
python manage.py runserver
```

You can open the local server on Postman (or any other API testing application) and try implenting the APIs through given URL patterns in core/urls.py
