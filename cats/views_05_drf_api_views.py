from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView, Request, Response
from .models import Cat

# We'll learn more about serializers another time. For now, we can just
# know this handles serialization to JSON.
class CatSerializer(ModelSerializer):
  class Meta:
    model = Cat
    fields = ["id", "age", "view_count"]

# `rest_framework.APIView` is mostly just a subclass of
# `django.generic.View`. But it is passed `rest_framework.Request`
# objects, which are a little nicer.

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
