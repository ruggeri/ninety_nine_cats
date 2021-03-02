from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Cat

# The `generic.TemplateView` class is not clearly superior to using
# `render` directly. Perhaps it requires one fewer import. Plus, it is
# the same idiom as `ListView` and `DetailView` which we will see
# shortly.

class CatsListView(generic.TemplateView):
  # It is the mixin `TemplateResponseMixin` that provides
  # `render_to_response` which uses the `template_name` attribute.
  template_name = "cats/cats_list_01.html"

  def get(self, request: HttpRequest):
    cats = Cat.objects.all()
    return self.render_to_response({"cats": cats})

class CatsDetailView(generic.TemplateView):
  template_name = "cats/cats_detail_01.html"

  def get(self, request: HttpRequest, cat_id: int):
    cat: Cat = get_object_or_404(Cat, id=cat_id)
    toys = cat.toys.all()
    return self.render_to_response({"cat": cat, "toys": toys})
