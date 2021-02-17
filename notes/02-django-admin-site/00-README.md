## Setup

You must start by running `./manage.py createsuperuser` to create a user
to administer the admin panel. You must update your project's primary
urls like so:

```python
from django.contrib import admin

urlpatterns = [
    # Project paths...
    path('cats/', include('cats.urls')),

    # Admin paths.
    path('admin/', admin.site.urls),
]
```

Any application can now register admin views:

```python
admin.site.register(models.Cat, CatAdmin)

# Create subclasses of admin.ModelAdmin
class CatAdmin(admin.ModelAdmin):
  pass

class ToyAdmin(admin.ModelAdmin):
  pass

# register these admins for the corresponding models.
admin.site.register(models.Cat, CatAdmin)
admin.site.register(models.Toy, ToyAdmin)

# alternatively:

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
  pass

```

You now have `admin/cats/cat` and `admin/toys/toy` routes. Django Admin
will look for an admin module in each of your applications and import
it. This is how it discovers your admin pages.

## The default `ModelAdmin` class

I will begin detailing the many features of `ModelAdmin`. Naturally, I
will cover those that most interest me, and skip those that do not.

**List View Display Fields**

This lists out all the model items. By default, it just calls `__str__`
to render each of the items. It provides a link to view a specific item.

To decide what fields to show in the list view, you can set
`list_display` to a list of field names. You can list four kinds of
things:

* A string that is a field name of the model.
* A string that is an attribute/method of the model that takes no
  arguments.
* A callable that takes an instance of the model and returns a string.
  * You can add a `short_description` attribute to a callable that will
    determine the column name.
  * You can also set an attribute on the callable of `boolean = True`.
    This will display a checkmark or x to show True/False.
* A string that is a *method name* of the *admin class*. The method
  should take an instance of the model.

BTW, you can use `django.utils.html.format_html` and
`django.utils.html.mark_safe` to return HTML that will be injected.

Normally the first field will be made into a link to the instance's
change form. However, you can set `ModelAdmin.list_display_links`. You
give a list of field names.

And also! You can set `list_editable` to set fields that can be edited
straight from the list page!! If you do this, a save button will be
provided.

**List View Ordering**

Fields can be selected for sorting. Not arbitrarily callables, usually.
Sorting is done at the database level, with an ORDER BY clause. However,
you can specify `admin_order_field` to give the corresponding column
name for a callable. This lets you continue to sort by a field if you
use a callable merely to change the display of the field.

In fact, you can even use a query expression!

**List View Actions**

There is a button to create a new item. This will take you to a form
where you can fill out various fields.

You may use checkboxes to select some of the items. You can apply an
"action" to these. The only out-of-the-box action is to delete.

**List View Filtering**

You can set a field called `list_filter`. This is an array of fields
that you should be allowed to filter on. You get a sidebar on the right
which lets you select values to show. You can even span relations here.

You can do deeper customization with a `SimpleListFilter`. Here's an
example:

```python
class BackwardNameFilter(admin.SimpleListFilter):
  # Displayed to user.
  title = "Backward name"

  # Used in query string.
  parameter_name = "backward_name"

  # Lookups the user may choose from.
  def lookups(self, request, model_admin):
    names = models.Cat.objects.values_list('name', flat=True)
    # [(value (which is serialized in query string), display name)]
    return [(name, name[::-1]) for name in names]

  # Perform the querying.
  def queryset(self, request, queryset):
    if self.value() is None:
      return queryset
    return queryset.filter(name=self.value())
```

TODO: There are some other helpful `FieldListFilters`, which I can
probably find more about in the github.

There is a field called `date_hierarchy`. If you specify a fieldname,
then the list view will give a bunch of filter options to only show
those objects with a date in the last hour, day, week, month, year, et
cetera. This field name can even dereference an association, like so:
`date_hierarchy = 'author__birth_date'` would allow you to show just
those articles with authors with a certain birth date.

**List Pagination**

`list_per_page` is set to 100 by default. A show all link will be shown
if the number of total objects is less than `list_max_show_all` (default
200).

**Detail/Form View Fields and Fieldsets**

`exclude` and `fields` can be used to list what fields appear in the
detail view. By default, all fields are editable. If you want to have a
non-editable field, you set `readonly_fields`. Note that these apply
equally to both the detail view (the change form) and the create form.

By default fields are listed one after another. But you can also make
several fields appear on the same line like so:

```python
class CatAdmin(admin.ModelAdmin):
  # Now name, age will appear on the same line.
  fields = [('name', 'age'), ('view_count', )]

  readonly_fields = ('view_count', )
```

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

A class that is helpful out-of-the-box are: `collapse`, which will start
this fieldset in a collapsed state, and you can click to expand.

**Further Form Customization**

* By default, the admin will generate a `ModelForm` for you. I don't
  know very much about ModelForm presently; I haven't studied it yet!
* You can specify the `ModelForm` yourself by setting the `form`
  attribute. I will have to look into this.

## TODO

* TODO: I've read up to here:
  * https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_select_related
* https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_horizontal
* https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_overrides

* Will probably have to look up `ModelForm`.
* https://docs.djangoproject.com/en/3.1/ref/contrib/admin/actions/
* https://docs.djangoproject.com/en/3.1/ref/contrib/admin/admindocs/
* https://docs.djangoproject.com/en/3.1/ref/contrib/admin/javascript/
