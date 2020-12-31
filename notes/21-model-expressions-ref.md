# Expressions

* I believe we've already discussed
  `Cat.objects.filter(name=Lower('name'))`.
* You can do similar with `F` expressions:
  `Cat.objects.filter(name=F('id'))`.
* Sometimes you must use `Value`. As in `Lower(Value('STRING TO
  LOWER'))`. Of course, why didn't you just lower that yourself in
  Python?

You can also do this:

```python
Cat.objects.filter(
  Exists(Toy.objects.filter(cat=OuterRef('id'), name='mousey'))
)
```

Notice the use of `OuterRef`, which is not immediately bound. It's like
`F` for an outer table.

It's unnecessarily complicated, but you can see that it will get those
`Cat`s who have a related `Toy` named `'mousey'`. A subquery will be
issued. Which is nicer than a JOIN being issued per
`Cat.objects.filter(toy__name='mousey')`, actually. This does have the
advantage of avoiding a needed call to `DISTINCT`.

**F Queries**

We've already discussed how `F` queries can be used to avoid race
conditions, and to do batch updates. We've also talked about their use
in filter queries with a field's name.

**Func Expressions**

* These take in a field, and perform some function. For instance,
  `Lower`, `Upper`.

**Aggregate Expressions**

* These inform Django that a GROUP BY must be performed. The group by
  will be based on the associated name.
* This is your `Sum`, `Count`, `Avg`.

**Subquery Expressions**

* As described above, you can ask Django to do a subquery for you.
* I think this would be most common with `EXISTS`.
* But you can also imagine doing a subquery for an IN:

```python
In [99]: Cat.objects.filter(name__in=Toy.objects.values('name'))
Out[99]: SELECT "cats_cat"."id",
       "cats_cat"."name",
       "cats_cat"."age"
  FROM "cats_cat"
 WHERE "cats_cat"."name" IN (
        SELECT U0."name"
          FROM "cats_toy" U0
       )
```

```python
# Wrong!
Cat.objects.annotate(Count('toys'), Count('related_humans')).values('id', 'toys__count', 'related_humans__count')
Out[131]: SELECT "cats_cat"."id",
       COUNT("cats_toy"."id") AS "toys__count",
       COUNT("cats_cathumanrelationship"."human_id") AS "related_humans__count"
  FROM "cats_cat"
  LEFT OUTER JOIN "cats_toy"
    ON ("cats_cat"."id" = "cats_toy"."cat_id")
  LEFT OUTER JOIN "cats_cathumanrelationship"
    ON ("cats_cat"."id" = "cats_cathumanrelationship"."cat_id")
 GROUP BY "cats_cat"."id",
          "cats_cat"."name",
          "cats_cat"."age"


toys_count = Count(Toy.objects.filter(cat_id=OuterRef('id')).values('id'))
humans_count = Count(CatHumanRelationship.objects.filter(cat_id=OuterRef('id')).values('id'))
cats = Cat.objects.annotate(toys_count=toys_count, humans_count=humans_count)
list(cats)
# SELECT "cats_cat"."id",
#        "cats_cat"."name",
#        "cats_cat"."age",
#        COUNT((SELECT U0."id" FROM "cats_toy" U0 WHERE U0."cat_id" = "cats_cat"."id")) AS "toys_count",
#        COUNT((SELECT U0."id" FROM "cats_cathumanrelationship" U0 WHERE U0."cat_id" = "cats_cat"."id")) AS "humans_count"
#   FROM "cats_cat"
#  GROUP BY "cats_cat"."id",
#           "cats_cat"."name",
#           "cats_cat"."age"
```

**RawSQL**

* I think this is prolly the best way to do certain fancy queries? Like
  my example of comparing the MD5 of two fields without doing an
  annotation?
