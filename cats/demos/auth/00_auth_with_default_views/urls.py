from django.urls import path
from . import views

# The easiest way of setting up auth is to add the line:
#
# urls = [path('accounts/', include('django.contrib.auth.urls'))]
#
# But this gives no real control over the auth setup. Here is a more
# customized way.

app_name = "cats"
urlpatterns = [
    path(
        "accounts/login/",
        views.LoginView.as_view(),
    ),
    path(
        "accounts/logout/",
        views.LogoutView.as_view(),
    ),

    # Route to show the user's profile name.
    path(
        "accounts/profile/",
        views.profile_detail,
        name="profile-detail",
    )
]
