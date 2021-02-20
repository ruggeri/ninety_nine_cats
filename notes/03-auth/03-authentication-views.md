# Setting Up Django Authentication Views

You need to first add the appropriate url patterns:

```python
# settings.py

urlpatterns = [
  path('accounts/', include('django.contrib.auth.urls'))
]
```

## Login/Logout Views

* `/accounts/login?next=something` (url name: `login`)
  * template name: `registration/login.html`.
    * You must provide this template.
  * This is both an endpoint for GET (the form), or POST (submit
    credentials and try to log user in).
  * On POST success, it will redirect to the url specified by the `next`
    parameter.
      * BTW, the `AuthenticationForm` will call `authenticate` to check
        credentials.
      * And then the `LoginView#form_valid` method will be called. This
        calls `login` to store the user data in the session.
  * If this is not specified, it will redirect to
    `settings.LOGIN_REDIRECT_URL`.
* A helpful `django.contrib.auth.redirect_to_login(next)` will generate
  the needed URL for you!

* `/accounts/logout?next=something` (url name: `logout`)
  * This view logs the user out.
  * Will redirect to either `next` parameter (if specified), or
    `settings.LOGOUT_REDIRECT_URL`.
  * If neither redirect URL is provided/set, then render
    `registration/logged_out.html`.

## Password Change Views

* `/accounts/password_change` (url name: `password_change`)
  * Template is `registration/password_change_form.html`.
  * This is both a GET and a POST endpoint.
  * On POST success, will redirect to attribute `success_url`. By
    default that is `password_change_done`.
  * Notice that the work of processing the form is done by
    `django.contrib.auth.forms.PasswordChangeForm`.
    * This does cool stuff like validating that the two password fields
      match.
    * Most importantly, it calls `set_password` in the `Form#save`
      method. This ensures that the password will be hashed.
* `accounts/password_change/done` (url name: `password_change_done`)
  * This is a success view to inform the user of what has been done.
  * Template: `registration/password_change_done.html`

## Requesting A Password Reset

* `accounts/password_reset` (url name: `password_reset`)
  * Template: `registration/password_reset_form.html`
  * Again, a GET and POST endpoint.
  * This will send an email to the user with a unique token allowing
    them to reset their password.
    * There are templates for generating the email body/subject.
  * As usual, POST success redirects to `password_reset_done`.
  * A unique ID will be generated for you by
    `PasswordResetTokenGenerator`.
    * This will take (1) the user's pk, (2) the current hash of the
      user's password (including the current salt).
    * This token can be used at most once, because even if the user uses
      the exact same password as before, a different random salt will be
      used when hashing the password.
    * Note: asking for a password reset doesn't log the user out.
    * Also note: the token generator will embed (signed) information
      about *when* the token was generated. Thus, the generator can (and
      will) reject tokens if they become too old.
* `accounts/password_reset/done` (url name: `password_reset_done`)
  * This success view shows a message that the password was reset
    successfully.
  * Template: `registration/password_reset_done.html`

## Completing A Password Reset

* `accounts/reset/<uidb64>/<token>/` (url name: `password_reset_confirm`)
  * `uidb64` is the user's id. `token` is the one-time token.
  * Initial GET flow:
    * First, check that a user exists for `uidb64`.
    * Next, check that the token is valid for this user.
    * Now store this token in the *session*.
    * Redirect to `accounts/reset/<uidb64>/set-password`.
      * This is a trick to avoid leaking the token from the referrer.
  * 2nd GET flow:
    * Get the user for the `uidb64` as before.
    * Notice that `token == "set-password"`.
    * Get the token out of the *session*. Check it.
    * Now dispatch (show the form).
    * Template: `registration/password_reset_confirm.html`.
  * POST flow:
    * Same as 2nd get flow.
    * The POST flow of the dispatch says to...
    * Will check the validity of the submitted `SetPassword` form.
    * Saves the `SetPassword` form.
    * If `post_reset_login` is set (default `False`), will perform a
      login for the user.
    * Last, will redirect to `success_url`, which is by default
      `password_reset_complete`.
  * BTW, if ever the token is invalid, it will render the form, but with
    context `validlink = False`. So you can display an error.
* `accounts/reset/done` (url name: `password_reset_complete`)
  * A typical view that is shown if password reset was completed
    successfully.
  * Template: `registration/password_reset_complete.html`
