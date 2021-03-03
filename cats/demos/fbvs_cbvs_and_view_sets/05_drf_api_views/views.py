from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView, Request, Response
from cats.models import Cat

# We'll learn more about serializers another time. For now, we can just
# know this handles serialization to JSON.
class CatSerializer(ModelSerializer):
  class Meta:
    model = Cat
    fields = ["id", "age", "view_count"]

# `rest_framework.APIView` is mostly just a subclass of
# `django.generic.View`. It dispatches by method name similarly. But
# `APIView` is passed `rest_framework.views.Request` objects, which are
# a little nicer.
#
# And it can happily be returned `rest_framework.views.Response`
# objects. This is how DRF can do automagic content negotiation for us.

class CatsListView(APIView):
  def get(self, request):
    if "q" in request.query_params:
      cats = Cat.objects.filter(
          name__icontains=request.query_params["q"]
      )
    else:
      cats = Cat.objects.all()

    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)

class CatsDetailView(APIView):
  def get(self, request: Request, cat_id: int):
    cat = get_object_or_404(Cat, id=cat_id)
    serializer = CatSerializer(cat)
    return Response(serializer.data)
