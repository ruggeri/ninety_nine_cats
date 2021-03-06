import importlib

url_module_names = [
    "cats.demos.fbvs_cbvs_and_view_sets.00_simple_view_functions.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.01_template_view_functions.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.02_simple_class_based_views.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.03_template_class_based_views.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.04_list_and_detail_views.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.05_drf_api_views.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.06_drf_generic_views.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.07_drf_view_sets.urls",
    "cats.demos.fbvs_cbvs_and_view_sets.08_drf_generic_view_sets.urls",
    "cats.demos.auth.00_auth_with_default_views.urls",
    "cats.demos.auth.01_auth_with_handroll_login_and_logout_views.urls",
]

urls_module = importlib.import_module(
    "cats.demos.auth.00_auth_with_default_views.urls",
)

# mypy: ignore-errors
app_name = urls_module.app_name
urlpatterns = urls_module.urlpatterns
