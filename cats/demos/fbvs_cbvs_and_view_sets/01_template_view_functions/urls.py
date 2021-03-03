from django.urls import path
from . import views

app_name = 'cats'
urlpatterns = [
    path("cats/", views.cats_list, name="cats_list"),
    path("cats/<int:cat_id>/", views.cats_detail, name="cats_detail"),
]
