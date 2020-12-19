## Initial Project Setup

To start the project:

```bash
mkdir ninety_nine_cats
cd ninety_cats
pyenv virtualenv ninety_nine_cats
pyenv local ninety_nine_cats
pip install --upgrade pip
pip install Django
pip freeze > requirements.txt
django-admin startproject ninety_nine_cats .
```

To run the server (default port 8000):

```python
./manage.py runserver
```

The server should auto-restart when code changes.

## Starting the `cats` App

Django distinguishes the concept of "project" from "app." An "app" is a
reusable part of the larger project. I think an example is the admin
panel is an app that you can add.

First, let's setup pylint:

```
pip install pylint-django
pip freeze > requirements.txt
```

And add these lines to `.vscode/settings.json`:

```json
{
  "python.pythonPath": "/Users/ruggeri/.pyenv/versions/ninety_nine_cats/bin/python",
  "python.linting.pylintArgs": [
    "--load-plugins",
    "pylint_django",
    // missing-module-docstring (C0114),
    // missing-class-docstring (C0115),
    // missing-function-docstring (C0116),
    // bad-indentation (W0311),
    // bad-continuation (C0330),
    // too-few-public-methods (R0903),
    "--disable=C0114,C0115,C0116,W0311,C0330,R0903"
  ]
}
```

Next, let's create a very basic view function in `cats/views.py`:

```python
from django.http import HttpResponse

def index(request):
  return HttpResponse("Hello world!")
```

And let's connect it to a url in `cats/urls.py` (you'll have to touch
the file to make it first):

```python
from django.urls import path
from . import views

# name gives us a way to construct a url later.
urlpatterns = [path('', views.index, name="index")]
```

Last, setup the url in `ninety_nine_cats/urls.py`:

```python
from django.contrib import admin
# include is used to mount an app at a path.
from django.urls import include, path

urlpatterns = [
    path('cats/', include('cats.urls')), # << this is the line to add
    path('admin/', admin.site.urls),
]
```
