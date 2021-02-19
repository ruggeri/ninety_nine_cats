## Authentication And Web Requests

Because a middleware has been installed, `request.user` will always be
filled out. It will either be the logged in user, or it will be an
instance of `AnonymousUser`. `AnonymousUser` is a dummy class with no
database backing. You can tell them apart by calling `is_authenticated`;
this is defined `True`/`False` on `User`/`AnonymousUser`.

To login a user, call `django.contrib.auth.login(request, user)`. This
first clears any existing session. Then it stores some info like the
user's id. You'll of course typically want to use
`django.contrib.auth.authenticate` before calling `login`.

To log a user out, simply use `django.contrib.auth.logout(request)`. All user
session data will be cleared.

## Limiting Views To Authenticated Users

The simplest way is to, in your view code, check
`request.user.is_authenticated`. If they are not, then issue a redirect.

Alternatively, you can use the `@login_required` decorator from
`django.contrib.auth.decorators`.

When you send someone to the `settings.LOGIN_URL`, you also specify a
`next` query parameter which is where to redirect the user back to after
login. This is taken care of by the `@login_required` decorator.

When using class based views, you'll want to use `LoginRequiredMixin`.
It works just like `@login_required`. Basically, it just does the check
before calling `dispatch`.

## Limiting Views To Specific Users

Let's say you want to only let users access a view if they pass a
"test." For instance, you want the user to have an email ending in
`@self-loop.com`.

You can easily test this yourself in your view code. You might issue a
redirect to login, but also if the user *is* logged in, but simply
doesn't pass the test, you might want to redirect them elsewhere.

One way to do this is to use
`django.contrib.auth.decorators.user_passes_test(test_fn, redirect_url,
next_field_name)`. By default `redirect_url` will be set to the login
URL. But you could set this to anything. If you don't have the user
login, you'll want to set `next_field_name = None`, because the user
won't be redirecting here...

When using CBVs, you'll want to use the `UserPassesTestMixin`. Here you
define `test_func` to  determine the test they should pass. You can also
override the method `handle_no_permission`, which determines what should
happen if the user fails the test. Alternatively, you can set
`login_url`, `permission_denied_message`, `redirect_field_name`
properties.

## Checking A User's Permissions

Another common scenario is testing whether a user has a certain
permission. You can do so with the `permission_required` decorator:

```python
@permission_required("cats.add_cat")
def my_view(request):
  pass
```

You can set the `login_url` to redirect them elsewhere, if desired. Or
you can set `raise_exception=True` if you want to raise a 403
PermissionDenied error.

They give an example of where you can raise an exception if the user
doesn't have permission, but give the user a chance first to login (if
they haven't already):

```python
@login_required
@permission_required("cats.add_cat", raise_exception=True)
def my_view(request):
  pass
```

Notice that if we don't set `permission_required=True`, we risk a
"login-circle" by trying to send a logged-in user without the correct
permission back to the login page, with a next parameter set to return
here again...

For CBVs, of course there is a mixin: `PermissionRequiredMixin`. You mix
this in and set `permission_required` to a permission codename or list
of codenames.

By default, the `AccessPermission` will *not* blindly redirect to the
login page if the user is already logged in.
