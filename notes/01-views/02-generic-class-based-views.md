## Generic Class Based Views

## `ListView`

This simply fetches all the objects and renders a template:

```python
# urls.py
path('', views.CatsListView.as_view(), name="list"),

# views.py
class CatsListView(generic.ListView):
  # The name of the model to fetch.
  model = Cat
  # You can specify. Else it is `model_app_name/model_name.html`.
  template_name = 'cats/cats_list.html'
```

In the template, you'll get a property called `objects_list`. It will
also set a property based on the name of the model object: `cats_list`,
for instance. But if you want a different name, you can add a class
property: `context_object_name = 'cats'`. This allows you to choose a
more meaningful, less machine-generated name.

You can specify a `queryset` property:

```python
class CatsListView(generic.ListView):
  # Can set to any kind of queryset object.
  queryset = Cat.objects.order_by('name').all()

  # Even more dynamic
  def get_queryset(self):
    return Cat.objects.order_by('name').all()
```

The routing parameters are available as `self.kwargs`. Thus, you can use
them in picking the queryset. They give an example:

```python
  # Override how objects are queried for the list.
  def get_queryset(self):
    # Use the request GET parameters.
    if 'name' not in self.request.GET:
      return Cat.objects.order_by('name').all()
    else:
      # A little silly. If someone specifies a name parameter, we can
      # filter all cats with that name.
      return Cat.objects.filter(
          name=self.request.GET['name'],
      ).order_by('name').all()
```

## `DetailView`

Sometimes you want to get data associated with an object. For instance,
say we have a `DetailView` that will show a `Cat`:

```python
class CatsDetailView(generic.DetailView):
  # Will auto infer that context_object_name='cat'
  model = Cat
  template_name = 'cats/cats_detail.html'
```

Say we also want to list the toys of the cat. There is more than one to
approach this, but here is an option:

```python
class CatsDetailView(generic.DetailView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['toys'] = context['cat'].toys.all()
    return context
```

They show an example of doing some extra work as part of fetching a cat:

```python
class CatsDetailView(generic.DetailView):
  def get_object(self, *args, **kwargs):
    # Get the cat in the usual way.
    obj: Cat = super().get_object(*args, **kwargs)
    # But now increment the view_count.
    obj.view_count += 1
    obj.save()
    return obj
```
