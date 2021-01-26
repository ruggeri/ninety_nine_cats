# `rest_framework.response.Response`

This appears to play the role of Django's `HttpResponse`, but it is
initialized with *unrendered data*, and based on content-negotiation,
DRF will decide how to render the data. Properties include:

* `.data`: the unrendered data.
* `.status`: the status code.
* `.template_name`: if they want HTML rendering, what template should be
  rendered?
* `.headers`: a dictionary of headers to render.

There's a method called `#render` that they will call. This fills out
`.content`.

## Sources

* https://www.django-rest-framework.org/api-guide/responses/
* https://github.com/encode/django-rest-framework/tree/master/rest_framework/response.py
