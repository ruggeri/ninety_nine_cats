# `rest_framework.views.APIView`

* They are class-based, like Django CBVs.
  * But you get an incoming DRF `Request` instance.
  * And you may return an outgoing DRF `HttpResponse` instance.
  * Content negotiation will be performed for you.
  * Authorization can be performed for you.

* Various configuration classes include:
  * `::renderer_classes`
  * `::parser_classes`
  * `::authentication_classes`
  * `::permission_classes`
  * These will be covered in later readings. These just configure the
    `APIView`.
* Basically, `APIView` doesn't do anything super fancy besides actually
  perform the various content negotiation/authentication/permission
  checking/throttling.
* Otherwise, it's mostly just a wrapper around the standard Django
  `View`.

## Decorators

* If you want to use function-based views (FBVs), you can use the
  decorator `@api_view(http_method_names=['GET'])`. You specify what
  HTTP method names the function should be invoked for.
* I will, for the moment, mostly ignore decorator/FBVs.

## Sources

* https://www.django-rest-framework.org/api-guide/views/
* https://github.com/encode/django-rest-framework/blob/master/rest_framework/views.py
* https://github.com/encode/django-rest-framework/blob/master/rest_framework/decorators.py
