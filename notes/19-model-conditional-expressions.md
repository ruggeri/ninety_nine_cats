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

## TODO

https://docs.djangoproject.com/en/3.1/ref/models/conditional-expressions/#advanced-queries
