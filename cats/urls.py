from django.urls import path

app_name = 'cats'

# from . import views_00_simple_view_functions
# urlpatterns = [
#     path(
#         "cats/",
#         views_00_simple_view_functions.cats_list,
#         name="cats_list"
#     ),
#     path(
#         "cats/<int:cat_id>",
#         views_00_simple_view_functions.cats_detail,
#         name="cats_detail"
#     ),
# ]

# from . import views_01_template_view_functions
# urlpatterns = [
#     path("cats/", views_01_template_view_functions.cats_list, name="cats_list"),
#     path(
#         "cats/<int:cat_id>",
#         views_01_template_view_functions.cats_detail,
#         name="cats_detail"
#     ),
# ]

# from . import views_02_simple_class_based_views
# urlpatterns = [
#     path(
#         "cats/",
#         views_02_simple_class_based_views.CatsListView.as_view(),
#         name="cats_list"
#     ),
#     path(
#         "cats/<int:cat_id>",
#         views_02_simple_class_based_views.CatsDetailView.as_view(),
#         name="cats_list"
#     ),
# ]

# from . import views_03_template_class_based_views
# urlpatterns = [
#     path(
#         "cats/",
#         views_03_template_class_based_views.CatsListView.as_view(),
#         name="cats_list"
#     ),
#     path(
#         "cats/<int:cat_id>",
#         views_03_template_class_based_views.CatsDetailView.as_view(),
#         name="cats_detail"
#     ),
# ]

from . import views_04_list_and_detail_views
urlpatterns = [
    path(
        "cats/",
        views_04_list_and_detail_views.CatsListView.as_view(),
        name="cats_list"
    ),
    path(
        "cats/<int:cat_id>",
        views_04_list_and_detail_views.CatsDetailView.as_view(),
        name="cats_detail"
    ),
]
