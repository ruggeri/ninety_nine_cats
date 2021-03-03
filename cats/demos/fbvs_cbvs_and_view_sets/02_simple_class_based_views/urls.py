from django.urls import path
from . import views

app_name = 'cats'
urlpatterns = [
    path("cats/", views.CatsListView.as_view(), name="cats_list"),
    path(
        "cats/<int:cat_id>/",
        views.CatsDetailView.as_view(),
        name="cats_list"
    ),
]
