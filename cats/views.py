from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from .models import Cat

# class CatsListView(generic.ListView):
#   template_name = 'cats/cats_list.html'
#   # specify what the object list should be called.
#   context_object_name = 'cats'

#   # Override how objects are queried for the list.
#   def get_queryset(self):
#     # Use the request GET parameters.
#     if 'name' not in self.request.GET:
#       return Cat.objects.order_by('name').all()
#     else:
#       # A little silly. If someone specifies a name parameter, we can
#       # filter all cats with that name.
#       return Cat.objects.filter(
#           name=self.request.GET['name'],
#       ).order_by('name').all()

# class CatsDetailView(generic.DetailView):
#   # Will auto infer that context_object_name='cat'
#   model = Cat
#   # URLConf wants to pass in arg as cat_id.
#   pk_url_kwarg = 'cat_id'
#   template_name = 'cats/cats_detail.html'

#   def get_object(self, *args, **kwargs):
#     obj: Cat = super().get_object(*args, **kwargs)
#     obj.view_count += 1
#     obj.save()
#     return obj

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['toys'] = context['cat'].toys.all()
#     return context

from rest_framework import viewsets
from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
  def has_permission(self, request: HttpRequest, view):
    return request.user.is_authenticated

class CanSayHelloToCats(BasePermission):
  def has_permission(self, request: HttpRequest, view):
    return not request.user.has_perm("cats.say_hello_cat")

class CatsViewSet(viewsets.ViewSet):
  permission_classes = [IsAuthenticated, CanSayHelloToCats]

  def list(self, request):
    # if request.user.is_anonymous:
    #   return redirect(reverse("cats:login"))

    # if request.user.has_perm("cats.say_hello_cat"):
    cat = Cat.objects.get(id=request.user.id)
    data = serializers.serialize("json", [cat])
    return HttpResponse(data, content_type="application/json")
    # else:
    #   return HttpResponse(
    #       "you're not allowed to say hello to cats", status=403
    #   )

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

def login(request: HttpRequest):
  if request.method == "GET":
    return render(
        request,
        "cats/user_login_form.html", {
            "username": "", "password": ""
        }
    )
  elif request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate(
        request, username=username, password=password
    )
    if user is None:
      return render(
          request,
          "cats/user_login_form.html", {
              "username": username, "password": password
          }
      )
    else:
      auth.login(request, user)
      return redirect(reverse("cats:list"))
  else:
    raise Exception("Method not supported!")

def logout(request: HttpRequest):
  auth.logout(request)
  return redirect(reverse("cats:login"))
