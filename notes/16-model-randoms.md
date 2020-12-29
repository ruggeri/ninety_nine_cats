### Search

They show how to use Postgres' document search features. These are DB
specific, and are more about pg than about Django. And they're in a
contrib library. So I don't really care.

### Managers

Hmm. You can add class methods to `Cat.objects` by creating a subclass
of `Manager`. But this won't add corresponding methods to the `QuerySet`
class.

I think the way to do this is

1. Create a `QuerySet` with your custom filtering methods.
2. Call `QuerySet::as_manager` to dynamically create the `Manager` class
   that corresponds.
3. The manager is like the `QuerySet`, except I think it just strips out
   some 'dangerous' methods that should only exist on the `QuerySet`.

Example:

```python
class ToysQuerySet(models.QuerySet):
  def get_mousey(self):
    return self.filter(name='mousey')

class Toy(models.Model):
  objects = ToysQuerySet.as_manager()
  # ...


Toy.objects.get_mousey()
cat = Cat.objects.first()
cat.toys.get_mousey()
```

I believe it has already been mentioned that some methods shouldn't be
copied to the manager. For instance: the `delete` method. This is not
(by default) copied because it would make it too easy to drop the whole
table.

You can configure `as_manager` to copy some methods but not others.

They talk about how custom managers are inherited when models are
inherited. Sounds fancy, and like I don't want to play with that right
now.

### Multi DB

They show a fairly bullshit system to handle multiple DBs. I think the
primary use case they want to support is primary/replica. You can
basically call a `using(db=name)` method on `QuerySet`, and pass a
`using=db_name` argument to model instance methods like `#save`.

The functionality here is primitive, but hopefully supports 90% of users
in what they might need for basic replication.

### Tablespaces

A tablespace is basically a name to give to a storage device. Databases
allow the DBA to specify what tables should be stored on what devices.
The device's 'name' is the tablespace.

The DBA has to setup the table space for you, but in Django, you can
specify that a certain index or table should live in a certain
tablespace. This is set in the model's `Meta#db_tablespace` property.
Certain fields that create indices or tables (e.g., `ForeignKeyField`,
`ManyToManyField`) will take a `db_tablespace` named argument.

## Execute Wrapper

`connection.execute_wrapper` basically installs a wrapper around every
query to the DB. It works middleware-style: you can do something, call
the quey, and then do something else. Here's a simple example:

```python
from django.db import connection
from django.shortcuts import render

def blocker(*args):
    raise Exception('No database access allowed here.')

def my_view(request):
    context = {...}  # Code to generate context with all data.
    template_name = ...
    with connection.execute_wrapper(blocker):
        return render(request, template_name, context)
```

I think they're thinking that you might write a logger, or time how long
queries take, or whatever.

## Raw SQL

They talk about the `raw` API. You can write:

```ipython
In [12]: list(Cat.objects.raw('SELECT * FROM cats_cat'))
SELECT *
  FROM cats_cat

Execution time: 0.000117s [Database: default]
Out[12]: [<Cat: Markov>]
```

Any fields that aren't fetched by the query, will be deferred. Any extra
properties will be treated as annotations.

You can interpolate query parameters:

```ipython
In [18]: cat = Cat.objects.raw('SELECT id FROM cats_cat WHERE name = %s LIMIT 1'
    ...: , ['Markov'])[0]
SELECT id
  FROM cats_cat
 WHERE name = 'Markov'
 LIMIT 1
```

You can also say `%(name)s` and pass a dictionary `{ 'name': 'Markov'
}` instead of the list. However, it doesn't work this Sqlite3.

You can also execute your own SQL directly:

```ipython
In [22]: with connection.cursor() as cursor:
    ...:     cursor.execute("SELECT * FROM cats_cat")
    ...:     rows = cursor.fetchall()
    ...:     print(rows)
    ...:
SELECT *
  FROM cats_cat

Execution time: 0.000123s [Database: default]
[(1, 'Markov', 13)]
```

## Optimization

They mention that `cat.toys.all()` will not cache. Therefore, in a
template, you may want to use the `with` template tag which lets you
make a local variable and thus cache a result.

If there are a lot of objects to fetch, you may prefer to use the
`QuerySet#iterator` method. This avoids the cache and just reads the
items one-at-a-time cursor-style.

They suggest using `selected_related` and `prefetch_related` to avoid
N+1 queries.

They recommend bulk operations.
