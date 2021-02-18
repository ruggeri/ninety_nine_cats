# List View Filtering

You can get Django admin to give you a bunch of filters that can be
selected in a right sidebar.

## Filtering By Value

The simplest way to use the `list_filter` attribute is to simply give a
list of column names. The filter will present the distinct values of the
column on the right hand side. You can select one of these, and the
admin list will show only those objects that match the filter.

Quickly there can become too many values. Django admin does not set a
limit to the distinct values displayed.

This kind of filter works simply: it just does a SELECT DISTINCT on the
listed fields to get their possible values. It's actually probably
pretty slow, unless you have an index on the field (which you probably
don't want!).

## Writing Your Own Custom Filter

You can do deeper customization with a `SimpleListFilter`. Here's an
example that demonstrates the API:

```python
class BackwardNameFilter(admin.SimpleListFilter):
  # Displayed to user as the title in the sidebar.
  title = "Backward name"

  # This is the parameter name that will be used in the query string.
  parameter_name = "backward_name"

  # This method does the work of finding what the possible values are.
  # It is run on load to generate the choice set.
  def lookups(self, request, model_admin):
    names = models.Cat.objects.values_list('name', flat=True)
    # [(value (which is serialized in query string), display name)]
    return [(name, name[::-1]) for name in names]

  # Perform the querying. Only called if a value has been selected. We
  # can access the selected value with `#value()`.
  def queryset(self, request, queryset):
    return queryset.filter(name=self.value())

class CatAdmin(admin.ModelAdmin):
  list_display = ('name', 'age')
  list_filter = (BackwardNameFilter)
```

## Using Built-In `FieldListFilter`s

When you give just a field name, Django will try to pick an appropriate
filter. You can also specify if you use the format `(field_name,
FilterType)`. For auto-selection, here is the order of kinds of filters
Django considers:

* `RelatedFieldListFilter`
  * Applies to remote fields. Gives a set of choices of related objects.
    On the cats list page, lets you pick a toy, for instance.
  * Includes also an "empty" choice to filter only those cats with no
    toys.
* `BooleanFieldListFilter`
  * Applies to boolean fields. Will let you pick Yes, No, or Unknown
    (`NULL`).
* `ChoicesFieldListFilter`
  * If it is a choices field, then this lists the choices. Just an
    optimization over `AllValuesFieldListFilter`.
* `DateFieldListFilter`
  * This lists "any date", "past 7 days", "this month", "this year."
* `AllValuesFieldListFilter`
  * This is your default, registered last. It differs from the choices
    filter because it does a query to find the possible values.

Here are two special ones, that you must select yourself:

* `RelatedOnlyFieldListFilter`
  * Same as `RelatedFieldListFilter`, but does an extra query to only
    present those related objects (toys) which belong to some cat.
  * That is, it doesn't list a toy as a choice if no cat owns it,
    anyway.
* `EmptyFieldListFilter`
  * This lets you search to see if a field is `NULL` or not.
