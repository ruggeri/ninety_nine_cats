## Further Model Notes

Here I will try to work through the topics pages on models and
databases.

### Common Model Attribute Options

**Blank and null**

You can set `blank=True`. The default is `False`. `True` allows a field
to be `None` or `""`. A blank field will not trigger a validation
failure when `full_clean` is called.

However, fields are by default `NOT NULL`. To allow `NULL` values, you
must set `null=True`. `null=True` is thus about the DB serialization,
whereas `blank=True` is about validation.

Thus:

* `blank=False, null=False`: both `""` and `None` are rejected.
* `blank=True, null=False`: `""` is allowed, but `None` is rejected.
  Only make sense on `CharField` and `TextField`?
* `blank=True, null=True`: you can use `None`. Makes sense for optional
  `IntegerField`. Usually shouldn't allow two empty values for a
  `CharField` or `TextField`. But could make sense if a `CharField` has
  a unique constraint.
* `blank=False, null=True`: doesn't make any sense?
  * Crazy, but `full_clean` is not called on save?? So save doesn't
    check a validation. Thus empty (but non-NULL) strings are easily
    saved to the DB.

**Choices**

You can set `choices`. This is a list of tuples. The tuples are
`(stored_value, checkbox_display_value)` pairs. This customizes how
forms are displayed. It's kind of like an enum, but it doesn't make an
enum at the DB level. Here's an example:

```python
class Cat(models.Model):
  CAT_SIZES = (
      ('S', 'Small'),
      ('M', 'Medium'),
      ('L', 'Large'),
  )

  size = models.CharField(max_length=1, choices=CAT_SIZES)

# The size property is still a single character. But you can call
# `cat.get_size_display()`. The real point of choices is for forms (I
# think).
```

**Other Common Attributes**

* You can use `primary_key=True` to tell Django to use this field as the
  primary key. Otherwise it will make its own pk field called `id`.
* The `default` option can be either a value, or a callable.
* `unique=True` will enforce uniqueness of this field.
* `help_text` will control what help text appears in a form widget.

### Many-To-One Relationships

You create a field called `ForeignKey`. Here is a basic example:

```python
class Toy(models.Model):
  # Adds both a cat_id field and an attribute cat that will fetch the
  # associated object.
  cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
```

You can use just the string `'Cat'`, which would allow you to define
model classes in any order. It is even possible to define recursive
relationships with `'self'`. If you want to refer to a model from
another app, you must say `other_app_name.ModelClassName`.

You must specify `on_delete`. You can set either `CASCADE` (when the
parent is deleted, all children are), `PROTECT` (the parent cannot be
deleted if there are still children), `RESTRICT` (some weird variant of
`PROTECT`), `SET_NULL` (sets the foreign key to NULL), or `SET_DEFAULT`
(sets the foreign key to the default value). Can even specify
`SET(callable)`, which will run a function to set the new value.

`limit_choices_to` controls the options that are presented for a form.
You could specify `limit_choices_to={ 'is_staff': True }` to only let
someone pick a `User` who is a staff member. Note: I don't think this
does any kind of validation.

By default, `related_name` is `XXX_set`. So `Cat#toy_set` is the related
name. You can override this to be `related_name='toys'` which means
`Cat#toys` is now the relationship back.

`related_name`, if set, will also set `related_query_name`. By default,
we say: `Cat.objects.filter(toy__name="mousey")` to select those cats
who have a toy named 'Mousey'. But you can override `related_query_name`
if desired. For instance, if you changed `related_name="toys"`, then you
might want to set `related_query_name="toy"`.

You can also specify the key in the parent. This defaults to the primary
key of the parent. But you can override with `to_field='email_address'`
or whatever. But you better have a `unique=True` constraint on that
field!

Oh yeah, `db_column` can be set to control the foreign key field name.
In the `Toy` example, this is `cat_id`. You can say `Toy#cat_id`, and
get/set this explicitly.

Also: a DB index will be generated for you.

Note: as far as I can tell, when you first call `Toy#cat`, it will
trigger the query. But any subsequent calls to `#cat` will use the
cached value.

## ManyToManyField

You set this to do a many-to-many relationship with a join table
auto-generated. I added one like this:

```python
class Human(models.Model):
  cats = models.ManyToManyField(Cat)
```

**SQL and Indices**

Check this dope SQL:

```sql
CREATE TABLE IF NOT EXISTS "cats_human_cats"(
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "human_id" integer NOT NULL REFERENCES "cats_human"("id") DEFERRABLE INITIALLY DEFERRED,
  "cat_id" integer NOT NULL REFERENCES "cats_cat"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX "cats_human_cats_human_id_cat_id_cfdb6b42_uniq" ON "cats_human_cats"(
  "human_id",
  "cat_id"
);
CREATE INDEX "cats_human_cats_human_id_c3a26c3d" ON "cats_human_cats"(
  "human_id"
);
CREATE INDEX "cats_human_cats_cat_id_873952ed" ON "cats_human_cats"("cat_id");
```

So we get some good indices. We don't exactly need `id`, but that's
fine.

**Association Methods**

By defining the `ManyToManyField`, we can write `cat.human_set.all()`
and `human.cats.all()`. This is unpleasantly asymmetric, but perhaps
similar to the situation with `ForeignKey`.

But that's BS. Notice this asymmetry:

```python
# Nice
Cat.objects.filter(human__name="Ned")
# Meh
cat.human_set
# Gross
Human.objects.filter(cats__name="Markov")
# Nice
human.cats
```

I'm not actually what the best way to deal with this asymmetry. I think
maybe one should by default always set `related_name='humans'` for both
`ForeignKeyField` and `ManyToManyField`. This would mean that you always
symmetrically refer to the associated many objects with a plural, both
for the association method `cat.humans` and for the query
`cat.filter(humans__name="Ned")`.

To be clear: it doesn't otherwise matter what side of the relationship
you put the `ManyToManyField`.

**Custom Through Tables**

Sometimes a join table should have extra fields. Let's consider if
`Human` and `Cat` are related by `CatHumanRelationship`. Let's define:

```python
class Human(models.Model):
  name = models.CharField(max_length=255)

class CatHumanRelationship(models.Model):
  cat = models.ForeignKey(
      Cat, on_delete=models.CASCADE, related_name="relationships"
  )
  human = models.ForeignKey(
      Human, on_delete=models.CASCADE, related_name="relationships"
  )
  # Number of years of duration of relationship
  duration = models.IntegerField(default=0)
```

You can now specify the many-to-many relationship between Human and Cat
this way:

```python
class Human(models.Model):
  name = models.CharField(max_length=255)
  related_cats = models.ManyToManyField(
      'Cat',
      through='CatHumanRelationship',
      related_name='related_humans'
  )
```

### OneToOneField

Conceptually this is the same as `ForeignKeyField` with `unique=True`.
But it's a little more convenient because the reverse relationship will
return `None`/the child instance, rather than a query set.

They point out that this is most useful when doing some kind of
multi-table inheritance thingy.

## Other

**Metadata**

You can set metadata with an internal class called `Meta`. For instance:

```python
class Cat:
  class Meta:
    # default ordering
    ordering = ['age']
    db_table = "the_cool_cats_table"
```

You can also add `constraints` (including multi-column constraints), and
`indices`.

**Overriding `#save`, `#delete`, et cetera**

You can do a sort of triggery thing when save or delete is called. You
accomplish this by overriding the functions. Now you can add pre and
post hooks.

As you may expect, these functions are not called when you do bulk
creation/deletion. Even trying to tie in with the signals functionality
won't always work.

Honestly, it seems like a bad idea.

### Abstract Base Class Models

An abstract model type adds functionality, but doesn't actually
instantiate a table. Here's a good use case (some cribbing from
django-model-utils 3rd party library):

```python
from django.utils.timezone import now
class TimeStampedModel(models.Model):
  created = models.DateTimeField(editable=False, default=now)
  # ...

  class Meta:
    abstract = True
```

One probably doesn't write that many abstract model classes. But it is
probably helpful to know about.

## Multi-table Inheritance

This is a pattern where you have a `Place`s table, and also a
`Restaurant`s table, where a `Restaurant` *is a* `Place`. So you make
`Restaurant` a subclass of `Place`, and Django will create the
`OneToOneField` from `Restaurant` to `Place` for you.

When you have a `Restaurant`, it has all the fields of a `Place`. If
`name` is a property of `Place`, you can write
`Restaurant.objects.filter(name="Chez Markov")`. On the other hand, you
can *downcast* from `Place` to `Restaurant` by writing
`myPlace.restaurant`. This gives an error if `myPlace` is not, in fact,
a `Restaurant`.

Wow. You can even do *multiple* inheritance! To do it, the parents have
to explicitly define primary keys. Here's an example:

```python
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    ...

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    ...

class BookReview(Book, Article):
    pass
```

## Proxy Models

A weird feature. Kind of like ActiveRecord scopes. An example:

```python
class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True
```

Now, if you say `OrderedPerson.objects.all()`, it will be ordered for
you, whereas `Person` will not be.

Not that exciting.

### TODO

* https://docs.djangoproject.com/en/3.1/topics/db/queries/
* https://docs.djangoproject.com/en/3.1/topics/db/aggregation/
* https://docs.djangoproject.com/en/3.1/topics/db/search/
* https://docs.djangoproject.com/en/3.1/topics/db/managers/
* https://docs.djangoproject.com/en/3.1/topics/db/sql/
* https://docs.djangoproject.com/en/3.1/topics/db/transactions/
* https://docs.djangoproject.com/en/3.1/topics/db/multi-db/
* https://docs.djangoproject.com/en/3.1/topics/db/tablespaces/
* https://docs.djangoproject.com/en/3.1/topics/db/optimization/
* https://docs.djangoproject.com/en/3.1/topics/db/instrumentation/
* https://docs.djangoproject.com/en/3.1/topics/db/examples/

* https://docs.djangoproject.com/en/3.1/ref/models/fields/
* https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-attribute-reference
* https://docs.djangoproject.com/en/3.1/ref/models/indexes/
* https://docs.djangoproject.com/en/3.1/ref/models/constraints/
* https://docs.djangoproject.com/en/3.1/ref/models/meta/
* https://docs.djangoproject.com/en/3.1/ref/models/relations/
* https://docs.djangoproject.com/en/3.1/ref/models/class/
* https://docs.djangoproject.com/en/3.1/ref/models/options/
* https://docs.djangoproject.com/en/3.1/ref/models/instances/
* https://docs.djangoproject.com/en/3.1/ref/models/querysets/
* https://docs.djangoproject.com/en/3.1/ref/models/lookups/
* https://docs.djangoproject.com/en/3.1/ref/models/expressions/
* https://docs.djangoproject.com/en/3.1/ref/models/conditional-expressions/
* https://docs.djangoproject.com/en/3.1/ref/models/database-functions/
