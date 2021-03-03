from django.contrib import auth
from django.contrib.auth import forms
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, View
from django.http import HttpResponse, HttpRequest
from django.urls import reverse

class LoginView(View):
  def get(self, request: HttpRequest):
    if "next" in request.GET:
      next_path = request.GET["next"]
    else:
      # Whatever default we want for testing...
      next_path = "/nowhere"

    # I'm just lazy and won't specify the next.
    context = {
        "form": forms.AuthenticationForm(),
        # I think form will need to upload this.
        "next": next_path,
    }

    return render(request, "admin/login.html", context=context)

  def post(self, request: HttpRequest):
    # Verify their credentials.
    user = auth.authenticate(
        request,
        username=request.POST["username"],
        password=request.POST["password"]
    )

    # If login fails, present the form again.
    if user is None:
      return self.get(request)

    # If login succeeded, find where to redirect the user.
    if "next" in request.POST:
      next_path = request.POST["next"]
    else:
      raise Exception("Expected a next parameter...")

    # Set session data in the cookie.
    auth.login(request, user)

    return redirect(next_path)

# To log the user out, simply clear the session data and send them back
# to the login page.
class LogoutView(RedirectView):
  def get_redirect_url(self, *args, **kwargs):
    return reverse("cats:login")

  def get(self, request: HttpRequest, *args, **kwargs):
    # `auth.logout` clears session data.
    auth.logout(request)
    return super().get(request, *args, **kwargs)

def profile_detail(request: HttpRequest):
  # I forgo the `@login_required` decorator to show how things can be
  # done more manually. I still use the helpful `redirect_to_login`
  # method, though. It conveniently builds the query string for me.
  if request.user.is_anonymous:
    return redirect_to_login(request.path, reverse("cats:login"))

  return HttpResponse(request.user.username, content_type="text/text")
