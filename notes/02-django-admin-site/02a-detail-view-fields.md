# Customizing Detail View Fields

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

## Multiple Fields Per Line

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
