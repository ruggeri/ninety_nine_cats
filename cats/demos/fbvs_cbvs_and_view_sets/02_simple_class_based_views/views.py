from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from cats.models import Cat

# `generic.View` is a starting point for class-based views. It defines a
# `#dispatch` method that will dispatch to the appropriate view method
# based on HTTP method. This allows you to separate code for, for
# instance, GET and POST requests.
#
# In `urls.py`, you will see that we need to call `#as_view` on this
# class.
#
# `generic.View` is used as a parent class for other class-based views
# that add more functionality.

class CatsListView(generic.View):
  def get(self, request: HttpRequest):
    cats = Cat.objects.all()
    data = serializers.serialize("json", cats)
    return HttpResponse(data, content_type="application/json")

class CatsDetailView(generic.View):
  def get(self, request: HttpRequest, cat_id: int):
    cat = get_object_or_404(Cat, id=cat_id)
    data = serializers.serialize("json", [cat])
    return HttpResponse(data, content_type="application/json")
