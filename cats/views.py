from django.http import HttpResponse
from django.template import loader
from .models import Cat

def cats_list(request):
  # Fetching models
  cats = Cat.objects.all()
  # Loading templates
  template = loader.get_template('cats/cats_list.html')
  # The template context
  context = {'cats': cats}
  # Rendering!
  return HttpResponse(template.render(context, request))

# The URL parameter gets passed in keyword-style.
def cats_detail(request, cat_id: int):
  cat = Cat.objects.get(id=cat_id)
  template = loader.get_template('cats/cats_detail.html')
  context = {'cat': cat}
  return HttpResponse(template.render(context, request))
