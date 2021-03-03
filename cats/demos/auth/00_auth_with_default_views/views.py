from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.urls import reverse

class LoginView(auth_views.LoginView):
  # Use standard admin login template.
  template_name = "admin/login.html"

  # This is usually configured with settings.LOGIN_REDIRECT_URL (set to
  # "/accounts/profile" by default). But I want to try to avoid touching
  # settings.py in these demos...
  def get_success_url(self):
    # Use the redirect URL in the query params if it exists.
    url = self.get_redirect_url()
    if url:
      return url

    # Else send them to the default profile page.
    return reverse("cats:profile-detail")

# Simply log them out and send them back to the login page.
class LogoutView(auth_views.LogoutView):
  next_page = "/cats/accounts/login/"

# The @login_required decorator will bounce them to the configured
# standard login URL. It will set the `next` query parameter
# appropriately.
@login_required(login_url="/cats/accounts/login")
def profile_detail(request: HttpRequest):
  return HttpResponse(request.user.username, content_type="text/text")
