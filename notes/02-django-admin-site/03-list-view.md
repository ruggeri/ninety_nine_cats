# Customizing The List View

## Choosing What Fields To Display

By default, `__str__` is called for each of the objects. This is
hyperlinked to the detail view for the object.

To decide what fields to show in the list view, you can set
`list_display` to a list of field names. You can list four kinds of
things:

1. A string that is a field name of the model.
2. A callable that takes an instance of the model and returns a string.
    * You can add a `short_description` attribute to a callable that
      will determine the column name.
    * You can also set an attribute on the callable of `boolean = True`.
      This will display a checkmark or x to show True/False.
3. A string that is a *method name* of the *admin class*. The method
   should take an instance of the model.
4. A string that is an attribute/method of the model that takes no
   arguments.

## Generating HTML

If you write a method, you may want to return HTML to be directly
injected. If so, you want to return an instance of
`django.utils.safestring.SafeString` (a simple wrapper of `str` with an
`__html__` method). The easiest way to produce one is
`django.utils.html.mark_safe`.

You should obviously be escaping user generated data. Python comes with
`html.escape` to do this.

As a convenience, you can use `django.utils.html.format_html`. This will
call `html.escape` on the format arguments. Then it will interpolate
them for you in the normal way into the format string. Last, it will
call `mark_safe` on the result for you!

## Other List Field Options

Normally the first field will be made into a link to the instance's
change form. However, you can set `ModelAdmin.list_display_links`. You
give a list of field names. Each of these becomes a link to the object's
change page. Of course, you probably need exactly one such field.

You can make fields editable directly in the admin! You can set
`list_editable` to set certain fields that should be allowed to be
edited straight from the list page. They will be displayed as input
tags. If you do this, a save button will be provided.

## Ordering/Sorting

The list page will let you click on columns to sort by those. Click
triggers a full page reload. The ordering is done at the database level
with an ORDER BY clause.

Thus, if you have a non-field column, such as specified by a callable,
Django admin won't let you sort on that. This would be annoying if you
simply wanted to colorize or change the presentation of some model
field.

Luckily, you can set an `admin_order_field` attribute on the callable to
specify what underlying field should be used in the ORDER BY to sort
with respect to this column.

In fact, you can even use a query expression!

If you want to disable sorting on some fields, you can specify
`sortable_by` to a list of fields you are allowed to sort by.

## Filtering

You can get Django admin to give you a bunch of filters that can be
selected in a right sidebar.

**Filtering By Value**

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

**Writing Your Own Filters**

You can do deeper customization with a `SimpleListFilter`. Here's an
example:

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

**Using a `FieldListFilter`**

When you give just a field name, Django will try to pick an appropriate
filter. Here is the order of kinds of filters it considers:

* `RelatedFieldListFilter`
  * Applies to remote fields. Gives a set of choices of related objects.
    On the cats list page, lets you pick a toy, for instance.
  * Includes also an "empty" choice to filter only those cats with no
    toys.
* `BooleanFieldListFilter`
  * Applies to boolean fields. Will let you pick Yes, No, or Unknown
    (`NULL`).
* `ChoicesFieldListFilter`
  * If it is a choices field, then this lists the choices.
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

## Pagination/Ordering

`list_per_page` is set to 100 by default. A show all link will be shown
if the number of total objects is less than `list_max_show_all` (default
200).

You can set an `ordering` attribute. It has the expected result.

## Optimization

The `list_select_related` option can be set to a tuple of fields to pass
those to `Queryset#select_related`.

By default, `list_select_related` is set to `False`. That means it will
call `select_related` with *no* params, which means that all
non-nullable relations will be selected! But the `ModelAdmin` will only
do this if the list fields include a relation field.

Basically: you should set `list_select_related` if you know that you
need a related field because of some `ModelAdmin` method field, that
colorizes/decorates/hides a `Model` field.

## List View Actions

There is a button to create a new item. This will take you to a form
where you can fill out various fields.

You may use checkboxes to select some of the items. You can apply an
"action" to these. The only out-of-the-box action is to delete.

TODO: can we add others???

## Searching

You can list the `search_fields`. This will give you a search text box.
The searching algorithm is simple. Say you search `"John Lennon"`. Then
this is split to the words `"John", "Lennon"`. Next, say you have listed
the fields `search_fields = ['first_name', 'last_name']`. Then the query
performed includes the fragment:

```sql
WHERE (first_name ILIKE '%John%' OR last_name ILIKE '%John%')
  AND (first_name ILIKE '%Lennon%' OR last_name ILIKE '%Lennon%')
```

If you want to be more specific about the field lookup, you can say
`'first_name_exact'`.

By default, only a limited number of results will be shown. Presumably
it is equal to the page size? The total number of matches will be shown
(even though not all the results themselves). Since this is potentially
expensive to compute, you can set `show_full_result_count = False` as an
optimization.
