# Customizing The Detail View

The detail view includes both the change and create forms.

`exclude` and `fields` can be used to list what fields appear in the
detail view. By default, all fields are editable. If you want to have a
non-editable field, you set `readonly_fields`. Note that these apply
equally to both the detail view (the change form) and the create form.

Similar to how `list_display` can call methods of the model or admin, so
can `fields`. These fields must be marked in `readonly_fields`, though.

```python
class CatAdmin(admin.ModelAdmin):
  def backward_name(self, model):
    return model.name[::-1]

  fields = ('name', 'age', 'backward_name')
  readonly_fields = ('view_count', 'backward_name')
```

## Inline Fields

By default, fields are listed one after another. But you can also make
several fields appear on the same line like so:

```python
class CatAdmin(admin.ModelAdmin):
  # Now name, age will appear on the same line.
  fields = [('name', 'age'), ('view_count', )]

  readonly_fields = ('view_count', )
```

## Fieldsets

You may apply even more control by using the `fieldsets` option:

```python
class CatAdmin(admin.ModelAdmin):
  # Each fieldset is of the format 'name', then options. The name is
  # displayed at the top of the fieldset.
  #
  # Options include `'classes'` (CSS classes), and `'fields'`, which
  # is simply the fields to display in the usual format. `'description'`
  # lets you add a little helper text at the top of the fieldset.
  fieldsets = [
      (None, {
          'fields': [('name', 'age')]
      }),
      (
          'Advanced', {
              'classes': ('collapse', ),
              'fields': ('view_count', ),
          }
      )
  ]
```

A class that is helpful out-of-the-box is `collapse`, which will start
this fieldset in a collapsed state, and you can click to expand.

## Foreign Key Field Types

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
that works soon!

Last, and most simply, you can set `raw_id_fields = ['cat']`. This lets
you directly write in a Cat id. You can also write a comma separated
value if this is a `ManyToManyField`.

## Save Actions

* You can set `save_as` to give a "Save as New" option. This creates a
  modified clone.
* You can also add `save_on_top = True` to show save buttons at the top
  of your model.

## Further Form Customization

* By default, the admin will generate a `ModelForm` for you. I don't
  know very much about `ModelForm` presently; I haven't studied it yet!
* TODO: You can specify the `ModelForm` yourself by setting the `form`
  attribute. I will have to look into this.
* TODO: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_overrides
  * This talks more about how to override some details of the default
    `ModelForm` without writing your own `ModelForm`.
