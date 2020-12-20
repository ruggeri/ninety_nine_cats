from django.urls import path
from . import views

app_name = 'cats'
urlpatterns = [
    path('', views.cats_list, name="list"),
    path('<int:cat_id>', views.cats_detail, name="detail"),
]
