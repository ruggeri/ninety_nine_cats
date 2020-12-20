## Many-To-One ForeignKey Associated Object

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
