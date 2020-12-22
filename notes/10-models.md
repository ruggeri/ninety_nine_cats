## Further Model Notes

Here I will try to work through the topics pages on models and
databases.

### Common Model Attribute Options

**Blank and null**

You can set `blank=True`. The default is `False`. `True` allows a field
to be `None` or `""`. A blank field will not trigger a validation
failure.

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
