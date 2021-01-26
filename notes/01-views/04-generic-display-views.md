# Generic Display Views

## `django.views.generic.detail.DetailView`

* Mixins:
  * `SingleObjectTemplateResponseMixin`
    * Basically: just tries to use the model name to guess the template
      name.
    * `TemplateResponseMixin` (previously covered)
  * `BaseDetailView`
    * Simply defines a `get` method that will call `get_object` (from
      `SingleObjectMixin`) to get the object, `get_context_data` (from
      `ContextMixin`) to get the rendering context, and
      `render_to_response` (from `TemplateResponseMixin`) render the
      template.
    * `SingleObjectMixin`
      * `get_queryset`:
        * Uses `queryset` property if provided.
        * Else it uses the `model` property's default manager.
      * `get_object`:
        * Uses `pk_url_kwarg` to get the pk out of the kwargs provided
          by the URL router. If provided, finds the object with the
          specified pk.
        * Will also try to get a slug with the `slug_url_kwarg`. Will
          try to find the object with the specified slug, using the
          `slug_field` property (defaults to `'slug'`).
      * `get_context_object_name` can be used to customize the name of
        the object in the context. It's always available as
        `context['object']`. If you don't specify a property
        `context_object_name`, it will just guess from the object's
        model name.
      * Uses `get_context_data` to store the object in the context.
      * `ContextMixin` (previously covered)

## `django.views.generic.list.ListView`

* Mixins:
  * `MultipleObjectTemplateResponseMixin`
    * Tries to figure out the template name.
    * `TemplateResponseMixin` (previously covered)
  * `BaseListView`
    * Defines a `get` method for you.
      * Will simply fetch the objects, build out the context, and render
        the template.
    * `MultipleObjectMixin`
      * `get_queryset`:
        * You can specify by `queryset` property of course.
        * Else uses `model`'s default manager.
        * If you specify `ordering` or `get_ordering`, it wil be used.
      * `paginate_queryset` method:
        * This is used to paginate results.
        * If you give a `paginate_by`/`get_paginate_by` (integer) value,
          pagination will be performed.
        * It will call `get_paginator`. This constructs an instance of
          the specified `paginator_class`. A default paginator is
          provided by Django.
        * The `page_kwarg` property is used to pull out what page we
          want. It'll look in the URL params, the GET request params,
          and finally default to page 1.
      * `get_context_data`:
        * `context_object_name`/`get_context_object_name` specifies a
          name for the queryset.
        * `object_list` is the default.
      * `ContextMixin` (previously covered)
