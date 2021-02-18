# List View Fields

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
