from django.urls import path
from . import views

urlpatterns = [
    path('', views.cats_list, name="list"),
    path('<int:cat_id>', views.cats_detail, name="detail"),
]
