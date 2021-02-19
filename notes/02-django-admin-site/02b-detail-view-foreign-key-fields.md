# Detail View Foreign Key Field Types

## ForeignKey fields (belongs to)

When you have a `ForeignKey` (belongs to), or a `choices` field, this is
by default rendered as a `<select>` tag. If you want to use radio
buttons, you can set this on the `ModelAdmin`. For example:

```python
class ToyAdmin(admin.ModelAdmin):
  # Related `cat` object should be selected by radio button. They should
  # be rendered horizontally. VERTICAL is the other option.
  radio_fields = {'cat': admin.HORIZONTAL}
```

Even more fancy is `autocomplete_fields = ['cat']`. What does this do?
It uses `select2` to let you query a related cat. You type in the name
of a cat, and it presents you with a selectable list of cats.

It requires that `search_fields` is defined on the related `ModelAdmin`
for cats. For instance `search_fields = ['name']`. But I'll explain how
that works in my description of list views.

Last, and most simply, you can set `raw_id_fields = ['cat']`. This lets
you directly write in a Cat id.

## ManyToMany Fields

By default, trivial `ManyToManyField`s are represented with a `<select
multiple>` tag. This can be difficult to work with.

Thus, you can set `ModelAdmin::filter_horizontal` or
`ModelAdmin::filter_vertical` to present *two* lists: one of unselected
options, and a second of selected options. You can use a couple buttons
to move elements from one to the other. This is just some nicer UI on
top of, ultimately, a hidden `<select multiple>`.

If you set `raw_id_fields` to include a `ManyToManyField`, you can also
write a comma separated value of ids.

Note one weird thing: the `ManyToManyField` can only be administered in
the *forward* direction. That's annoying, especially if the `ManyToMany`
is trivial. You'll have to use inlines.

## Further Customization

There are methods to control the form fields for `ForeignKeyField`,
`ManyToManyField`, and `ChoiceField`. They are:

* `formfield_for_foreignkey(db_field, request, **kwargs)`
* `formfield_for_manytomany(db_field, request, **kwargs)`
* `formfield_for_choice_field(db_field, request, **kwargs)`

Here is the example from the docs:

```python
class MyModelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "car":
            kwargs["queryset"] = Car.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
```

This shows that when `db_field.name = "car"`, the user should only be
able to select from those `Car` objects they actually own.
