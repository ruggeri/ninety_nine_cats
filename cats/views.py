from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Cat

def cats_list(request):
  # Fetching models
  cats = Cat.objects.all()
  # The template context
  context = {'cats': cats}
  # Rendering!
  return render(request, 'cats/cats_list.html', context)

# The URL parameter gets passed in keyword-style.
def cats_detail(request, cat_id: int):
  cat = get_object_or_404(Cat, id=cat_id)
  context = {'cat': cat, 'toys': list(cat.toy_set.all())}
  return render(request, 'cats/cats_detail.html', context)
