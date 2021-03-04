from django.urls import path
from . import views

app_name = "cats"
urlpatterns = [
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path(
        "accounts/logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),

    # Route to show the user's profile name.
    path(
        "accounts/profile/",
        views.profile_detail,
        name="profile-detail",
    )
]
