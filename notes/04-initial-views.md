## Initial Views

Let's add some list and details views/routes. Here are the routes:

```python
# cats/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cats_list, name="list"),
    # Notice the URL parameter
    path('<int:cat_id>', views.cats_detail, name="detail"),
]
```

Next, here are the views:

```python
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
```

And now, we make our templates! We put them in `cats/templates/cats/`.
Sigh. Why not just `cats/templates`? It looks like
`django.template.loader` will load a template by name in *any* app's
templates directory: it chooses the first that matches. So we need to
make our template name globally unique by naming it
`cats/cats_list.html`.

Here is our `cats/cats_list.html` template:

```html
{% if cats %}
<ul>
  {% for cat in cats %}
  <li>
    <a href="/cats/{{cat.id}}">{{cat.name}}</a>
  </li>
  {% endfor %}
</ul>
{% else %}
<h1>THERE ARE NO CATS</h1>
{% endif %}
```

Notice that the if will display something different if the `cats` list
is empty. Also note how I laboriously construct the url by hand.

There is also a shortcut way to render a template using
`django.shortcuts.render`.

```python
from django.http import HttpResponse
from django.shortcuts import render
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
  cat = Cat.objects.get(id=cat_id)
  context = {'cat': cat}
  return render(request, 'cats/cats_detail.html', context)
```

## Detail View

Here is our Django template for the detail template:

```
<h1>{{cat.name}}</h1>

{% if toys %}
<ul>
  {% for toy in toys %}
  <li>{{toy.name}}</li>
  {% endfor %}
</ul>
{% else %}
<h3>THERE ARE NO TOYS FOR THIS CAT</h3>
{% endif %}

<a href="/cats">Back to cats list</a>
```

And here is our improved view code:

```python
# The URL parameter gets passed in keyword-style.
def cats_detail(request, cat_id: int):
  cat = Cat.objects.get(id=cat_id)
  context = {'cat': cat, 'toys': list(cat.toy_set.all())}
  return render(request, 'cats/cats_detail.html', context)
```

## 404'd!

There is a shortcut that will raise a 404 error if a specified object is
not found.

```python
# cats/views.py
from django.shortcuts import get_object_or_404, render

# The URL parameter gets passed in keyword-style.
def cats_detail(request, cat_id: int):
  cat = get_object_or_404(Cat, id=cat_id)
  context = {'cat': cat, 'toys': list(cat.toy_set.all()}
  return render(request, 'cats/cats_detail.html', context)
```

## Url Helper

Because we named our URL routes, we can use a helper in the Django
templates:

```
<a href="{% url "list" %}">Back to cats list</a>

<a href="{% url "detail" cat.id %}">{{cat.name}}</a>
```

They immediately address the problem of namespacing. It's simple:

```python
# in cats/url.py
app_name = 'cats'
```

```
<a href="{% url "cats:list" %}">Back to cats list</a>

<a href="{% url "cats:detail" cat.id %}">{{cat.name}}</a>
```
