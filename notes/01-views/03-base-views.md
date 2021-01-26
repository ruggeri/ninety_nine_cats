# Base Views

## `django.views.generic.base.View`

* The most basic view.
* `http_method_names` allows you to set a property to filter which
  methods can be defined. But you can probably leave this alone and
  simply *not define* the methods you don't want to support.
  * `options` method allows you to reply with the allowed HTTP verbs.
  * There's also `http_method_not_allowed`: this is called if the http
    method is not allowed. By default, produces a
    `HttpResponseNotAllowed` 405 with a list of the allowed method
    names.
* `as_view`: this is what you use to convert the CBV to the FBV needed
  by `pattern`.
* `setup`: a hook before dispatch where it sets itself up.
* `dispatch(request)`: this is the entrypoint to everything. It will
  delegate the various HTTP methods to various methods.

* https://docs.djangoproject.com/en/3.1/ref/class-based-views/base/

## `django.views.generic.base.TemplateView`

* Very simple view. It's going to simply leverage `ContextMixin` and
  `TemplateResponseMixin`.
  * It will call `get_context_data`, and then pass this into
    `render_to_response`.

**`ContextMixin`**

* Responsible for building out a context object.
* Looks for an `extra_content` attribute. This can also be specified as
  a kwarg of `as_view`.
* `get_context_data`: you can override this to add properties. Various
  mixins will define their own `get_context_data` methods to fill out
  their own contributions to the context.

**`TemplateResponseMixin`**

* `template_name`: you need to specify this so it knows what to render.
* There are other properties like: `template_engine`, or
  `response_class`. But you shouldn't need these if you're just
  rendering using a normal Django template.
* Basically, it's just going to produce a `TemplateResponse`, which
  lists the name of the template, the engine, and the context. Some
  other *middleware* will take care of the rendering later.

## `django.views.generic.base.RedirectView`

* Will simply let the user specify a redirect URL.
  * You can either use `url` class property, or `get_redirect_url`
    instance method.
  * You can also use `pattern_name` if you want to use a reversal URL
    mapping name.
* You can specify permanent or not.
