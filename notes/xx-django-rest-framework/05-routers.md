# `rest_framework.routers`

You instantiate a router instance. You `#register` some view sets. And
then you add `router.urls` to the urlpatterns.

## `BaseRouter`

* Just has a `register(prefix, viewset, basename)` method.
  * Will simply add an entry to the 'registry' or routes.

## `SimpleRouter`

* Extends `BaseRouter`.

* List route:
  * `url`: `r'^{prefix}{trailing_slash}$'`
  * `mapping`: `{'get': 'list', 'post': 'create'}`.
  * `name`: `'{basename}-list'`
  * `detail`: False
* Dynamic list routes:
  * `url`: `r'{prefix}/{url_path}{trailing_slash}'`
  * `name`: `'{basename}-{url_name}'`
  * `detail`: False
* Detail route:
  * `url`: `r'^{prefix}/{lookup}{trailing_slash}$'`
  * `mapping`: get->retrieve, put->update, patch->partial_update,
    delete->destroy.
  * `name`: `'{basename}-detail`
  * `detail`: True
* Dynamic detail route:
  * `url`: `r'^{prefix}/lookup}/{url_path}/{trailing_slash}$'`
  * `name`: `'{basename}-{url_name}'`
  * `detail`: True

* It will try to get a default basename by looking at the
  `viewset.queryset.model` if available. But this won't work if you
  defined your own `get_queryset` method.
* `#get_routes`: The static routes are good, even though they map to
  several viewset actions. But the dynamic routes need to be expanded.
  If there are several custom list actions, then we need to create a
  dynamic route for each. And this is what `get_routes` does.
  * Basically 'expands' the `{url_path}` part of `url` and the
    `{url_name}` part of `name`.
* `#get_urls`: the implementation iterates the registry and generates
  routes for each viewset registered.
  * Does the final expansion of route url format strings. Expands the
    prefix, any pk lookup part, and the trailing slash.
  * It will instantiate the viewset as a view.
  * It will set the view's `basename`. It will set the view's `detail`
    appropriately to whether this is a list or detail view.

## `DefaultRouter`

* Extends `SimpleRouter`
* You can ask it to `include_root_view`
  * I think this is like a view that documents the routes for you.
  * But I'm not that interested right now...
* You can also ask the URLs to be extended by additional URLs that have
  a `.{format}` at the end, like Rails allows the user to specify the
  format with the suffix. This can be convenient.

## Summary

* I hope this helps.
* Viewsets and Routers seem fairly closely tied together. I think you'll
  want to use them together, rather than on their own.
* It's a little wonky how Routers find the actions defined on viewsets,
  and also how the viewset methods define the routing information. But
  now we've seen!

## Sources

* https://www.django-rest-framework.org/api-guide/routers/
* https://github.com/encode/django-rest-framework/blob/master/rest_framework/routers.py
