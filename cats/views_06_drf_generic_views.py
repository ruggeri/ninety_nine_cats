from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.serializers import ModelSerializer
from .models import Cat

# We'll learn more about serializers another time. For now, we can just
# know this handles serialization to JSON.
class CatSerializer(ModelSerializer):
  class Meta:
    model = Cat
    fields = ["id", "age", "view_count"]

# There are all sorts of generic APIViews (`ListAPIView`,
# `ListCreateAPIView`, `RetrieveAPIView`,
# `RetrieveUpdateDestroyAPIView`, et cetera). These are all just very
# trivial variants that map `#get`/`#post`/`#delete` HTTP methods to
# `#list`, `#retrieve`, `#create`, `#destroy` implementations.
#
# The class at the heart of all this is `GenericAPIView`.

class CatsListView(ListAPIView):
  # Specify the queryset
  queryset = Cat.objects.all()
  # Specify the serializer
  serializer_class = CatSerializer

  # `ListAPIView` maps `#get` to `ListModelMixin#list`. This in turn
  # calls `GenericAPIView#get_queryset`. Filtering and pagination will
  # also be performed. Finally, serialization is done.

class CatsDetailView(RetrieveAPIView):
  # We still actually need to provide a queryset so that `get_object`
  # knows what to select from.
  queryset = Cat.objects.all()
  # `GenericAPIView#get_object` uses this to find the specified object.
  lookup_url_kwarg = "cat_id"
  serializer_class = CatSerializer

  # The `RetrieveAPIView` maps `#get` to `RetrieveModelMixin#retrieve`.
  # This in turn calls `GenericAPIView#get_object`.

# Later we can look at other variants that create, update and destroy.
