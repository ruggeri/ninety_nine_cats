from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import Cat

# This shows the most basic way with using `django.template.loader`
# directly.

# def cats_list(request: HttpRequest):
#   cats = Cat.objects.all()
#   template = loader.get_template("cats/cats_list_01.html")
#   context = {"cats": cats}
#   content = template.render(context, request)
#   return HttpResponse(content)

# def cats_detail(request: HttpRequest, cat_id: int):
#   cat = get_object_or_404(Cat, id=cat_id)
#   toys = cat.toys.all()
#   template = loader.get_template("cats/cats_detail_01.html")
#   context = {"cat": cat, "toys": toys}
#   content = template.render(context, request)
#   return HttpResponse(content)

# This will use `django.shortcut.render`.

def cats_list(request: HttpRequest):
  cats = Cat.objects.all()
  context = {"cats": cats}
  return render(request, "cats/cats_list_01.html", context)

def cats_detail(request: HttpRequest, cat_id: int):
  cat = get_object_or_404(Cat, id=cat_id)
  toys = cat.toys.all()
  context = {"cat": cat, "toys": toys}
  return render(request, "cats/cats_detail_01.html", context)
