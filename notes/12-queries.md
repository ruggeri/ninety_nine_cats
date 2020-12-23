# Queries

## Creation

You can use `#save`. There is also `::create`.

When you call save, the following steps happen:

* `pre_save` signal is sent, listeners run,
* Each field's `pre_save` method is called. This lets `auto_now_add`,
  `auto_now` work.
* Each field's `get_db_prep_save` method is called. This converts the
  field's value into a DB writeable value. Most fields won't need this.
* Data is inserted.
* `post_save` signal is fired.

Django knows to do an INSERT instead of an UPDATE based on whether the
`pk` is present. But, BTW, if the UPDATE doesn't hit any record (because
the `pk` doesn't exist in the DB), then an INSERT is subsequently
performed. This allows the user to specify a `pk` value rather than rely
on it to be auto-generated.

**Race Conditions**

Sometimes there are potential race conditions. As in:

```python
post = Post.objects.get(id=post_id)
post.likes += 1
post.save()
```

You could either use a transaction, or you could use a **F expression**.
As in:

```python
post.likes = F('likes') + 1
```

You might also want to

```python
post.save(update_fields=['likes'])
```

This will prevent you from clobbering other fields that might be
changing concurrently.

**Associating Objects**

When you write

```python
toy.cat = markov
toy.save()
```

This works in the expected way. The `toy` object is saved and the
`cat_id` field is updated.

On the other hand, consider:

```python
markov.toys.add(mousey)
```

This immediately updates the associated record `mousey`. I believe it
requires that both `markov` and `mousey` have been previously saved (so
that `mousey` exists to update, and `markov` has a pk to use in the
`mousey.cat_id`).

## Retrieval

You start with a `Manager`. This is `Cat.objects`. I'll learn more about
`Manager`s later, I think. `Cat.objects.all()` returns a `QuerySet` that
selects everyone.

`filter` is the common way of filtering only those results you want
(WHERE style). You can call it directly on the `Manager`
`Cat.objects.filter` or you can call it on a `QuerySet`
`Cat.objects.all().filter`.

`QuerySet`s are a 'builder' interface. You build up a query, but the
sub-steps don't fire any queries, and future chaining just builds
further (does not mutate prior intermediate `QuerySet`s).

`QuerySet`s are evaluated lazily.

You can use `get` if you expect exactly one value to be returned. Common
is `get(id=123)`. If `get` returns zero or >1 objects, exceptions will
be thrown.

**Limit and Offset**

If you slice, this triggers a LIMIT/OFFSET:

```python
Cat.objects[:10] # LIMIT 10
Cat.objects[10:] # OFFSET 10
```

**Filtering By Value**

We can use simple equality constraints with `filter`. But you can also
have fancier queries:

```python
Cat.objects.filter(name__startswith="M")
```

Other matchers are:

* `iexact`
* `contains`, `icontains`
* `startswith`/`istartswith`, `endswith`/`iendswith`,
* `in`

**Filtering Spanning Relations**

We know that you can say stuff like
`Cat.objects.filter(toy__name="mousey")`.

They address a complicated situation:

* Find all Cats that have one toy that starts with 'm' and ends in 'y'.
* Find all Cats that have one toy that starts with 'm', and one (maybe
  different) toy that ends in 'y'.

You do it like this:

```python
# Find a Cat which has a toy meeting both requirements. Does a single
# JOIN with two WHERE conditions.
Cat.objects.filter(toys__name__startswith='m', toys__name__endswith='y')
# Find a Cat with a toy for the first requirement, and a toy for the
# second requirement. Does two JOINs.
Cat.objects
  .filter(toys__name__startswith='m')
  .filter(toys__name__endswith='y')
```

**Querying With F Expressions**

Let's say you want to find a Cat with a toy named the same as the cat:

```ipython
# Hmm. But how does F('name') know that it should refer to
# cats_cat.name?
In [11]: Cat.objects.filter(toys__name=F('name'))
Out[11]: SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 INNER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
 WHERE "cats_toy"."name" = "cats_cat"."name"
 LIMIT 21
```

## Caching

`QuerySet` results are cached. That is: when you need the result, the
query is executed and the result is cached. If you use the same
`QuerySet` twice, you'll get the same result.

There is a caveat. If you only want `query_set[5]`, and the set hasn't
been evaluated yet, it will request just the one item, and trigger a
query each time.

BTW, they explicitly note that printing a query set doesn't exactly load
it. The reason is that the `QuerySet#__str__` method only selects the
first few items to print.

## JSONField Querying

There are an inordinate and baroque set of ways to query `JSONField`s. I
won't go into them here: they're mostly intuitive, and I don't use
`JSONField` that much. I could review later if interested.

## Q Operator

The `django.models.Q` operator lets you build conditions for a `filter`:

```python
query = Q(toys__name='mousey') | Q(name='Markov')
cats = list(Cat.objects.filter(query))
```

You can also use `&` to AND criteria, and you can also use `~` to negate
a query.

As far as I can see, the primary use of `Q` objects would be for OR
queries.

## Deletion

They note that you can call `#delete` on either a model instance or a
`QuerySet`. They note that when called on a `QuerySet`, the `delete`
method isn't called on each individual item. But I don't think you
should be overriding a model's `delete` method anyway...

## Bulk Update

A `QuerySet` has a `update` method that will update every element in the
query set. They explain that you can only update the fields that are
directly on a model, not any fields in associated columns. That sounds
reasonable.

Of course, the save method won't be called.

This is a good use case for `F` expressions.

## Relations

They rehash some information about relations. They talk about
`select_related`, which is like the ActiveRecord `include` option. This
prefetches related objects. You can say
`Cat.objects.selected_related('toys')` to get the related `Toy`s.

You can use `add`, `create`, `remove` (for many-to-many or `ForeignKey`
if `null=True`), `clear` (ditto), `set` on a reverse relation manager
like `Cat#toys`.

## Other QuerySet Methods

**anotate**

Allows you to add additional fields to pull down. The most common case
for this is aggregations. For instance:
`Blog.objects.anotate(number_of_entries=Count('entry'))` will get `Blog`
items and an entry count.

**order_by**

This is pretty clear. One thing they mention is that
`Cat.objects.order_by('toys__name')` can return the same cat *multiple
times*.

```ipython
In [6]: Cat.objects.order_by('toys__name').all()
Out[6]: SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
  LEFT OUTER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
 ORDER BY "cats_toy"."name" ASC
 LIMIT 21

Execution time: 0.000168s [Database: default]
<QuerySet [<Cat: Markov>, <Cat: Markov>]>
```

**distinct**

Notice that this problem with duplicate objects applies to any time a
join might be performed:

```ipython
In [12]: Cat.objects.filter(toys__name__startswith="")
Out[12]: SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 INNER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
 WHERE "cats_toy"."name" LIKE '%' ESCAPE '\'
 LIMIT 21

Execution time: 0.000181s [Database: default]
<QuerySet [<Cat: Markov>, <Cat: Markov>]>
```

But you can fix this by calling `distinct()`:

```ipython
In [21]: Cat.objects.filter(toys__name__startswith="").distinct()
Out[21]: SELECT DISTINCT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 INNER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
 WHERE "cats_toy"."name" LIKE '%' ESCAPE '\'
 LIMIT 21

Execution time: 0.000213s [Database: default]
<QuerySet [<Cat: Markov>]>
```

Watch out for a footgun when using distinct with order_by:

```ipython
In [22]: Cat.objects.order_by('toys__name').distinct()
Out[22]: SELECT DISTINCT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age",
       "cats_toy"."name"
  FROM "cats_cat"
  LEFT OUTER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
 ORDER BY "cats_toy"."name" ASC
 LIMIT 21

Execution time: 0.000146s [Database: default]
<QuerySet [<Cat: Markov>, <Cat: Markov>]>
```

I think the reason for the problem here is that a DISTINCT is
effectively a GROUP BY. And GROUP BY gets done before ORDER BY.

**values**

This lets you select just those fields you desire:

```ipython
In [24]: Cat.objects.values('id', 'name')
Out[24]: SELECT "cats_cat"."id",
       "cats_cat"."name"
  FROM "cats_cat"
 LIMIT 21

Execution time: 0.000198s [Database: default]
<QuerySet [{'id': 1, 'name': 'Markov'}]>
```

You get the expected explosion when you JOIN other tables:

```ipython
In [25]: Cat.objects.values('id', 'name', 'toys')
Out[25]: SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_toy"."id"
  FROM "cats_cat"
  LEFT OUTER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
 LIMIT 21

Execution time: 0.000158s [Database: default]
<QuerySet [{'id': 1, 'name': 'Markov', 'toys': 1}, {'id': 1, 'name': 'Markov', 'toys': 2}]>
```

**select_related/prefetch_related**

We've already covered `select_related`: you give it relations and it
will do a JOIN and SELECT out both sets of fields. To avoid explosion,
it only works with `ForeignKeyField`s and `OneToOneField`s.

When you want to go backward through a `ForeignKeyField`, or have a
`ManyToManyField`, you should use `prefetch_related`. This one does two
separate queries, and does the stitching together in Python. This way
the JOIN doesn't explode things.

```ipython
In [28]: list(Cat.objects.prefetch_related('toys'))
SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"

Execution time: 0.000198s [Database: default]
SELECT "cats_toy"."id",
       "cats_toy"."cat_id",
       "cats_toy"."name"
  FROM "cats_toy"
 WHERE "cats_toy"."cat_id" IN (1)

Execution time: 0.000086s [Database: default]
Out[28]: [<Cat: Markov>]
```

**defer/only**

Another baroque optimization. You can `defer(field_name)`, and this
won't be selected. *But* you'll still have an attribute for that field
that will lazily load it. Maybe useful if you're selecting a large
number of objects with big text fields, and you just don't want that
field.

`only(field_name)` is the opposite of `defer`. It says to only eagerly
load the specified field name.

`only` is a little like `values`, but with the ability to fetch further
data as needed.

**select_for_update**

Basically immediately locks the rows on a MVCC DB.

**get_or_create**

A convenience to get the object with certain properties, or create it.
But it isn't actually concurrency safe. Multiple objects can get
created.

**update_or_create**

Ditto.

**bulk_create/bulk_update**

Both methods will not call `#save`, and will not fire signals.

**iterator**

Gives an iterator over the `QuerySet`. But as the `QuerySet` is
evaluated, the results are not cached. So this is a performance
enhancement.

They do note that it also matters whether the DB driver can support a
cursor. The PostgreSQL driver, for instance, will give a cursor that can
minimize memory from fetching. But I think the MySQL DB does not, and
thus all results are fetched in one go (but presumably not turned into
Python objects right away).

**exists**

Does what you think.

**update**

Using this can do a bulk update on all the objects matching a query. But
it can also avoid a race-condition, as opposed to (1) load, (2) change
field, (3) save. Sensibly, you can only call `update` on fields stored
in the object under consideration (rather than related objects).

Of course, does not call save, nor emit signals.

## Field Matchers

**in**

Interesting, but you can pass a `QuerySet` that would produce a list of
results. This will produce a nested query. This may or may not be well
optimized for your DB engine.

**regex**

You can match on REGEXP.

## TODO

I've read up through https://docs.djangoproject.com/en/3.1/ref/models/querysets/#aggregation-functions
