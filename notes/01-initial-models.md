## Initial Models

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
