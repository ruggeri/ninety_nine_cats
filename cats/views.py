from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
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

def cats_new(request):
  cat = Cat()
  context = {'cat': cat}
  return render(request, 'cats/cats_new.html', context)

def cats_create(request: HttpRequest):
  cat = Cat(name=request.POST['name'], age=request.POST['age'])
  cat.save()

  # Trigger a re-direct to the cats:detail page for the newly created
  # cat. Notice how we use `django.urls.reverse` to create a url to
  # redirect to.
  return HttpResponseRedirect(reverse('cats:detail', args=(cat.id, )))
