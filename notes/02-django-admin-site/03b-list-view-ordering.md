# List View Ordering/Sorting

The list page will let you click on columns to sort by those. Click
triggers a full page reload. The ordering is done at the database level
with an ORDER BY clause.

If you have a non-field column, such as specified by a callable, Django
admin won't let you sort on that. This would be annoying if you simply
wanted to colorize or change the presentation of some model field.

Luckily, you can set an `admin_order_field` attribute on the callable to
specify what underlying field should be used in the ORDER BY to sort
with respect to this column. In fact, you can even use a query
expression!

If you want to disable sorting on some fields, you can specify
`sortable_by` to a list of fields you are allowed to sort by. Don't know
why you would want to do this, though.

You can set an `ordering` attribute. It specifies a *default* ordering,
but this can be overridden if the user clicks a column. The default
ordering is shown in the UI.
