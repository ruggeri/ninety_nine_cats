from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from cats.models import Cat

# We'll learn more about serializers another time. For now, we can just
# know this handles serialization to JSON.
class CatSerializer(ModelSerializer):
  class Meta:
    model = Cat
    fields = ["id", "age", "view_count"]

# `rest_framework.viewsets.ReadOnlyModelViewSet` derives from
# `GenericViewSet`. While `ViewSet` derives from `APIView`,
# `GenericViewSet` derives from `GenericAPIView`. This means that
# `GenericViewSet` has `get_queryset` and `get_object` methods.
#
# `ReadOnlyModelViewSet` simply mixes in `ListModelMixin` and
# `RetrieveModelMixin`. This adds `list` and `retrieve` methods, which
# the `DefaultRouter` will find and create routes for.
#
# If we wanted to support all five CRUD actions, we would extend
# `ModelViewSet`, which mixes in the remaining CRUD mixins.

class CatsViewSet(ReadOnlyModelViewSet):
  queryset = Cat.objects.all()
  serializer_class = CatSerializer

  # We'll get the `list` and `retrieve` methods for free!
