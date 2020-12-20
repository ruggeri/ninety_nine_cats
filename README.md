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

## Database Setup

In `ninety_nine_cats/settings.py` there is some database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

We won't go deeper into setting up Postgres right away. But you can see
it is here. We will run the default generated migration files (for admin
console, et cetera):

```
./manage.py migrate
```

Now you can run `sqlite3 db.sqlite3` and run `.schema --indent` to see
the default created schema.

Let's make our first models in `cats/models.py`:

```python
from django.db import models

# Each subclass of models.Model represents a model
class Cat(models.Model):
  # The fields are described as class properties. Every field has their
  # own options, which we will review some future time.
  name = models.CharField(max_length=255)
  age = models.IntegerField()

class Toy(models.Model):
  # Foreign key is going to create a property `cat` which fetches the
  # associated object. I believe it will also create a `toys` field.
  cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
```

To generate migrations, we must first list the `cats` app as amongst the
`INSTALLED_APPS` in `ninety_nine_cats/settings.py`:

```python
INSTALLED_APPS = [
    'cats.apps.CatsConfig',
    '...'
]
```

And let's make the migrations:

```
>> ./manage.py makemigrations
Migrations for 'cats':
  cats/migrations/0001_initial.py
    - Create model Cat
    - Create model Toy
```

We can examine these; they're a lot like migrations written in
JavaScript style ORMs. We can run the migration with:

```
>> ./manage.py sqlmigrate cats 0001
...will print out the sql it would run, for you to examine and learn from...
>> ./manage.py migrate cats
```

We'll now setup the iPython REPL:

```
pip install django-extensions
pip install ipython
pip freeze > requirements.txt
# ADD 'django_extensions' to INSTALLED_APPS in settings.py.
./manage.py shell_plus --ipython
# And SHELL_PLUS = "ipython" to settings.py. Makes iPython the default.
./manage.py shell_plus
```

The glory of this is that it will autoload your models!

## Basics With Models

```ipython
# Basic query to get all
In [2]: Cat.objects.all()
Out[2]: <QuerySet []>

# Make a new cat
In [4]: c = Cat(name="Markov", age=8)
In [6]: c.__dict__
Out[6]:
{'_state': <django.db.models.base.ModelState at 0x1123d7910>,
 'id': None,
 'name': 'Markov',
 'age': 8}

# Save a cat
In [7]: c.save()
In [9]: c.__dict__
Out[9]:
{'_state': <django.db.models.base.ModelState at 0x1123d7910>,
 'id': 1,
 'name': 'Markov',
 'age': 8}
```

We can change the output representation of our models:

```python
# cats/models.py
class Cat(models.Model):
  # ...

  def __str__(self):
    return self.name

class Toy(models.Model):
  # ...

  def __str__(self):
    return self.name
```

Let's practice with some querying:

```ipython
# Lookup single object by id
In [5]: c = Cat.objects.get(id=1); c
Out[5]: <Cat: Markov>

# Lookup single object by field.
# Will give error if more than one result is returned.
In [7]: c = Cat.objects.get(name__startswith="M"); c
Out[7]: <Cat: Markov>

# Filter may contain many
In [9]: c = Cat.objects.filter(name__startswith="M"); c
Out[9]: <QuerySet [<Cat: Markov>]>

# QuerySet is lazily evaluated and chainable
In [10]: c = Cat.objects.filter(name__startswith="M").filter(name__endswith="v"); c
Out[10]: <QuerySet [<Cat: Markov>]>

# Better
In [15]: c = Cat.objects.filter(name__startswith="M", name__endswith="v")

In [16]: c
Out[16]: SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 WHERE ("cats_cat"."name" LIKE '%v' ESCAPE '\' AND "cats_cat"."name" LIKE 'M%' ESCAPE '\')
 LIMIT 21

Execution time: 0.000204s [Database: default]
<QuerySet [<Cat: Markov>]>

```

This is a good time to add the `--print-sql` flag to `shell_plus`. Add
`SHELL_PLUS_PRINT_SQL = True` to `settings.py`.

## Has Many Associated Object

Let's start making a `Toy` for our cat.

```ipython
In [23]: t = Toy(name="mousey")

In [24]: t.__dict__
Out[24]:
{'_state': <django.db.models.base.ModelState at 0x10e077f10>,
 'id': None,
 'cat_id': None,
 'name': 'mousey'}

# Trying to find an associated object will fail if no such object exists yet.
In [25]: t.cat
...errors...
RelatedObjectDoesNotExist: Toy has no cat.

In [26]: t.cat_id = 1

In [27]: t.__dict__
Out[27]:
{'_state': <django.db.models.base.ModelState at 0x10e077f10>,
 'id': None,
 'cat_id': 1,
 'name': 'mousey'}

In [28]: t.cat
SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 WHERE "cats_cat"."id" = 1
 LIMIT 21

Execution time: 0.000203s [Database: default]
Out[28]: <Cat: Markov>

# Query only happens the first time.
In [29]: t.cat
Out[29]: <Cat: Markov>

# But it's smart enough to require reload of the cat.
In [31]: t.cat_id = 2

In [32]: t.cat
SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 WHERE "cats_cat"."id" = 2
 LIMIT 21

Execution time: 0.000151s [Database: default]
Out[32]: <Cat: Maurice>
```

You can query from the other side:

```ipython
# Note that the inverse association is called `toy_set`.
In [40]: c.toy_set.all()
Out[40]: SELECT "cats_toy"."id",
       "cats_toy"."cat_id",
       "cats_toy"."name"
  FROM "cats_toy"
 WHERE "cats_toy"."cat_id" = 1
 LIMIT 21

Execution time: 0.000138s [Database: default]
<QuerySet []>

# The query appears to be re-run every time.

# Naturally it doesn't know about Maurice's toy (I haven't saved it yet).
In [43]: c2 = Cat.objects.get(id=2); c2.toy_set.all()
SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 WHERE "cats_cat"."id" = 2
 LIMIT 21

Execution time: 0.000152s [Database: default]
Out[43]: SELECT "cats_toy"."id",
       "cats_toy"."cat_id",
       "cats_toy"."name"
  FROM "cats_toy"
 WHERE "cats_toy"."cat_id" = 2
 LIMIT 21

Execution time: 0.000087s [Database: default]
<QuerySet []>

# Saved the toy.
In [44]: t.save()
INSERT INTO "cats_toy" ("cat_id", "name")
VALUES (2, 'mousey')

Execution time: 0.001734s [Database: default]

# Now the toy is found!
In [45]: c2.toy_set.all()
Out[45]: SELECT "cats_toy"."id",
       "cats_toy"."cat_id",
       "cats_toy"."name"
  FROM "cats_toy"
 WHERE "cats_toy"."cat_id" = 2
 LIMIT 21

Execution time: 0.000144s [Database: default]
<QuerySet [<Toy: mousey>]>

# You can even get toys by associated object data.
In [48]: Toy.objects.filter(cat__name="Maurice")
Out[48]: SELECT "cats_toy"."id",
       "cats_toy"."cat_id",
       "cats_toy"."name"
  FROM "cats_toy"
 INNER JOIN "cats_cat"
    ON ("cats_toy"."cat_id" = "cats_cat"."id")
 WHERE "cats_cat"."name" = 'Maurice'
 LIMIT 21

Execution time: 0.000122s [Database: default]
<QuerySet [<Toy: mousey>]>

# And it works in the opposite direction too. Note that the
# inverse association is just called toy when used this way.
In [49]: Cat.objects.filter(toy__name="mousey")
Out[49]: SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 INNER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
 WHERE "cats_toy"."name" = 'mousey'
 LIMIT 21

Execution time: 0.000212s [Database: default]
<QuerySet [<Cat: Maurice>]>

```

## Admin Cosole Basics

Start by creating a super user:

```
./manage.py createsuperuser
```

You can now login via `http://localhost:8000/admin/`.

To administer your models, go to `cats/admin.py`:

```python
# cats/admin.py
from django.contrib import admin
from . import models

admin.site.register(models.Cat)
admin.site.register(models.Toy)
```

For free, this will give you admin pages to CRUD your model objects.

## TODO

* How to setup Postgres?
* Django Rest Framework.
* Various attributes of model properties.
* How associations are done. Go deeper into associated objects/creation.
* Chaining queries onto QuerySet.

## Tutorials

* Tutorial Pages
  * https://docs.djangoproject.com/en/3.1/intro/tutorial03/
  * https://docs.djangoproject.com/en/3.1/intro/tutorial04/
  * https://docs.djangoproject.com/en/3.1/intro/tutorial05/
  * https://docs.djangoproject.com/en/3.1/intro/tutorial06/
  * https://docs.djangoproject.com/en/3.1/intro/tutorial07/
* More documentation:
  * https://docs.djangoproject.com/en/3.1/
  * TODO: review to see what additional doc pages are useful.
