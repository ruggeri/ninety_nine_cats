from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.views import Request, Response
from rest_framework.viewsets import ViewSet
from cats.models import Cat

# We'll learn more about serializers another time. For now, we can just
# know this handles serialization to JSON.
class CatSerializer(ModelSerializer):
  class Meta:
    model = Cat
    fields = ["id", "age", "view_count"]

# A `rest_framework.viewsets.ViewSet` is a lot like a Rails controller.
# More than one path can point to the `ViewSet`, and it will be
# dispatched to the appropriate `ViewSet` method.
#
# The primitive `ViewSet` class inherits from `APIView`.

class CatsViewSet(ViewSet):
  def list(self, request: Request):
    cats = Cat.objects.all()
    if "q" in request.query_params:
      cats = cats.filter(name__icontains=request.query_params["q"])

    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)

  # You'll make life easier for yourself if you use pk here. The name of
  # this parameter is chosen by the *router*, and `pk` will be the
  # default.
  def retrieve(self, request: Request, pk: int):
    cat = get_object_or_404(Cat, id=pk)
    serializer = CatSerializer(cat)
    return Response(serializer.data)

# Make sure to look at urls.py to see how the router is set up. The
# router is necessary because we can't simply call `as_view()` anymore.
