# `rest_framework.request.Request`

This is a wrapper for Django's `HttpRequest` object. It sounds like
mostly a convenience. It provides some attributes:

* Request parsing:
  * `.data`: which is similar to `HttpRequest#POST`, except it also has
    `PUT` and `PATCH` data, as well as the `HttpRequest#FILES`.
  * `.query_params`: a better named `HttpRequest#GET`. They mention that
    *any* request method may include query parameters, not just `GET`...
* Authentication:
  * `.user`: if any authentication is done by middleware, the `.user`
    attribute is filled out. We'll learn more when we look at
    authorization.
  * `.auth`: any additional authorization context.

## Sources

* https://www.django-rest-framework.org/api-guide/requests/
* https://github.com/encode/django-rest-framework/tree/master/rest_framework/request.py
