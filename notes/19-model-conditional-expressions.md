# Conditional Expressions

This basically describes how to write a CASE WHEN in Django. It's a
little crazy:

```python
from django.db.models import When, Value

# This is how you specify a condition: WHEN name = 'Markov' THEN 1.
When(name='Markov', then=1)

# Annotate a my_example attribute.
cats = Cat.objects.annotate(
  my_example=Case(
    # If name is Markov, then return 1
    When(name='Markov', then=1),
    # any other conditions can also be listed
    # ...
    # choose an ELSE value
    default=0,
    # specify the kind of field returned? Presumably how to parse.
    output_field=IntegerField(),
  )
)
```

I believe we've already seen how to do a form of conditional
aggregation:

```python
Cat.objects.aggregate(
  num_cats=Count('id', filter=Q(name='Markov'))
)

# SELECT COUNT("cats_cat"."id") FILTER (WHERE "cats_cat"."name" = 'Markov') AS "num_cats"
#   FROM "cats_cat"
```
