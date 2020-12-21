from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Cat

class CatsListView(generic.ListView):
  template_name = 'cats/cats_list.html'
  # specify what the object list should be called.
  context_object_name = 'cats'

  # Override how objects are queried for the list.
  def get_queryset(self):
    return Cat.objects.order_by('name').all()

class CatsDetailView(generic.DetailView):
  # Will auto infer that context_object_name='cat'
  model = Cat
  # URLConf wants to pass in arg as cat_id.
  pk_url_kwarg = 'cat_id'
  template_name = 'cats/cats_detail.html'

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
