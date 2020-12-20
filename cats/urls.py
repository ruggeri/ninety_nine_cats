from django.urls import path
from . import views

app_name = 'cats'
urlpatterns = [
    path('', views.cats_list, name="list"),
    path('new', views.cats_new, name="new"),
    path('create', views.cats_create, name="create"),
    path('<int:cat_id>', views.cats_detail, name="detail"),
]
