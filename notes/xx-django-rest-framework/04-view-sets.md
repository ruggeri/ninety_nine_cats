# `rest_framework.viewsets`

## Motivation/Introduction

* Viewsets are like controllers in Rails. They're a place to place
  related view functions.
  * In particular, the Rails `CatsController` would have methods for the
    CRUD actions, even though these have different urls.
  * A `View` in Django typically has only one url associated. Different
    HTTP method verbs can be dispatched to different View methods. But
    you kind of can't do a list + detail view.
  * There *are* a bunch of generic views for `RetrieveUpdateDestroyView`
    and `ListCreateView`.
* Thus we have `ViewSet`s.
  * You define methods like `list`, `create`, `retrieve`, `update`,
    `destroy`.
  * You then use `DefaultRouter` to register routes like so:

```python
# urls.py
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
urlpatterns += router.urls
```

* They provide:
  * `ViewSet`: basic view set implementation. But it has all the magic.
    Derives from `ViewSetMixin` and `APIView`.
  * `GenericViewSet`: still basic. But derives from `GenericAPIView`
    instead of `APIView`, and thus has `get_object` and `get_queryset`
    methods.
  * `ReadOnlyModelViewSet`: `GenericViewSet` with `RetrieveModelMixin`
    and `ListModelMixin` mixed in.
  * `ModelViewSet`: has all five CRUD mixins mixed in.

## `viewsets.ViewSet`

* All the magic is here!
* `as_view` returns a `view` function:
  * You've got to give it a actions mapping of `{ httpVerbName:
    classMethodName }`.
  * But I guess `as_view` is going to get called by `DefaultRouter` for
    us usually. But this is how it works.
  * Like the typical Django `as_view`, this will instantiate the class.
  * It will also go through the actions map, and make aliases for each
    HTTP verb to each target method.
  * And last, it will call the usual `dispatch` method.
  * Dispatch will work as expected because of the aliases from the
    actions map.
* `@action`:
  * `@action` decorator is defined in `rest_framework.decorators`.
  * `methods`: you specify what HTTP verbs to reply to.
  * `detail`: a boolean of whether this is a list or detail view.
  * `url_path`: by default, the path is generated by taking the Python
    method name and appending it to the usual list or detail path.
  * `url_name`: this is the name used for reverse mapping.
  * Instead of `url_name`, I think you can specify `suffix`?
* `get_extra_action_url_map`:
  * Will give you any extra actions defined on the `ViewSet`.
  * Kind of weird. It's defined on an *instance*. The instance should be
    marked as list or detail. It will only return extra actions of that
    type.
  * I presume that the way the router works is it adds adds separate URL
    patterns for list and instance. Any further dispatch needs to know
    what kind of actions apply.
* Properties
  * When the view is instantiated, it should be provided with `basename`
    and `detail`.
  * I think for logging, a view can have a `name`, or more simply a
    `suffix`, in which case the basename is also used to generate the
    name. But I think this is only used for logging?

To have a more full understanding, I think we need to get into routing,
also. And maybe play around.

## Sources

* https://www.django-rest-framework.org/api-guide/viewsets/
* https://github.com/encode/django-rest-framework/blob/master/rest_framework/viewsets.py
* https://github.com/encode/django-rest-framework/blob/master/rest_framework/decorators.py#L123