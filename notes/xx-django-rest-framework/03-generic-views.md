# `rest_framework.generics` and `rest_framework.mixins`

## `GenericAPIView`

* Extends `APIView`.
  * Isn't quite an analogue of Django's `ListView` or a `DetailView`.
    Factors out some common properties.
* You pick the `queryset`/`get_queryset`.
* You pick `serializer_class`/`get_serializer_class`.
  * You can use `get_serializer_class` if you want to use either a
    regular-user or admin-user style serialization based on whether the
    requester is logged in as an admin.
* You pick the `lookup_field` which tells how to fetch an object by pk.
  You can specify `lookup_url_kwarg` also. Or you can go all-out and
  override `get_object`.
* You can pick `filter_backends`.
  * We'll see more of this later! This will allow them to do all sorts
    of query string filtering stuff.
  * The method `filter_queryset` will do the filtering for you.
* You can pick `pagination_class`.
* `get_object`: it will find the object requested, or raise a 404. It
  will check the permissions on the object for you.

## Concrete View Classes

* `CreateAPIView`: just has a `post` method that calls `create`. Uses
  `mixins.CreateModelMixin`.
* `ListAPIView`: just has a `get` method that calls `list`. Uses
  `mixins.ListModelMixin`.
* `RetrieveAPIView`: just has a `get` method that calls `retrieve`. Uses
  `mixins.RetrieveModelMixin`.
* `DestroyAPIView`: just has a `delete` method that calls `destroy`.
  Uses `mixins.DestroyModelMixin`.
* `UpdateAPIView`: has `put` and `patch` methods that call
  `update`/`partial_update`. Uses `mixins.UpdateModelMixin`.
* `ListCreateAPIView`: combines create and list.
* `RetrieveUpdateAPIView`: combines retrieve and update.
* `RetrieveDestroyAPIView`: combines retrieve and destroy.
* `RetrieveUpdateDestroyAPIView`: combines retrieve, update, and
  destroy.

## Mixins

* `CreateModelMixin`
  * Defines `create`.
  * It uses the serializer with `data=request.data`. Interesting: looks
    like serializers can go both ways?
  * Then it asks the serializer to do `is_valid`. Interesting: looks
    like serializers will do validation?
  * It then saves the model.
  * It renders the result with a 201 CREATED. It also gives a LOCATION
    header back.
  * It appears that it will look for a url field name property on the
    serialized data.
  * TODO: Will it do a redirect for us? Maybe not, because this is an
    API?
* `ListModelMixin`
  * Just defines `list`. Filters and fetches the queryset. Uses the
    paginator. Serializes.
* `RetrieveModelMixin`
  * Just defines `retrieve`. Calls `get_object` (which looks by pk/url
    kwarg). Serializes.
* `UpdateModelMixin`
  * `partial_update` just calls `update` with partial set to true.
  * Gets the target object.
  * Instantiates the serializer with *both* (1) the model instance, and
    (2) data. The serializer will also want to know whether this is a
    partial update.
  * The serializer checks validations, then it calls save.
* `DestroyModelMixin`
  * Defines `destroy`. Gets the model object and calls `delete`. Returns
    an empty response 204 NO CONTENT.

## Sources

* https://www.django-rest-framework.org/api-guide/generic-views/
* https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py
* https://github.com/encode/django-rest-framework/blob/master/rest_framework/mixins.py
