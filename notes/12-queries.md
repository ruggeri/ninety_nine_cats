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

## TODO

* I've read up to here: https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects
