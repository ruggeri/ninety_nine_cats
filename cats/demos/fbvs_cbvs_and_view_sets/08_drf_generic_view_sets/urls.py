from rest_framework.routers import DefaultRouter
from . import views

app_name = 'cats'
urlpatterns = []

# `DefaultRouter` maps `/cats` and `/cats/{pk}` to appropriate methods
# in the `ViewSet`. It also creates url names like `cats-detail` and
# `cats-list`.
router = DefaultRouter()
router.register("cats", views.CatsViewSet, basename="cats")
urlpatterns += router.urls
