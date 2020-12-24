# Model Methods

The only class field is `objects`?

## Fetching/Creating Objects

The `__init__` method is pretty dangerous to override. They basically
recommend defining a class method if you want to do some kind of custom
construction.

You can override the class method `Model::from_db`, which deserializes
DB fields/values into an instance. Seems like nothing to fuck with.

## Refreshing Objects

`refresh_from_db` will fetch fields from the DB. It will bust cached
relations. Delayed fields are not fetched. In fact, delayed fields will
fetch themselves via
`refresh_from_db(fields=['the_name_of_the_delayed_field'])`.

`get_delayed_fields` fetches all delayed fields.

## Validation

**`clean_fields`**

I can see that this iterates through fields. If `blank=True`, and the
value is in the field's `empty_values` set, then validation is skipped.

Else, `field.clean(raw_value, model)` is called. This is also a hook
opportunity to transform the value pre-save. The cleaned value is
assigned as the new field value to the model.

If an exception is thrown, the validation error is saved to the
`ValidationError#errors` map.

**`clean`**

This is where you can do model-specific work on fields. For instance,
you can do model specific pre-save cleaning of fields. And you can do
model-specific validation of those fields.

This is especially necessary for any validations that make reference to
multiple fields. This example from the ref is pretty good:

```python
class Article(models.Model):
    def clean(self):
        # Validation across fields.
        if self.status == 'draft' and self.pub_date is not None:
            raise ValidationError(_('Draft entries may not have a publication date.'))
        # Cleaning.
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()
```

**`validate_unique`**

This checks the uniqueness constraint on any fields which have them.

**`full_clean`**

Calls `clean_fields`, `clean`, and `validate_unique`. `full_clean` is
not called before the `save` method; when saving no validation is done!

## Saving

It describes that after `save`, `id` will get populated. But you can set
`id` explicitly if you want. In that case, you probably want to say
either `force_insert=True` or `force_update=True`.

Steps of saving are:

1. Send `pre_save` signal for object.
2. Call each field's `pre_save` method for automated transformation.
3. Serialize the fields by calling their `get_db_prep_save` method. This
   is the data that will be written to the DB.
4. Write it to the DB.
5. Emit a `post_save` signal for the object.

Elsewhere I've mentioned `F` expressions for updating fields (like
bumping a like count). I believe I've also mentioned that
`save(update_fields=['name'])` which will only update that one field.

## Other Methods

`__str__` is useful to define so you can the name of the object.
Otherwise just the id is shown.

`__eq__` will just compare (1) same model, (2) same primary key. If
primary key is `None`, then it will never compare equal. Note that no
fields are compared other than `id`.

`get_absolute_url` is a method that constructs a URL representing the
model object. You don't have to write it. But it is handy if you do have
a detail page for the object. If you set this, the admin panel with have
a "Show on Site" button for your object. Also it's useful to use this to
build URLs in your templates (rather than by hand, which is a bad idea).

There are also methods generated for you:

* `get_XXX_display()`: gives the display name for a choice field.
* `get_next_by_created_at`: or `updated_at`, or whatever. Such a method
  exists for every `DateTimeField`, `DateField`. It helps you find the
  chronologically prev/next.

https://docs.djangoproject.com/en/3.1/ref/models/instances/#validating-objects

