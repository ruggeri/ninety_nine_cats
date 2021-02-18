# `InlineModelAdmin`

It is typical to want to update related objects from an admin detail
view. This is commonly the case on the "reverse" side of a
`ForeignKeyField`. It also happens when you have a non-trivial
`ManyToManyField`.

Django admin allows this with *inlines*:

```python
class ToyInline(admin.StackedInline):
  # Notice that you must set model because this won't be known from
  # `admin.site.register`.
  model = models.Toy

class CatAdmin(admin.ModelAdmin):
  # Allow them to create/update toys directly from a Cat object.
  inlines = [ToyInline]
```

The `StackedInline` class separates each inlined `Toy` object a bit. The
`TabularInline` looks more like a table with rows. They are functionally
identical and only the template is different. All options are in common
to both.

## Shared Features From `ModelAdmin`

Here are some of the shared features:

* `form`: specifies a `ModelForm`
* `fields`, `fieldsets`, `exclude`, `readonly_fields`
* `ordering`
* `radio_fields`, `raw_id_fields`
  * I believe `autocomplete_fields` is also available, at least for
    `StackedInline`.

## New Options

* `extra = 3` is the default number of "extra" blank items to offer. You
  can set `extra = 0` and they can always dynamically add more by
  clicking an "add" link.
* `can_delete`: should you be shown a checkbox to select items for
  deletion?
* `show_change_link = True`: defaults to False. This will add a link
  to the admin's change page for the related object.
  * This can make sense if the inline only presents a few fields that
    you might want to edit from here.

## Permissions

These correspond to permissions for the `ModelAdmin` object. But I list
them here because Anastassia and I used these to reduce the number of
input tags on an inline where we just wanted to *show* inline data.

* `has_add_permission(request, parent_object)`: this determines whether
  they should be allowed to add new items.
* `has_change_permission(request, parent_object)`: this determines
  whether they should be allowed to change existing items.
* `has_delete_permission(request, parent_object)`: this determines
  whether they should be allowed to delete existing items.
  * Maybe `can_delete` is about offering delete functionality to anyone,
    while `has_delete_permission` is checking the user's permissions?
