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
