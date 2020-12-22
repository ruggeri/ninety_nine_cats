# Model Fields Reference

## Common Field Options

**Choices**

They talk a bunch about how to make an enum that lists choices. There
are some helpers to create the list of tuples format:

```python
MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
MedalType.choices
# [('GOLD', 'Gold'), ('SILVER', 'Silver'), ('BRONZE', 'Bronze')]
Place = models.IntegerChoices('Place', 'FIRST SECOND THIRD')
Place.choices
# [(1, 'First'), (2, 'Second'), (3, 'Third')]
```

**editable**

A non-editable field won't be displayed in forms. It is skipped during
model validation.

**validators**

Here you can list validators to run. But I haven't learned anything
about those yet!

## Various Field Types

* `AutoField` used for primary keys
* `BooleanField`
* `CharField`
* `DateField`, `DateTimeField`
  * Has an `auto_now` option. This is useful for `updated_at`.
  * `auto_now_add` option. Useful for `created_at`.
  * BTW, `updated_at` and `created_at` set `blank=True`, which makes
    sense. The form shouldn't try to set these fields (which are not
    editable).
* `EmailField` - runs an email validation.
* `FileField`
  * **TODO**: this is a fancy one. You set where the files should be
    stored. Some kind of service takes care of this for you.
  * All that will be stored in the DB is a path to the actual file.
  * When you say `cat.photo`, you get a `FieldFile` instance that
    proxies to the file. It has `url`, `size`. It also has an `open`
    method, and once opened you can `read`.
  * You can `save`
* `FloatField`
* `GenericIPAddressField`
* `ImageField` is a subclass of `FileField`
* `IntegerField`
* `JSONField` does storage of JSON into the DB.
* `TextField`
* `TimeField`
* `URLField` an instance of `CharField`, validated with `URLValidator`.
* `UUIDField` is an alternative to `AutoField`. But you should use
  `default` to specify a function that generates a unique value.

## Custom Fields

There was some brief discussion that started to hint at how you could
define your own custom fields. But I am ignoring this for now!
