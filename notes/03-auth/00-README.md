## Caching

`ModelBackend` will cache fetched user permissions on the model. If you
modify permissions, you may want to "refresh" the user.

## Password Validators

We can validate whether the password meets threshold criteria of a
strong password. This is configured in
`settings.AUTH_PASSWORD_VALIDATORS`. By default, a number of criteria
(length, similarity to other fields, on a list of common passwords) will
be checked. These will be used by default to check passwords whenever
`set_password` is called.

## TODO

* Authentication in Web requests (earlier parts have already been completed)
  https://docs.djangoproject.com/en/3.1/topics/auth/default/#authentication-data-in-templates

https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
