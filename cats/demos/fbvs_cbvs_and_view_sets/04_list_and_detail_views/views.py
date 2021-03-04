from django.views import generic
from cats.models import Cat

# The `ListView` and `DetailView` are helpful view classes for the most
# typical REST type endpoints.

class CatsListView(generic.ListView):
  model = Cat
  template_name = "cats/cats_list_01.html"

  # Has a `#get_queryset` method which will get all the cats for us. It
  # will also, if configured appropriately, do ordering and pagination
  # for us.
  #
  # If we wanted to filter the cats returned by a URL parameter, we
  # could override `#get_queryset` and use `self.kwargs` or
  # `self.request.GET`.
  def get_queryset(self):
    if "q" in self.request.GET:
      return self.model.objects.filter(
          name__icontains=self.request.GET["q"]
      )
    else:
      return self.model.objects.all()

  # `get` will render the template. What context does it provide? This
  # is defined by `#get_context_data`. The most important parameter is
  # `object_list`.
  #
  # As an alias for `object_list`, `cat_list` will also be provided as
  # template context. To configure this yourself, set
  # `context_object_name` as I have.

  context_object_name = "cats"

class CatsDetailView(generic.DetailView):
  model = Cat
  template_name = "cats/cats_detail_01.html"
  # The default URL kwarg is "pk".
  pk_url_kwarg = "cat_id"

  # There is a `get_object` method that will fetch the requested object.
  # If it doesn't exist, a 404 is thrown.
  #
  # Here I add some extra functionality around getting the object.
  # Probably bad practice though to do this here. Should probably
  # override the get method myself...
  def get_object(self, queryset=None):
    cat: Cat = super().get_object(queryset)
    cat.view_count += 1
    cat.save()
    return cat

  # By default the context includes just `"object"` (alias "cat",
  # inferred from the model name). If we need more, we can override.
  def get_context_data(self, **kwargs):
    # Could extend like this:
    #
    # context = super().get_context_data(**kwargs)
    # context["toys"] = context.cat

    # Probably simpler:
    cat = self.object
    toys = cat.toys.all()
    return {"cat": cat, "toys": toys}
