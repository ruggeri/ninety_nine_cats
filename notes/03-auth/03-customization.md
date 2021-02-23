You can customize and create your own backends. They can be external, or
they might add features to track per-object permissions. Presumably
there are third party libraries for common scenarios. I don't want to
get bogged down in those details, though.

They talk a bit about how to customize the user model. They recommend
creating a second model, and having a `OneToOneField` to the user.

On the other hand, you could create your own custom user model extending
`AbstractUser`, and set `settings.AUTH_USER_MODEL =
"myapp.MyUserModel"`. They recommend you do it from the start; it is
tricky to change the user model after the first migration has been run
:-|

Django seems to lean toward the `OneToOneField` way, but also endorses
`AbstractUser` extension.

Source: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
