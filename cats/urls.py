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

# from . import views_04_list_and_detail_views
# urlpatterns = [
#     path(
#         "cats/",
#         views_04_list_and_detail_views.CatsListView.as_view(),
#         name="cats_list"
#     ),
#     path(
#         "cats/<int:cat_id>",
#         views_04_list_and_detail_views.CatsDetailView.as_view(),
#         name="cats_detail"
#     ),
# ]

# from . import views_05_drf_api_views
# urlpatterns = [
#     path(
#         "cats/",
#         views_05_drf_api_views.CatsListView.as_view(),
#         name="cats_list"
#     ),
#     path(
#         "cats/<int:cat_id>",
#         views_05_drf_api_views.CatsDetailView.as_view(),
#         name="cats_detail"
#     ),
# ]

# from . import views_06_drf_generic_views
# urlpatterns = [
#     path(
#         "cats/",
#         views_06_drf_generic_views.CatsListView.as_view(),
#         name="cats_list"
#     ),
#     path(
#         "cats/<int:cat_id>",
#         views_06_drf_generic_views.CatsDetailView.as_view(),
#         name="cats_detail"
#     ),
# ]

# from . import views_07_drf_view_sets
# from rest_framework.routers import DefaultRouter

# # `DefaultRouter` maps `/cats` and `/cats/{pk}` to appropriate methods
# # in the `ViewSet`. It also creates url names like `cats-detail` and
# # `cats-list`.
# router = DefaultRouter()
# router.register(
#     "cats", views_07_drf_view_sets.CatsViewSet, basename="cats"
# )
# urlpatterns = []
# urlpatterns += router.urls

from . import views_08_drf_generic_view_sets
from rest_framework.routers import DefaultRouter

# `DefaultRouter` maps `/cats` and `/cats/{pk}` to appropriate methods
# in the `ViewSet`. It also creates url names like `cats-detail` and
# `cats-list`.
router = DefaultRouter()
router.register(
    "cats", views_08_drf_generic_view_sets.CatsViewSet, basename="cats"
)
urlpatterns = []
urlpatterns += router.urls
