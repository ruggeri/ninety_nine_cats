from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from cats.models import Cat

# This shows how to use basic django view functions. This is the
# lowest-level way to do things.

def cats_list(request: HttpRequest):
  cats = Cat.objects.all()
  data = serializers.serialize("json", cats)
  return HttpResponse(data, content_type="application/json")

# This version does not use any helper.

# def cats_detail(request: HttpRequest, cat_id: int):
#   try:
#     cat = Cat.objects.get(id=cat_id)
#   except Cat.DoesNotExist:
#     return HttpResponse(
#         "Cat does not exist", content_type="text/text", status=404
#     )

#   data = serializers.serialize("json", [cat])
#   return HttpResponse(data, content_type="application/json")

# The URL is going to be passed in as a kwarg by urls.py.
def cats_detail(request: HttpRequest, cat_id: int):
  # This version will raise a 404 exception for us if the specified
  # `Cat` does not exist.
  cat = get_object_or_404(Cat, id=cat_id)
  data = serializers.serialize("json", [cat])
  return HttpResponse(data, content_type="application/json")
