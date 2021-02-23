## Basics

The auth system contains:

1. Users
2. Permissions: binary yes/no flags for whether a user is allowed to
   perform an action.
3. Groups: a user can be associated with a group that has a set of
   permissions enabled for all members.
4. Password hashing/storage/verification

At a high-level, the `AuthenticationMiddleware` will store/read the
logged in user credentials in the session. This requires that
`SessionMiddleware` is also installed. Presumably the
`SessionMiddleware` will store data in a cookie.

## `User`

An `AbstractBaseUser` has:

1. `password`
  * This takes care of some fanciness where only a password hash is
    stored in the DB.
2. `last_login`

A `User` is a trivial extension of `AbstractUser`, which has the
properties:

1. `username`
2. `first_name`, `last_name`
3. `email`
4. `is_staff` (boolean for whether this user is staff)
5. `is_active` (boolean to uncheck when a user is "deleted")
6. `date_joined`

`User` also mixes in `PermissionsMixin`. This has the properties:

1. `is_superuser` (boolean for whether this user is a superuser)
2. `groups`
  * A `ManyToManyField` associating with `Group`s.
3. `user_permissions`
  * A `ManyToManyField` associating with `Permission`s.

The most useful method of `PermissionsMixin` is of course
`User#has_perm(permission_name)`.

**`UserManager`**

The `UserManager` has a few methods:

* `UserManager#create_user(username, email, password, kwargs)`
  * This creates a normal user.
* `UserManager#create_superuser(username, email, password, kwargs)`
  * This creates a user who is both staff and a superuser.
* `UserManger#with_perm(permission_name, is_active=True, include_superusers=True)`
  * You give a permission name, and this returns all users with this
    permission.

**User Creation**

In addition to doing things with the `UserManager` methods, you may use
some `./manage.py` commands:

* `./manage.py createsuperuser`
  * Odd, there isn't a command for create a normal, or staff user? I
    guess you're supposed to do it from the Django console?
* `./manage.py changepassword`

Of course, you can also do things from the Django admin. Last, I believe
Django gives you pages for users to create *themselves*, though I don't
know how to do that yet!

**Authenticating Users**

* The easiest way is `django.admin.authenticate(request, username,
  password)`. This returns an instance of `User`, if any matches the
  credentials.
  * There isn't an easy way to say `User.authenticate`. Why?
  * I think the reason is that there may be more than one authentication
    "backend," and thus going directly to the model is too direct.
  * I'm not sure why `request` is needed...
    * I think maybe some external backends might want it?
* But I think you seldom will need this, since we'll later see how users
  can login through a typical web view.

**Password Strength Validation**

We can validate whether the password meets threshold criteria of a
strong password. This is configured in
`settings.AUTH_PASSWORD_VALIDATORS`. By default, a number of criteria
(length, similarity to other fields, on a list of common passwords) will
be checked. These will be used by default to check passwords whenever
`set_password` is called.

## `Permission`s

Permissions are used internally by the Django admin. You can create your
own permissions. Here are the fields of the `Permission` model:

1. `name`: a human-readable name/description of the permission
2. `content_type`: the kind of model that the permission pertains to
  * In Django, by default, you can't give permission to just a certain
    subset of model instances. It pertains to the entire class.
3. `codename`: a name that can be programmatically generated easily.
  * Of course, `(content_type, codename)` must be unique.

Django admin will make a few permissions per model:

1. `view_cat`: let the user look at cats.
2. `add_cat`: let the user create cats.
3. `change_cat`: let the user change cats.
4. `delete_cat`: let the user delete cats.

However, you can be more explicit in Django `ModelAdmin` instances and
override the various `has_view_permission`, `has_add_permission`, et
cetera.

These permissions are automatically added because Django admin schedules
a `post_migrate` listener.

## `Group`s

A `Group` is a simple model. We already described the `User`'s
`ManyToManyField` to `Group`. The `Group` itself has a `ManyToManyField`
to `Permission`.

## Creating New Permissions

It's simple. You create a new `Permission` model instance. You set
`codename` to something unique, `name` to something human readable, and
you set `content_type = ContentTypes.objects.get_for_model(SomeModel)`.

But the more common way is like this:

```python
class Task(models.Model):
    # Here you can list custom permissions that will be added by a post
    # migration hook.
    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]
```
